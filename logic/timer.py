# logic/timer.py
import time


class FatigueTimer:
    def __init__(self, yawn_duration_threshold=6.0):
        self.yawn_duration_threshold = yawn_duration_threshold
        self.yawn_start_time = None

    def update(self, mouth_open):
        current_time = time.time()

        if mouth_open:
            if self.yawn_start_time is None:
                self.yawn_start_time = current_time
            yawn_duration = current_time - self.yawn_start_time
        else:
            self.yawn_start_time = None
            yawn_duration = 0.0

        sustained_yawn = yawn_duration >= self.yawn_duration_threshold
        trigger_alert = sustained_yawn  # Alert every time condition is met

        return {
            "sustained_yawn": sustained_yawn,
            "yawn_duration": round(yawn_duration, 1),
            "trigger_alert": trigger_alert
        }