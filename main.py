import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from gui_converter import MediaConverterGUI
from utils import check_ffmpeg

def main():
    # 1. Check for FFmpeg dependency before launching the GUI
    ffmpeg_status = check_ffmpeg()
    if not ffmpeg_status['success']:
        # Show a critical error message if FFmpeg is missing
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("CRITICAL DEPENDENCY MISSING")
        msg.setInformativeText(ffmpeg_status['message'])
        msg.setWindowTitle("FFmpeg Error")
        msg.exec()
        sys.exit(1)

    # 2. Launch the PySide6 application
    app = QApplication(sys.argv)
    window = MediaConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
