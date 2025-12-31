#  Fatigue Detector 😴

A cross-platform desktop app that gently reminds you to take breaks when you're tired, using only your webcam and local processing.

Detects **sustained yawning** as a reliable fatigue signal and shows a beautiful full-screen reminder to stretch and rest your eyes.

**100% local • No data leaves your device • No cloud • Full privacy**

### Features
- Real-time face mesh visualization
- Sustained yawn detection (≥6 seconds mouth open)
- Full-screen soft blurred reminder overlay
- Non-intrusive, calming design
- Built with Python, OpenCV, MediaPipe, and PyQt6

### How It Works
1. Uses MediaPipe Face Mesh to track lip distance
2. Triggers only on prolonged mouth opening (real yawn, not talking)
3. Shows gentle full-screen light overlay with break reminder
4. Auto-dismisses after 15 seconds

### Installation & Run
```bash
git clone https://github.com/Zee5han/bad_posture_detection.git
cd posture_detection
pip install -r requirements.txt
python app/main.py