# Scoliosis Analysis System - User Guide

## Introduction

The Scoliosis Analysis System is a sophisticated tool designed for real-time posture analysis and scoliosis assessment. This guide will walk you through the setup, usage, and features of the system.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the System](#using-the-system)
5. [Understanding Measurements](#understanding-measurements)
6. [Reports and History](#reports-and-history)
7. [Troubleshooting](#troubleshooting)

## System Requirements

### Hardware
- Computer with webcam or USB camera
- Minimum 2GB RAM
- Multi-core processor recommended
- Stable internet connection
- Good lighting conditions

### Software
- Windows 10/11, macOS, or Linux
- Python 3.8 or higher
- Web browser (Chrome/Firefox recommended)
- USB drivers (for external cameras)

## Installation

1. **Clone the Repository**
   ```bash
   git clone 
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Application**
   ```bash
   python app.py
   ```

5. **Access the Interface**
   - Open your web browser
   - Navigate to: http://localhost:5000

## Getting Started

### Initial Setup

1. **Camera Selection**
   - Choose your camera type from the dropdown
   - Options: PC Camera, USB Camera
   - System will automatically detect available cameras

2. **Calibration**
   - Ensure good lighting
   - Stand 2-3 meters from camera
   - Face the camera directly

3. **Threshold Settings**
   - Click "Settings" button
   - Adjust thresholds as needed:
     - Shoulder Angle: 5° default
     - Hip Angle: 5° default
     - Frame Tilt: 2° default

## Using the System

### Taking Measurements

1. **Preparation**
   - Stand in the marked area
   - Keep arms relaxed at sides
   - Face forward
   - Maintain natural posture

2. **Capture Process**
   - Click "Take Photo" button
   - Wait for 5-second countdown
   - Stay still during capture
   - Review captured measurements

3. **Saving Measurements**
   - Review displayed angles
   - Click "Save Measurement" to store
   - Or "Try Again" for another capture

### Real-time Feedback

- **Color Indicators**
  - Green: Within threshold
  - Yellow: Warning level
  - Red: Above threshold

- **Reference Lines**
  - Dotted lines show ideal alignment
  - Arrows indicate correction direction
  - Distance shows deviation amount

## Understanding Measurements

### Angle Types

1. **Shoulder Angle**
   - Measures shoulder line deviation from horizontal
   - Ideal range: ±5 degrees
   - Indicates upper body alignment

2. **Hip Angle**
   - Measures hip line deviation from horizontal
   - Ideal range: ±5 degrees
   - Indicates pelvic alignment

3. **Frame Tilt**
   - Measures overall posture frame tilt
   - Ideal range: ±2 degrees
   - Compensates for camera alignment

### Interpretation

- **Good Posture**
  - All angles within thresholds
  - Symmetric body alignment
  - Balanced shoulder and hip lines

- **Needs Attention**
  - One or more angles exceed thresholds
  - Asymmetric alignment
  - Consistent deviation patterns

## Reports and History

### Viewing History

1. **Access History**
   - Click "View History" button
   - See all saved measurements
   - Filter by date/time
   - Sort by any column

2. **Analytics**
   - Trend graphs
   - Progress tracking
   - Statistical analysis
   - Pattern identification

### Generating Reports

1. **Report Creation**
   - Click "Download Report"
   - PDF generated automatically
   - Includes:
     - Latest measurements
     - Historical data
     - Trend analysis
     - Professional formatting

2. **Report Sharing**
   - Download PDF file
   - Print or email
   - Share with healthcare providers

## Troubleshooting

### Common Issues

1. **Camera Not Detected**
   - Check USB connections
   - Verify camera permissions
   - Try different USB ports
   - Restart application

2. **Poor Detection**
   - Improve lighting
   - Adjust distance from camera
   - Wear contrasting clothing
   - Check for obstructions

3. **Connection Issues**
   - Check internet connection
   - Clear browser cache
   - Refresh page
   - Restart application

### Getting Help

- Check error messages
- Consult technical documentation
- Report bugs through GitHub/gitlab

## Best Practices

1. **Regular Use**
   - Take measurements consistently
   - Same time of day
   - Similar clothing
   - Consistent position

2. **Data Management**
   - Save important measurements
   - Generate regular reports
   - Track progress over time
   - Share data with professionals

3. **System Maintenance**
   - Clean camera lens
   - Maintain good lighting
   - Regular calibration checks

## Safety Notes

- Follow proper posture during measurement
- Don't make sudden movements
- Take breaks between sessions
- Consult healthcare providers for medical advice

## Support

For  upport or questions:
- Please Make PR 
- Documentation: /docs
- GitHub/gitlab Issues: 