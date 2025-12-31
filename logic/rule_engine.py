# logic/rule_engine.py
from logic.timer import FatigueTimer


class RuleEngine:
    def __init__(self, yawn_duration_threshold=6.0):
        self.timer = FatigueTimer(yawn_duration_threshold=yawn_duration_threshold)

    def evaluate(self, mouth_open):
        result = self.timer.update(mouth_open)
        return {
            "trigger_alert": result["trigger_alert"],
            "sustained_yawn": result["sustained_yawn"],
            "yawn_duration": result["yawn_duration"]
        }