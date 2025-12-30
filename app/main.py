import cv2
import time

from vision.camera import Camera
from vision.posture_detector import PostureDetector
from vision.mouth_detector import MouthDetector
from logic.timer import ViolationTimer
from logic.rule_engine import RuleEngine


def main():
    camera = Camera(camera_index=0)
    posture_detector = PostureDetector()
    mouth_detector = MouthDetector()

    timer = ViolationTimer()
    rules = RuleEngine(time_threshold=10)

    camera.start()
    print("[INFO] Running Phase-1 Visual Test")

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            posture = posture_detector.analyze(frame, draw=True)
            mouth = mouth_detector.analyze(frame, draw=True)

            posture_bad = posture["bad_posture"]
            mouth_open = mouth["mouth_open"]

            violation_active = posture_bad or mouth_open
            violation_time = timer.update(violation_active)

            decision = rules.evaluate(
                posture_bad,
                mouth_open,
                violation_time
            )

            # ---- UI TEXT ----
            cv2.putText(frame, f"Posture: {'BAD' if posture_bad else 'GOOD'}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255) if posture_bad else (0, 255, 0), 2)

            cv2.putText(frame, f"Mouth: {'OPEN' if mouth_open else 'CLOSED'}",
                        (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255) if mouth_open else (0, 255, 0), 2)

            cv2.putText(frame, f"Timer: {violation_time:.1f}s",
                        (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 0), 2)

            if decision["trigger_alert"]:
                cv2.putText(frame, "⚠ BAD POSTURE ALERT ⚠",
                            (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3)

            cv2.imshow("Posture - Phase 1 Debug", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
