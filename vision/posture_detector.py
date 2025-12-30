import mediapipe as mp
import cv2


class PostureDetector:
    def __init__(self, threshold=0.03):
        self.threshold = threshold

        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def analyze(self, frame, draw=False):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if not results.pose_landmarks:
            return {
                "bad_posture": False,
                "ear_y": None,
                "shoulder_y": None
            }

        lm = results.pose_landmarks.landmark

        left_ear = lm[self.mp_pose.PoseLandmark.LEFT_EAR]
        right_ear = lm[self.mp_pose.PoseLandmark.RIGHT_EAR]
        left_shoulder = lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]

        ear_y = (left_ear.y + right_ear.y) / 2
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2

        bad_posture = ear_y > (shoulder_y + self.threshold)

        if draw:
            self.mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return {
            "bad_posture": bad_posture,
            "ear_y": round(ear_y, 4),
            "shoulder_y": round(shoulder_y, 4)
        }
