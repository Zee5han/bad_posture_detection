# app/overlay.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsBlurEffect


class FatigueOverlay(QWidget):
    def __init__(self, display_seconds=15):
        super().__init__()
        self.display_seconds = display_seconds
        self.setup_ui()
        self.setup_window_flags()
        self.hide()

    def setup_ui(self):
        # Transparent window
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # Full-screen soft white background layer
        self.background = QLabel(self)
        self.background.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);  /* Soft white, ~70% opacity */
            border-radius: 0px;
        """)
        self.background.lower()  # Behind text

        # Apply strong blur to the background layer
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(30)  # Nice soft blur — adjust 20–40 to taste
        self.background.setGraphicsEffect(blur)

        # Centered reminder text — dark for good contrast on light background
        self.label = QLabel("Time for a break! 😴\nStretch, look away,\nand rest your eyes.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 52, QFont.Weight.Bold))
        self.label.setStyleSheet("""
            color: #2c3e50;               /* Deep navy/gray for calm readability */
            background: transparent;
            padding: 60px;
        """)

        # Center the text
        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def setup_window_flags(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

    def show_alert(self):
        # Full screen
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # Make background fill entire window
        self.background.setGeometry(self.rect())

        # Start faded out
        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()

        # Fade in
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1200)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

        # Auto fade out after display time
        QTimer.singleShot(self.display_seconds * 1000, self.fade_out)

    def fade_out(self):
        self.anim.setDuration(2000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()