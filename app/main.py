# main.py
import cv2
import sys
from PyQt6.QtWidgets import QApplication

from vision.camera import Camera
from vision.posture_detector import PostureDetector
from vision.mouth_detector import MouthDetector
from logic.rule_engine import RuleEngine
from app.overlay import FatigueOverlay


def main():
    app = QApplication(sys.argv)
    overlay = FatigueOverlay(display_seconds=15)

    camera = Camera(camera_index=0)
    posture_detector = PostureDetector(threshold=0.03)
    mouth_detector = MouthDetector(distance_threshold=0.025)  # Tune this!

    rules = RuleEngine(yawn_duration_threshold=6.0)

    camera.start()
    print("[INFO] Fatigue Detector Running")
    print("→ Sustained yawn (≥6s) triggers full-screen gentle reminder")
    print("Press ESC to quit")

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            posture = posture_detector.analyze(frame, draw=True)
            mouth = mouth_detector.analyze(frame, draw=True)

            decision = rules.evaluate(mouth_open=mouth["mouth_open"])

            # Debug info
            cv2.putText(frame, f"Posture: {'BAD' if posture['bad_posture'] else 'GOOD'}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255) if posture['bad_posture'] else (0, 255, 0), 2)

            cv2.putText(frame, f"Yawn Duration: {decision['yawn_duration']:.1f}s",
                        (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            if decision["sustained_yawn"]:
                cv2.putText(frame, "SUSTAINED YAWN DETECTED!", (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

            if decision["trigger_alert"]:
                overlay.show_alert()

            cv2.imshow("Debug View (Full Face Mesh)", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

            app.processEvents()

    finally:l
