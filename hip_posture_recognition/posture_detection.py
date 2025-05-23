import cv2
import mediapipe as mp
import numpy as np
from dataclasses import dataclass

@dataclass
class PostureMeasurements:
    head_tilt: float
    shoulder_tilt: float
    hip_shift: float

class PostureDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            model_complexity=1
        )
        
    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        
        if not results.pose_landmarks:
            return frame, None
            
        height, width = frame.shape[:2]
        landmarks = []
        
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((
                int(landmark.x * width),
                int(landmark.y * height),
                landmark.z * width
            ))
            
        measurements = self._calculate_measurements(landmarks)
        annotated_frame = self._draw_annotations(frame, landmarks, measurements)
        
        return annotated_frame, measurements
        
    def _calculate_measurements(self, landmarks):
        # Calculate head tilt using ear landmarks
        left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value]
        head_tilt = self._calculate_angle(left_ear, right_ear)
        
        # Calculate shoulder tilt
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_tilt = self._calculate_angle(left_shoulder, right_shoulder)
        
        # Calculate hip shift using the hip landmarks
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        hip_shift = self._calculate_lateral_shift(left_hip, right_hip)
        
        return PostureMeasurements(
            head_tilt=head_tilt,
            shoulder_tilt=shoulder_tilt,
            hip_shift=hip_shift
        )
    
    def _calculate_angle(self, point1, point2):
        # Calculate angle relative to horizontal
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        angle = np.degrees(np.arctan2(dy, dx))
        return angle
    
    def _calculate_lateral_shift(self, point1, point2):
        # Calculate lateral deviation from center
        center_x = (point1[0] + point2[0]) / 2
        frame_center_x = 0.5  # Normalized center
        shift = (center_x - frame_center_x) * 100  # Convert to percentage
        return shift
        
    def _draw_annotations(self, frame, landmarks, measurements):
        # Draw landmarks and connections
        connections = [
            (self.mp_pose.PoseLandmark.LEFT_EAR.value, self.mp_pose.PoseLandmark.RIGHT_EAR.value),
            (self.mp_pose.PoseLandmark.LEFT_SHOULDER.value, self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value),
            (self.mp_pose.PoseLandmark.LEFT_HIP.value, self.mp_pose.PoseLandmark.RIGHT_HIP.value)
        ]
        
        for start_idx, end_idx in connections:
            start_point = landmarks[start_idx][:2]
            end_point = landmarks[end_idx][:2]
            
            color = (0, 255, 0)  # Green for good posture
            if abs(measurements.head_tilt) > 10 or abs(measurements.shoulder_tilt) > 10 or abs(measurements.hip_shift) > 15:
                color = (0, 0, 255)  # Red for poor posture
                
            cv2.line(frame, start_point, end_point, color, 2)
            cv2.circle(frame, start_point, 5, color, -1)
            cv2.circle(frame, end_point, 5, color, -1)
            
        return frame
