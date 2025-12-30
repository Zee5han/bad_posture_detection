import cv2
import threading
import time


class Camera:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height

        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.running = False
        self.frame = None
        self.lock = threading.Lock()

    def start(self):
        """Start camera capture in background thread"""
        if self.running:
            return

        self.running = True
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        """Continuously grab frames"""
        while self.running:
            success, frame = self.cap.read()
            if success:
                with self.lock:
                    self.frame = frame
            time.sleep(0.01)  # reduce CPU usage

    def get_frame(self):
        """Return latest frame"""
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        """Stop camera safely"""
        self.running = False
        time.sleep(0.1)
        if self.cap.isOpened():
            self.cap.release()
