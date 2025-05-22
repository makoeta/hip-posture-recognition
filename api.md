# Scoliosis Analysis API Documentation

## License

```
Copyright 2024 HHN University & UniTyLab

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Overview

The Scoliosis Analysis API provides real-time posture analysis using computer vision and machine learning techniques. It captures and analyzes body posture through video feed, calculating key angles that are crucial for scoliosis assessment.

## Key Features

- Real-time posture detection and analysis
- Multi-camera support (PC, USB, Raspberry Pi)
- Angle measurements (shoulder, hip, frame tilt)
- Historical data tracking
- PDF report generation
- Real-time data visualization
- Configurable measurement thresholds

## REST Endpoints

### Main Interface

#### GET /
- **Description**: Main dashboard interface
- **Response**: HTML dashboard view
- **Features**: 
  - Live video feed
  - Real-time angle measurements
  - Capture controls
  - Settings management
- **Example**: `GET http://localhost:5000/`

### Video Processing

#### GET /video_feed
- **Description**: Real-time video feed with pose detection
- **Response**: MJPEG stream
- **Features**:
  - Pose landmark detection
  - Angle visualization
  - Reference lines
  - Color-coded indicators
- **Example**: `GET http://localhost:5000/video_feed`

### Measurement Management

#### POST /capture_measurement
- **Description**: Save a captured measurement
- **Request Body**:
```json
{
    "shoulder_angle": 32.5,
    "hip_angle": 28.7,
    "tilt_angle": -15.3
}
```
- **Response**: Success status with measurement details
```json
{
    "success": true,
    "measurement": {
        "shoulder_angle": 32.5,
        "hip_angle": 28.7,
        "tilt_angle": -15.3,
        "timestamp": 1705912345.678
    }
}
```

#### GET /history
- **Description**: View measurement history with analytics
- **Response**: HTML view with:
  - Measurement timeline
  - Trend analysis
  - Statistical overview
  - Filterable data table
- **Example**: `GET http://localhost:5000/history`

### Threshold Management

#### GET /get_thresholds
- **Description**: Retrieve current posture thresholds
- **Response**: Current threshold values
```json
{
    "shoulder_threshold": 5.0,
    "hip_threshold": 5.0,
    "tilt_threshold": 2.0
}
```

#### POST /update_thresholds
- **Description**: Update posture analysis thresholds
- **Request Body**:
```json
{
    "shoulder_threshold": 5.0,
    "hip_threshold": 5.0,
    "tilt_threshold": 2.0
}
```
- **Response**: Updated threshold values
- **Example**: 
```bash
curl -X POST http://localhost:5000/update_thresholds 
-H "Content-Type: application/json" 
-d '{"shoulder_threshold": 5.0, "hip_threshold": 5.0, "tilt_threshold": 2.0}'
```

### Data Management

#### POST /clear_history
- **Description**: Clear measurement history
- **Response**: Success status
```json
{
    "status": "success"
}
```

#### GET /generate_report
- **Description**: Generate PDF report of measurements
- **Response**: PDF file download
- **Features**:
  - Latest measurements
  - Historical data
  - Trend analysis
  - Professional formatting with logos

## WebSocket Events

### Client → Server

#### connect
- **Description**: Client establishes WebSocket connection
- **Purpose**: Enable real-time data streaming
- **No payload required**

#### disconnect
- **Description**: Client terminates WebSocket connection
- **Purpose**: Clean up resources
- **No payload required**

### Server → Client

#### measurements
- **Description**: Real-time measurement updates
- **Frequency**: Every processed frame
- **Payload**:
```json
{
    "shoulder_angle": 5.2,
    "hip_angle": 3.1,
    "tilt_angle": 1.5
}
```

## Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid input)
- **500**: Internal Server Error

### Error Response Format
```json
{
    "error": "Detailed error description"
}
```

## Performance Specifications

### Rate Limits
- **Video Processing**: 30 FPS
- **Measurement Updates**: Every other frame
- **History Storage**: Last 100 records
- **WebSocket Ping**: Every 5 seconds
- **Connection Timeout**: 10 seconds

### Technical Requirements
- **Python**: 3.8+
- **Memory**: 2GB minimum
- **CPU**: Multi-core recommended
- **Camera**: 640x480 minimum resolution

## Dependencies

### Core Components
- **Flask**: Web framework
- **SocketIO**: Real-time communication
- **OpenCV**: Computer vision processing
- **Mediapipe**: Pose detection
- **NumPy**: Numerical computations
- **ReportLab**: PDF generation

### Additional Libraries
- **Plotly**: Data visualization
- **Pandas**: Data manipulation
- **JSON**: Data serialization

## Development Setup

1. **Environment Setup**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Installation**:
```bash
pip install -r requirements.txt
```

3. **Configuration**:
- Set environment variables (optional)
- Configure camera settings
- Adjust thresholds if needed

4. **Run Application**:
```bash
python app.py
```

5. **Access Interface**:
- Open browser: http://localhost:5000
- Test video feed
- Verify WebSocket connection

## Security Considerations

- CORS enabled for development
- Rate limiting on API endpoints
- Input validation for all data
- Secure file operations
- Error logging and monitoring
