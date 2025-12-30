import mediapipe as mp
import cv2


class MouthDetector:
    def __init__(self, threshold=0.015):
        self.threshold = threshold

        self.mp_face = mp.solutions.face_mesh
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

        self.face_mesh = self.mp_face.FaceMesh(
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
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]

        lip_distance = abs(upper_lip.y - lower_lip.y)
        mouth_open = lip_distance > self.threshold

        if draw:
            self.mp_draw.draw_landmarks(
                frame,
                results.multi_face_landmarks[0],
                self.mp_face.FACEMESH_TESSELATION,
                self.draw_spec,
                self.draw_spec
            )

        return {
            "mouth_open": mouth_open,
            "lip_distance": round(lip_distance, 4)
        }
