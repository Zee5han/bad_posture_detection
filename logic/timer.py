import time


class ViolationTimer:
    def __init__(self):
        self.start_time = None

    def update(self, violation_active):
        """
        Returns elapsed violation time in seconds
        """
        if violation_active:
            if self.start_time is None:
                self.start_time = time.time()
            return time.time() - self.start_time
        else:
            self.reset()
            return 0.0

    def reset(self):
        self.start_time = None
