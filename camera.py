import cv2
import mediapipe as mp
import numpy as np
from dataclasses import dataclass
import logging
import json
import os
import time
import math

logger = logging.getLogger(__name__)

@dataclass
class PostureMeasurements:
    shoulder_angle: float
    hip_angle: float
    tilt_angle: float
    timestamp: float = None

@dataclass
class PostureThresholds:
    shoulder_threshold: float = 5.0
    hip_threshold: float = 5.0
    tilt_threshold: float = 2.0

class Camera:
    def __init__(self, camera_type='pc_camera', camera_index=None, test_mode=False):
        """
        Initialize the camera object.

        :param camera_type: 'pc_camera' or 'usb_camera'.
        :param camera_index: An integer specifying the device index if known.
        :param test_mode: If True, do not attempt to open any real camera (generates test frames).
        """
        self.video = None
        self.camera_type = camera_type
        self.camera_index = camera_index
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            model_complexity=1
        )
        self.custom_connections = [
            (11, 12),  # Shoulder
            (13, 14),  # Hip
            (23, 24)   # Knee
        ]
        self.RED = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.PINK = (255, 105, 180)

        self.thresholds = self.load_thresholds()
        self.test_mode = test_mode
        self.frame_count = 0
        self.captured_measurements = []

        # If not in test mode, try to open the camera
        if not self.test_mode:
            time.sleep(0.5)  # Small delay before initialization
            self.try_init_camera()
        else:
            logger.info("Starting in test mode")

    def list_camera_indices(self, max_test=5):
        """
        Enumerate camera indices that can be opened successfully.
        Returns a list of indices (e.g. [0, 1]) you can then pick from.

        :param max_test: How many indices to test (0..max_test-1).
        :return: A list of valid camera indices.
        """
        available_indices = []
        for i in range(max_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    available_indices.append(i)
                cap.release()
        return available_indices

    def load_thresholds(self):
        """
        Load posture thresholds from thresholds.json file, if it exists.
        """
        try:
            thresholds_path = os.path.join(os.path.dirname(__file__), 'thresholds.json')
            if os.path.exists(thresholds_path):
                with open(thresholds_path, 'r') as f:
                    data = json.load(f)
                    return PostureThresholds(
                        shoulder_threshold=float(data.get('shoulder_threshold', 5.0)),
                        hip_threshold=float(data.get('hip_threshold', 5.0)),
                        tilt_threshold=float(data.get('tilt_threshold', 2.0))
                    )
        except Exception as e:
            logger.error(f"Error loading thresholds: {e}")
        return PostureThresholds()

    def save_thresholds(self):
        """
        Save current posture thresholds into thresholds.json (atomic replace).
        """
        thresholds_path = None
        temp_path = None
        try:
            thresholds_path = os.path.join(os.path.dirname(__file__), 'thresholds.json')
            temp_path = thresholds_path + '.tmp'
            with open(temp_path, 'w') as f:
                json.dump({
                    'shoulder_threshold': self.thresholds.shoulder_threshold,
                    'hip_threshold': self.thresholds.hip_threshold,
                    'tilt_threshold': self.thresholds.tilt_threshold
                }, f)
            os.replace(temp_path, thresholds_path)
        except Exception as e:
            logger.error(f"Error saving thresholds: {e}")
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    def update_thresholds(self, shoulder=None, hip=None, tilt=None):
        """
        Update thresholds in memory and save them to file.
        """
        if shoulder is not None:
            self.thresholds.shoulder_threshold = float(shoulder)
        if hip is not None:
            self.thresholds.hip_threshold = float(hip)
        if tilt is not None:
            self.thresholds.tilt_threshold = float(tilt)
        self.save_thresholds()
        return self.thresholds

    def try_init_camera(self):
        """
        Attempt to initialize either a PC camera or a USB camera.
        If it fails after several retries, fall back to test_mode.
        """
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # If there's an existing camera open, release it
                if self.video:
                    self.__del__()
                    time.sleep(1)

                if self.camera_type == 'pc_camera':
                    # If a user-specified index is set, try that first
                    index_to_try = self.camera_index if self.camera_index is not None else 0
                    logger.info(f"Attempting to open PC camera at index {index_to_try}...")
                    self.video = cv2.VideoCapture(index_to_try)
                    if self.video.isOpened():
                        self._configure_camera_settings()
                        ret, frame = self.video.read()
                        if ret and frame is not None:
                            logger.info(f"Successfully initialized PC camera at index {index_to_try}")
                            self.test_mode = False
                            return
                    raise Exception("Could not initialize PC camera")

                elif self.camera_type == 'usb_camera':
                    # If a user-specified index is set, try that first
                    if self.camera_index is not None:
                        logger.info(f"Attempting to open USB camera at index {self.camera_index}...")
                        self.video = cv2.VideoCapture(self.camera_index)
                        if self.video.isOpened():
                            # Attempt different resolutions
                            for resolution in [(640, 480), (1280, 720), (800, 600)]:
                                self._configure_camera_settings(*resolution)
                                ret, frame = self.video.read()
                                if ret and frame is not None:
                                    logger.info(f"Successfully initialized USB camera at index {self.camera_index} "
                                                f"with resolution {resolution}")
                                    self.test_mode = False
                                    return
                            # If we get here, release and set None
                            self.video.release()
                            self.video = None
                            logger.warning(f"Failed to read a valid frame from USB camera at index {self.camera_index}. "
                                           "Will fallback to scanning all indices...")

                    # Fallback: scan indices 0..3 with multiple resolutions
                    found_camera = False
                    for i in range(4):
                        logger.info(f"Attempting to open USB camera at index {i}...")
                        self.video = cv2.VideoCapture(i)
                        if self.video.isOpened():
                            for resolution in [(640, 480), (1280, 720), (800, 600)]:
                                self._configure_camera_settings(*resolution)
                                ret, frame = self.video.read()
                                if ret and frame is not None:
                                    logger.info(f"Successfully initialized USB camera on index {i} "
                                                f"with resolution {resolution}")
                                    self.test_mode = False
                                    found_camera = True
                                    break
                            if found_camera:
                                break
                            else:
                                # Release this index and continue
                                self.video.release()
                                self.video = None

                    if not found_camera:
                        raise Exception("Could not find working USB camera")

                    return  # If found_camera is True, we've already returned

            except Exception as e:
                logger.error(f"Camera initialization attempt {retry_count + 1} failed: {e}")
                retry_count += 1
                time.sleep(2)

        logger.warning("All camera initialization attempts failed, falling back to test mode.")
        self.test_mode = True

    def _configure_camera_settings(self, width=640, height=480):
        """
        Configure common OpenCV camera settings for convenience, 
        including width, height, FPS, and buffer size.
        """
        if self.video:
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.video.set(cv2.CAP_PROP_FPS, 30)
            self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def __del__(self):
        """
        Clean up the camera resource when the object is destroyed.
        """
        if self.video:
            try:
                if hasattr(self.video, 'release'):
                    self.video.release()
                    time.sleep(0.5)
                elif hasattr(self.video, 'stop'):
                    self.video.stop()
                    time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error releasing camera: {e}")
            finally:
                self.video = None

    def generate_test_frame(self):
        """
        Generate a synthetic frame for test_mode. Also returns dummy posture measurements.
        """
        try:
            self.frame_count += 1
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

            # Create a moving gradient background
            t = self.frame_count * 0.05
            for i in range(3):
                gradient = (np.sin(t + i * 2) * 127 + 128).astype(np.uint8)
                frame[:, :, i] = gradient

            # Overlay text
            text = f"Test Mode - No {self.camera_type} Available"
            cv2.putText(frame, text, (50, 240), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)

            # Generate fake measurements for testing
            angle = float(np.sin(t) * 10)
            measurements = PostureMeasurements(
                shoulder_angle=angle,
                hip_angle=angle * 0.5,
                tilt_angle=angle * 0.25
            )

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                raise Exception("Failed to encode test frame")

            return jpeg.tobytes(), measurements

        except Exception as e:
            logger.error(f"Error generating test frame: {e}")
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes(), None

    def get_frame(self):
        """
        Capture a frame from the camera (or test frame if test_mode).
        Process it to produce posture measurements and return
        both the JPEG image bytes and the measurements (if any).
        """
        if self.test_mode:
            return self.generate_test_frame()

        try:
            success, frame = self.video.read()
            if not success or frame is None:
                logger.error("Failed to capture frame")
                self.test_mode = True
                return self.generate_test_frame()

            # Flip frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)
            processed_frame, measurements = self.process_frame(frame)

            ret, jpeg = cv2.imencode('.jpg', processed_frame)
            if not ret:
                raise Exception("Failed to encode frame")

            return jpeg.tobytes(), measurements

        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            # Fallback to test frame on error
            return self.generate_test_frame()

    def calculate_frame_tilt(self, frame):
        """
        Estimate the tilt of the entire frame by detecting dominant lines via Hough transform.
        Returns an angle in degrees, or None if no lines are found.
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

            if lines is not None:
                angles = []
                for line in lines:
                    rho, theta = line[0]
                    angle = (theta - np.pi / 2) * (180 / np.pi)
                    angles.append(angle)

                median_angle = np.median(angles)
                return float(median_angle)
            return None
        except Exception as e:
            logger.error(f"Error calculating frame tilt: {e}")
            return None

    def calculate_horizontal_angle(self, point1, point2):
        """
        Calculate the angle between two points relative to the horizontal axis.
        """
        try:
            deltaY = point1[1] - point2[1]
            deltaX = point1[0] - point2[0]
            angle = math.atan2(deltaY, deltaX) * (180.0 / math.pi)
            # Normalize angle into -180 to 180
            angle = (angle + 360) % 360 - 180
            return float(angle)
        except Exception as e:
            logger.error(f"Error calculating horizontal angle: {e}")
            return 0.0

    def rotate_2d(self, point1, point2, target_x, target_y, angle):
        """
        Rotate point2 around point1 by a given angle (in degrees).
        Returns the new (x, y).
        """
        try:
            x1, y1 = point1
            x2, y2 = point2

            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            new_angle = math.radians(angle)

            new_x = target_x + distance * math.cos(new_angle)
            new_y = target_y + distance * math.sin(new_angle)

            return new_x, new_y
        except Exception as e:
            logger.error(f"Error in rotate_2d: {e}")
            return point1

    def draw_dotted_line(self, img, start, end, color, thickness, dot_length=2, space_length=10):
        """
        Draw a dotted line between start and end points.
        """
        try:
            total_length = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
            if total_length == 0:
                return

            num_dots = int(total_length / (dot_length + space_length))
            vector = ((end[0] - start[0]) / total_length, (end[1] - start[1]) / total_length)

            for i in range(num_dots):
                dot_start = (
                    int(start[0] + vector[0] * (i * (dot_length + space_length))),
                    int(start[1] + vector[1] * (i * (dot_length + space_length)))
                )
                dot_end = (
                    int(dot_start[0] + vector[0] * dot_length),
                    int(dot_start[1] + vector[1] * dot_length)
                )
                cv2.line(img, dot_start, dot_end, color, thickness)
        except Exception as e:
            logger.error(f"Error drawing dotted line: {e}")

    def process_frame(self, frame):
        """
        Process a single frame: run MediaPipe Pose detection, compute angles,
        and overlay info on image.
        """
        if frame is None:
            # If something is wrong, generate test frame instead
            test_img, test_meas = self.generate_test_frame()
            # Convert the test_img bytes back to an image for consistency
            nparr = np.frombuffer(test_img, np.uint8)
            test_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return test_frame, test_meas

        try:
            output_image = frame.copy()
            imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(imageRGB)
            height, width, _ = frame.shape
            landmarks = []
            measurements = None

            # Calculate the tilt of the entire frame
            frame_tilt = self.calculate_frame_tilt(frame)
            if frame_tilt is not None:
                cv2.putText(
                    output_image,
                    f"Frame Tilt: {frame_tilt:.2f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )

            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append((
                        int(landmark.x * width),
                        int(landmark.y * height),
                        (landmark.z * width)
                    ))

                # 11,12 => Shoulders, 13,14 => Hips
                shoulder_points = (landmarks[11][:2], landmarks[12][:2])
                hip_points = (landmarks[13][:2], landmarks[14][:2])

                # Calculate angles
                shoulder_angle = self.calculate_horizontal_angle(shoulder_points[0], shoulder_points[1])
                hip_angle = self.calculate_horizontal_angle(hip_points[0], hip_points[1])

                # Subtract frame tilt if available
                if frame_tilt is not None:
                    shoulder_angle -= frame_tilt
                    hip_angle -= frame_tilt

                # Normalize to 0-180, flipping if >90
                shoulder_angle = abs(shoulder_angle) % 180
                if shoulder_angle > 90:
                    shoulder_angle = 180 - shoulder_angle

                hip_angle = abs(hip_angle) % 180
                if hip_angle > 90:
                    hip_angle = 180 - hip_angle

                # If frame_tilt is None, approximate tilt as average of angles
                tilt_angle = frame_tilt if frame_tilt is not None else (shoulder_angle + hip_angle) / 2

                measurements = PostureMeasurements(
                    shoulder_angle=float(shoulder_angle),
                    hip_angle=float(hip_angle),
                    tilt_angle=float(tilt_angle)
                )

                # Draw lines, angles, etc.
                self._draw_enhanced_pose(output_image, landmarks, measurements, frame_tilt)

            return output_image, measurements

        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return frame, None

    def _draw_enhanced_pose(self, image, landmarks, measurements, frame_tilt):
        """
        Draw circles, lines, angle annotations, and reference lines for corrections.
        """
        try:
            for connection in self.custom_connections:
                point1 = landmarks[connection[0]][:2]
                point2 = landmarks[connection[1]][:2]

                # Calculate angle for this connection
                angle = self.calculate_horizontal_angle(point1, point2)
                if frame_tilt is not None:
                    angle -= frame_tilt
                angle = abs(angle) % 180
                if angle > 90:
                    angle = 180 - angle

                # Determine threshold based on connection
                if connection == (11, 12):  # Shoulder
                    threshold = self.thresholds.shoulder_threshold
                elif connection == (13, 14):  # Hip
                    threshold = self.thresholds.hip_threshold
                else:
                    threshold = self.thresholds.tilt_threshold

                # Draw angle text near the midpoint
                mid_x = (point1[0] + point2[0]) // 2
                mid_y = (point1[1] + point2[1]) // 2
                cv2.putText(
                    image,
                    f"{angle:.1f}°",
                    (mid_x - 40, mid_y - 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

                # Color and lines
                if abs(angle) > threshold:
                    cv2.circle(image, point1, 10, self.RED, -1)
                    cv2.circle(image, point2, 10, self.RED, -1)
                    cv2.line(image, point1, point2, self.RED, 2)

                    # Draw reference correction lines if we have a frame tilt angle
                    if frame_tilt is not None:
                        new_x, new_y = self.rotate_2d(point1, point2, point1[0], point1[1], frame_tilt)
                        cv2.circle(image, (int(new_x), int(new_y)), 10, self.PINK, -1)
                        self.draw_dotted_line(image, point1, (int(new_x), int(new_y)), self.PINK, 2)
                else:
                    cv2.circle(image, point1, 10, self.GREEN, -1)
                    cv2.circle(image, point2, 10, self.GREEN, -1)
                    cv2.line(image, point1, point2, self.GREEN, 2)

        except Exception as e:
            logger.error(f"Error drawing enhanced pose: {e}")

    def set_camera_type(self, camera_type):
        """
        Change the camera type at runtime. This will release the existing camera and attempt a new init.
        :param camera_type: 'pc_camera' or 'usb_camera'
        """
        if camera_type != self.camera_type:
            self.camera_type = camera_type
            self.__del__()  # Release current camera
            self.try_init_camera()

    def capture_measurement(self, data):
        """
        Store a measurement when a photo is captured.
        """
        try:
            measurement = PostureMeasurements(
                shoulder_angle=float(data['shoulder_angle']),
                hip_angle=float(data['hip_angle']),
                tilt_angle=float(data['tilt_angle']),
                timestamp=time.time()
            )
            self.get_measurements_history()  # Load existing from file
            self.captured_measurements.insert(0, measurement)  # Insert newest at front
            self.save_measurements()  # Save all
            return {
                'success': True,
                'measurement': {
                    'shoulder_angle': measurement.shoulder_angle,
                    'hip_angle': measurement.hip_angle,
                    'tilt_angle': measurement.tilt_angle,
                    'timestamp': measurement.timestamp
                }
            }
        except Exception as e:
            logger.error(f"Error capturing measurement: {e}")
            return {'success': False, 'error': str(e)}

    def get_measurements_history(self):
        """
        Return all captured measurements (loaded from captured_measurements.json if present).
        """
        try:
            measurements_path = os.path.join(os.path.dirname(__file__), 'captured_measurements.json')
            if os.path.exists(measurements_path):
                with open(measurements_path, 'r') as f:
                    data = json.load(f)
                    self.captured_measurements = []
                    for m in data:
                        try:
                            measurement = PostureMeasurements(
                                shoulder_angle=float(m['shoulder_angle']),
                                hip_angle=float(m['hip_angle']),
                                tilt_angle=float(m['tilt_angle']),
                                timestamp=float(m['timestamp'])
                            )
                            self.captured_measurements.append(measurement)
                        except Exception as e:
                            logger.error(f"Error converting measurement: {e}")

            # Sort newest first by timestamp
            return sorted(self.captured_measurements, key=lambda x: x.timestamp, reverse=True)

        except Exception as e:
            logger.error(f"Error loading measurements history: {e}")
            return self.captured_measurements

    def save_measurements(self):
        """
        Save the in-memory measurements to a JSON file (atomic replace).
        """
        measurements_path = None
        temp_path = None
        try:
            measurements_path = os.path.join(os.path.dirname(__file__), 'captured_measurements.json')
            temp_path = measurements_path + '.tmp'

            data = []
            for m in self.captured_measurements:
                data.append({
                    'shoulder_angle': float(m.shoulder_angle),
                    'hip_angle': float(m.hip_angle),
                    'tilt_angle': float(m.tilt_angle),
                    'timestamp': float(m.timestamp) if m.timestamp else time.time()
                })

            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2)

            os.replace(temp_path, measurements_path)

        except Exception as e:
            logger.error(f"Error saving measurements: {e}")
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    def clear_measurements(self):
        """
        Clear all captured measurements from memory and remove the JSON file.
        """
        try:
            self.captured_measurements = []
            measurements_path = os.path.join(os.path.dirname(__file__), 'captured_measurements.json')
            if os.path.exists(measurements_path):
                os.remove(measurements_path)
            return True
        except Exception as e:
            logger.error(f"Error clearing measurements: {e}")
            return False

