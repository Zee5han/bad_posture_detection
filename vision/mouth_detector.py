# vision/mouth_detector.py
import mediapipe as mp
import cv2
import numpy as np


class MouthDetector:
    def __init__(self, distance_threshold=0.025):
        """
        Recommended: Tune between 0.020 and 0.035 based on your face/camera.
        """
        self.distance_threshold = distance_threshold

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def analyze(self, frame, draw=False):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return {
                "mouth_open": False,
                "lip_distance": None
            }

        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        # Points 13 (upper) and 14 (lower) inner lip
        upper = np.array([landmarks[13].x * w, landmarks[13].y * h])
        lower = np.array([landmarks[14].x * w, landmarks[14].y * h])

        # Normalized by frame height (more stable across resolutions/distances)
        lip_distance = np.linalg.norm(upper - lower) / h
        mouth_open = lip_distance > self.distance_threshold

        if draw:
            # Draw FULL face mesh — looks awesome!
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.multi_face_landmarks[0],
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.drawing_spec
            )

            # Optional: highlight lip points and line
            cv2.circle(frame, (int(upper[0]), int(upper[1])), 6, (0, 255, 255), -1)
            cv2.circle(frame, (int(lower[0]), int(lower[1])), 6, (0, 255, 255), -1)
            cv2.line(frame, (int(upper[0]), int(upper[1])), (int(lower[0]), int(lower[1])), (255, 255, 0), 3)

            # Live debug info
            cv2.putText(frame, f"Lip Dist: {lip_distance:.4f}", (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            cv2.putText(frame, f"Thresh: {self.distance_threshold:.4f}", (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        return {
            "mouth_open": mouth_open,
            "lip_distance": round(lip_distance, 4)
        }