import mediapipe as mp


class PostureDetector:
    def __init__(self, threshold=0.03):
        """
        threshold: normalized Y-axis distance in MediaPipe space
        """
        self.threshold = threshold

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def analyze(self, frame):
        """
        Analyze posture from a frame.
        Returns:
            dict: {
                "bad_posture": bool,
                "ear_y": float,
                "shoulder_y": float
            }
        """
        rgb = frame[:, :, ::-1]
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

        return {
            "bad_posture": bad_posture,
            "ear_y": round(ear_y, 4),
            "shoulder_y": round(shoulder_y, 4)
        }
