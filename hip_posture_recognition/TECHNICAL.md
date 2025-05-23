# Scoliosis Analysis Technical Documentation

## Overview

This document provides detailed technical information about the Scoliosis Analysis project, including mathematical foundations, algorithms, and implementation details.

## Pose Detection System

### MediaPipe Integration

The system utilizes MediaPipe's pose detection model, which provides 33 body landmarks in 3D space. Key landmarks used for scoliosis analysis include:

- Shoulders (landmarks 11, 12)
- Hips (landmarks 13, 14)
- Spine midline (derived from multiple points)

### Coordinate System

- **Origin**: Top-left corner of the frame
- **X-axis**: Horizontal (right positive)
- **Y-axis**: Vertical (down positive)
- **Z-axis**: Depth (away from camera positive)

## Angle Calculations

### Frame Tilt Detection

```python
def calculate_frame_tilt(frame):
    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Hough transform for line detection
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    
    # Calculate median angle of detected lines
    angles = [theta - np.pi/2 * (180/np.pi) for rho, theta in lines[0]]
    return np.median(angles)
```

### Horizontal Angle Calculation

The angle between two points relative to the horizontal:

```python
def calculate_horizontal_angle(point1, point2):
    deltaY = point1[1] - point2[1]  # Y-coordinate difference
    deltaX = point1[0] - point2[0]  # X-coordinate difference
    angle = math.atan2(deltaY, deltaX) * (180.0/math.pi)
    return (angle + 360) % 360 - 180
```

### Angle Normalization

Angles are normalized to ensure consistent measurements:

1. Convert to absolute value: `angle = abs(angle)`
2. Apply modulo 180: `angle = angle % 180`
3. Convert to acute angle if needed: `angle = 180 - angle if angle > 90 else angle`

## Real-time Processing Pipeline

1. **Frame Acquisition**
   - Capture frame from camera
   - Convert to RGB color space
   - Apply frame tilt correction if needed

2. **Pose Detection**
   - Process frame through MediaPipe pose detector
   - Extract landmark coordinates
   - Convert to pixel coordinates

3. **Angle Measurements**
   ```python
   # Calculate shoulder angle
   shoulder_points = (landmarks[11][:2], landmarks[12][:2])
   shoulder_angle = calculate_horizontal_angle(*shoulder_points)
   
   # Calculate hip angle
   hip_points = (landmarks[13][:2], landmarks[14][:2])
   hip_angle = calculate_horizontal_angle(*hip_points)
   
   # Adjust for frame tilt
   if frame_tilt is not None:
       shoulder_angle -= frame_tilt
       hip_angle -= frame_tilt
   ```

4. **Visualization Enhancement**
   - Draw pose landmarks
   - Add angle measurements
   - Show reference lines
   - Color-code based on thresholds

## Data Processing and Storage

### Measurement Data Structure

```python
@dataclass
class PostureMeasurements:
    shoulder_angle: float
    hip_angle: float
    tilt_angle: float
    timestamp: float = None
```

### Storage Format (JSON)

```json
{
    "shoulder_angle": 32.5,
    "hip_angle": 28.7,
    "tilt_angle": -15.3,
    "timestamp": 1705912345.678
}
```

## Visualization Techniques

### Real-time Gauge Display

1. **Angle Mapping**
   - Input: Raw angle (-180° to 180°)
   - Output: Normalized value (0 to 100)
   ```python
   normalized = (angle + 180) / 360 * 100
   ```

2. **Color Coding**
   - Good: ≤ threshold (green)
   - Warning: ≤ threshold * 2 (yellow)
   - Critical: > threshold * 2 (red)

### Reference Line System

1. **Horizontal Reference**
   - Drawn as dotted lines
   - Shows ideal alignment
   - Updates with frame tilt

2. **Correction Indicators**
   - Direction arrows
   - Distance to ideal position
   - Color-coded feedback

## Performance Optimization

### Camera Handling

1. **Resolution Management**
   ```python
   camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   camera.set(cv2.CAP_PROP_FPS, 30)
   camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
   ```

2. **Frame Processing**
   - Skip frames if processing lags
   - Maintain consistent FPS
   - Buffer management

### Memory Management

1. **Measurement History**
   - Limited to 100 records
   - Oldest records removed first
   - Atomic file operations

2. **Image Processing**
   - Efficient numpy operations
   - Minimize copy operations
   - Release resources properly

## Error Handling and Validation

### Measurement Validation

```python
def validate_measurement(data):
    required_fields = ['shoulder_angle', 'hip_angle', 'tilt_angle']
    if not all(key in data for key in required_fields):
        raise ValueError("Missing required measurement data")
    
    for key in required_fields:
        try:
            float(data[key])
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for {key}")
```

### Error Recovery

1. **Camera Failures**
   - Automatic reconnection
   - Fallback to test mode
   - Error logging

2. **Data Corruption**
   - Atomic file operations
   - Backup measurements
   - Data validation

## Future Enhancements

1. **Machine Learning Integration**

   - Prediction models
   - Transformer models 

2. **Advanced Analytics**
   - Trend analysis
   - Correlation detection
   - Progress tracking

3. **Hardware Optimization**
   - Multi-camera support
   - Depth sensing
   - Mobile integration 