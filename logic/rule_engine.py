class RuleEngine:
    def __init__(self, time_threshold=10):
        self.time_threshold = time_threshold

    def evaluate(self, posture_bad, mouth_open, violation_time):
        """
        Returns:
            dict: {
                "violation_active": bool,
                "trigger_alert": bool
            }
        """
        violation_active = posture_bad or mouth_open
        trigger_alert = violation_time >= self.time_threshold

        return {
            "violation_active": violation_active,
            "trigger_alert": trigger_alert
        }
