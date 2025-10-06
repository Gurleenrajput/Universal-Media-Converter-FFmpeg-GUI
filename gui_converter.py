from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QComboBox,
                               QProgressBar, QFileDialog, QMessageBox)
from PySide6.QtCore import QThread
from ffmpeg_worker import FFmpegWorker  # Worker thread class will be imported here

class MediaConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Media Converter")
        self.setGeometry(100, 100, 700, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._init_ui()
        self.worker_thread = None  # Placeholder for the worker thread

    def _init_ui(self):
        # --- 1. Top Input/Output Section ---
        io_layout = QHBoxLayout()

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("Select Input Audio/Video File...")
        self.btn_browse = QPushButton("Browse", self)
        self.btn_browse.clicked.connect(self.select_input_file)

        self.output_format = QComboBox(self)
        self.output_format.addItems(["mp4 (H.264/AAC)", "mp3 (Audio Only)", "webm", "mkv", "avi"])

        io_layout.addWidget(self.file_input)
        io_layout.addWidget(self.btn_browse)
        io_layout.addWidget(QLabel("Output Format:"))
        io_layout.addWidget(self.output_format)
        self.layout.addLayout(io_layout)

        # --- 2. Advanced Settings (Simplified) ---
        settings_layout = QHBoxLayout()
        self.resolution_input = QLineEdit(self)
        self.resolution_input.setPlaceholderText("Resolution (e.g., 1280:720 or leave blank)")
        settings_layout.addWidget(QLabel("Resolution:"))
        settings_layout.addWidget(self.resolution_input)
        self.layout.addLayout(settings_layout)

        # --- 3. Progress Bar and Status ---
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.status_label = QLabel("Ready.")
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)

        # --- 4. Control Buttons ---
        self.btn_convert = QPushButton("Start Conversion", self)
        self.btn_convert.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.btn_convert)

    # --- Methods ---
    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Media File", "",
                                                   "Media Files (*.mp4 *.mkv *.mov *.avi *.mp3 *.wav)")
        if file_name:
            self.file_input.setText(file_name)

    def start_conversion(self):
        input_file = self.file_input.text()
        output_ext = self.output_format.currentText().split(' ')[0]  # e.g., 'mp4'
        resolution = self.resolution_input.text()

        if not input_file:
            QMessageBox.warning(self, "Input Error", "Please select an input file.")
            return

        # Simple file saving dialogue
        suggested = input_file.rsplit('.', 1)[0] + "." + output_ext
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Output File", suggested,
                                                   f"Output Files (*.{output_ext})")
        if not save_path:
            return

        self.btn_convert.setEnabled(False)
        self.status_label.setText("Starting conversion...")
        self.progress_bar.setValue(0)

        # --- Start the Worker Thread ---
        self.worker = FFmpegWorker(input_file, save_path, output_ext, resolution)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.conversion_finished)

        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Processing: {value}% complete...")

    def conversion_finished(self, result):
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.btn_convert.setEnabled(True)

        if result.get('success'):
            self.status_label.setText(f"Success! Output saved to: {result['output_path']}")
            QMessageBox.information(self, "Success", f"Conversion complete:\n{result['output_path']}")
        else:
            self.status_label.setText(f"Error: {result.get('message', 'Unknown error.')}")
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{result.get('message', 'Unknown error.')}")
