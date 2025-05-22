import os
import logging
import json
from flask import Flask, render_template, Response, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from camera import Camera, PostureThresholds
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from datetime import datetime
import time
import math

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex())

# Print template/static paths for debugging
print("Template folder path:", app.template_folder)
print("Static folder path:", app.static_folder)

# Configure SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=True,
    ping_timeout=5000,
    ping_interval=2500,
    max_http_buffer_size=1e8,
    reconnection=True,
    reconnection_attempts=5,
    reconnection_delay=1000,
    reconnection_delay_max=5000
)

camera = None

def parse_timestamp(ts):
    """
    Attempts to parse a timestamp that might be:
    - int/float epoch time
    - numeric string epoch time
    - ISO8601 string
    Returns a datetime object.
    """
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(float(ts))
    if isinstance(ts, str):
        # Try to parse as float (epoch time)
        try:
            return datetime.fromtimestamp(float(ts))
        except ValueError:
            # Otherwise, try ISO8601 (or any known format)
            try:
                return datetime.fromisoformat(ts)
            except ValueError:
                raise ValueError(f"Unsupported timestamp format: {ts}")
    raise ValueError(f"Unsupported timestamp type: {type(ts)} ({ts})")

def get_camera():
    """
    Returns the global camera instance. If it's not initialized,
    create it (pc_camera by default), or if something fails, create a test_mode camera.
    """
    global camera
    if camera is None:
        try:
            camera = Camera(camera_type='pc_camera', test_mode=False)
            # Example: you could set a frame_buffer_size property if you like
            # camera.frame_buffer_size = 10
            logger.info("Camera initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            camera = Camera(test_mode=True)
    return camera

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/capture_measurement', methods=['POST'])
def capture_measurement():
    try:
        data = request.json
        if not data or not all(key in data for key in ['shoulder_angle', 'hip_angle', 'tilt_angle']):
            raise ValueError("Missing required measurement data")

        cam = get_camera()
        result = cam.capture_measurement(data)
        
        if result and result.get('success'):
            return jsonify(result)
        else:
            raise ValueError(result.get('error', 'Failed to save measurement'))
            
    except Exception as e:
        logger.error(f"Error capturing measurement: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history')
def history():
    try:
        cam = get_camera()
        captured_measurements = cam.get_measurements_history()
        
        if not captured_measurements:
            return render_template('history.html', history=[], history_json=json.dumps([]))
        
        history_data = []
        for m in captured_measurements:
            try:
                dt = parse_timestamp(m.timestamp)
                history_data.append({
                    'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'measurements': {
                        'shoulder_angle': round(float(m.shoulder_angle), 1),
                        'hip_angle': round(float(m.hip_angle), 1),
                        'tilt_angle': round(float(m.tilt_angle), 1)
                    }
                })
            except Exception as e:
                logger.error(f"Error processing measurement: {e}")
                continue

        return render_template('history.html',
                               history=history_data,
                               history_json=json.dumps(history_data))
    except Exception as e:
        logger.error(f"Error rendering history page: {e}")
        return render_template('error.html', error=str(e))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        cam = get_camera()
        cam.clear_measurements()
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({'error': str(e)}), 500

def generate_frames():
    cam = get_camera()
    last_emit_time = 0
    emit_interval = 1/30  # Limit to ~30 FPS for socket emissions
    
    while True:
        try:
            frame, measurements = cam.get_frame()
            if frame is not None:
                current_time = time.time()
                
                # Throttle measurement emissions
                if measurements and (current_time - last_emit_time) >= emit_interval:
                    try:
                        data = {
                            'shoulder_angle': round(float(measurements.shoulder_angle), 2),
                            'hip_angle': round(float(measurements.hip_angle), 2),
                            'tilt_angle': round(float(measurements.tilt_angle), 2)
                        }
                        socketio.emit('measurements', data)
                        last_emit_time = current_time
                    except Exception as e:
                        logger.error(f"Error emitting measurements: {e}")
                        continue

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
                # Add small sleep to prevent CPU overload
                time.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Error generating frames: {e}")
            time.sleep(0.1)
            continue

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_thresholds')
def get_thresholds():
    try:
        cam = get_camera()
        return jsonify({
            'shoulder_threshold': cam.thresholds.shoulder_threshold,
            'hip_threshold': cam.thresholds.hip_threshold,
            'tilt_threshold': cam.thresholds.tilt_threshold
        })
    except Exception as e:
        logger.error(f"Error getting thresholds: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_thresholds', methods=['POST'])
def update_thresholds():
    try:
        data = request.json
        cam = get_camera()
        thresholds = cam.update_thresholds(
            shoulder=data.get('shoulder_threshold'),
            hip=data.get('hip_threshold'),
            tilt=data.get('tilt_threshold')
        )
        return jsonify({
            'shoulder_threshold': thresholds.shoulder_threshold,
            'hip_threshold': thresholds.hip_threshold,
            'tilt_threshold': thresholds.tilt_threshold
        })
    except Exception as e:
        logger.error(f"Error updating thresholds: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/generate_report')
def generate_report():
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.utils import ImageReader

        cam = get_camera()
        captured_measurements = cam.get_measurements_history()
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Add logos
        try:
            hhn_logo = ImageReader(os.path.join(app.static_folder, 'img', 'hhn_logo.png'))
            p.drawImage(hhn_logo, 50, height - 100, width=100, height=80, mask='auto')
            
            unity_logo = ImageReader(os.path.join(app.static_folder, 'img', 'unityLab.jpg'))
            p.drawImage(unity_logo, width - 120, height - 80, width=70, height=60, mask='auto')
        except Exception as e:
            logger.error(f"Error loading logos: {e}")

        # Title and header
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, height - 150, "Scoliosis Analysis Report")
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 180, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if captured_measurements:
            # Most recent measurement
            last_measurement = captured_measurements[0]
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 220, "Latest Captured Measurement")
            p.setFont("Helvetica", 12)
            y = height - 250

            measurements_info = [
                ("Shoulder Angle", last_measurement.shoulder_angle, 5),
                ("Hip Angle", last_measurement.hip_angle, 5),
                ("Frame Tilt", last_measurement.tilt_angle, 2)
            ]

            for label, value, threshold in measurements_info:
                # Color code logic
                if abs(value) <= threshold:
                    color = '#52c41a'    # green
                elif abs(value) <= threshold * 2:
                    color = '#faad14'  # orange
                else:
                    color = '#f5222d'  # red

                # Convert hex color -> RGB
                r = int(color[1:3], 16) / 255.0
                g = int(color[3:5], 16) / 255.0
                b = int(color[5:7], 16) / 255.0
                p.setFillColorRGB(r, g, b)

                p.drawString(70, y, f"{label}: {value:.1f}°")
                y -= 20

            # History section
            if len(captured_measurements) > 1:
                p.showPage()

                # Redraw logos on the new page
                try:
                    p.drawImage(hhn_logo, 50, height - 100, width=100, height=80, mask='auto')
                    p.drawImage(unity_logo, width - 120, height - 80, width=70, height=60, mask='auto')
                except Exception as e:
                    logger.error(f"Error loading logos on second page: {e}")

                p.setFont("Helvetica-Bold", 16)
                p.drawString(50, height - 150, "Measurement History")
                p.setFont("Helvetica", 12)
                y = height - 180

                # Show all measurements in history
                for m in captured_measurements:
                    try:
                        dt = parse_timestamp(m.timestamp)
                        timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        logger.error(f"Error parsing timestamp in generate_report: {e}")
                        continue

                    status = "Good" if (
                        abs(m.shoulder_angle) <= 5 and
                        abs(m.hip_angle) <= 5 and
                        abs(m.tilt_angle) <= 2
                    ) else "Needs Attention"

                    # Draw the text
                    p.drawString(
                        70,
                        y,
                        f"Time: {timestamp_str} - Status: {status} | "
                        f"Shoulder: {m.shoulder_angle:.1f}° | "
                        f"Hip: {m.hip_angle:.1f}° | "
                        f"Tilt: {m.tilt_angle:.1f}°"
                    )
                    y -= 20

                    # Paginate if out of space
                    if y < 50:
                        p.showPage()
                        p.setFont("Helvetica", 12)
                        y = height - 50

        p.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name = f'scoliosis_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

# ------------------------------------------------------------------
# NEW: Route to list camera indices for the user
# ------------------------------------------------------------------
@app.route('/camera_list')
def camera_list():
    """
    List available camera indices on this machine.
    """
    cam = get_camera()
    indices = cam.list_camera_indices(max_test=5)
    return jsonify({"available_indices": indices})

# ------------------------------------------------------------------
# NEW: Route to select a camera type/index
# ------------------------------------------------------------------
@app.route('/select_camera', methods=['POST'])
def select_camera():
    """
    Switch camera type or index based on user input.
    Example JSON payload:
      { "camera_type": "usb_camera", "camera_index": 1 }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    new_type = data.get("camera_type", "pc_camera")
    new_index = data.get("camera_index", None)

    global camera
    try:
        # If an existing camera instance exists, delete it so we can recreate
        if camera is not None:
            del camera
            camera = None

        # Create a fresh camera with the new settings
        camera = Camera(camera_type=new_type, camera_index=new_index, test_mode=False)
        logger.info(f"Switched to {new_type} at index {new_index} successfully.")
        
        return jsonify({
            "camera_type": new_type,
            "camera_index": new_index,
            "message": "Camera selection updated. Check /video_feed"
        })
    except Exception as e:
        logger.error(f"Error selecting camera: {e}")
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    try:
        logger.info("Client connected")
        emit('connection_status', {'status': 'connected'})
    except Exception as e:
        logger.error(f"Error in handle_connect: {e}")
        return False

@socketio.on('disconnect')
def handle_disconnect(sid):
    try:
        logger.info(f"Client disconnected: {sid}")
    except Exception as e:
        logger.error(f"Error in handle_disconnect: {e}")

@socketio.on_error_default
def default_error_handler(e):
    logger.error(f"SocketIO error: {str(e)}")
    emit('error', {'error': str(e)})

if __name__ == '__main__':
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=True,
            allow_unsafe_werkzeug=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")

