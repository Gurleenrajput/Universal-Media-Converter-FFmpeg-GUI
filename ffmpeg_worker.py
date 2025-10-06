import ffmpeg
from PySide6.QtCore import QObject, Signal
import time

class FFmpegWorker(QObject):
    # Signals for communicating back to the main GUI thread
    progress_signal = Signal(int)
    finished_signal = Signal(dict)

    def __init__(self, input_path, output_path, output_ext, resolution):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.output_ext = output_ext
        self.resolution = resolution
        self._is_running = True

    def run(self):
        """Builds and executes the FFmpeg command."""
        try:
            # --- 1. Build the FFmpeg command ---
            stream = ffmpeg.input(self.input_path)

            # Add resolution filter if specified
            if self.resolution and ':' in self.resolution:
                w, h = self.resolution.split(':')
                stream = stream.filter('scale', w, h)

            # Define output options based on selected format
            output_options = {}
            if self.output_ext == 'mp3':
                output_options.update(acodec='libmp3lame', vn=None)  # vn=None drops video stream
            elif self.output_ext == 'mp4':
                output_options.update(vcodec='libx264', acodec='aac')

            # --- 2. Execute the command (simplified without real-time parsing) ---
            # NOTE: For true real-time progress, you would use subprocess.Popen and parse stderr.
            # Here, we simulate progress for UX demonstration, then "pretend" success.

            for i in range(1, 101):
                time.sleep(0.02)
                self.progress_signal.emit(i)
                if not self._is_running:
                    self.finished_signal.emit({'success': False, 'message': 'Job canceled.'})
                    return

            # In a real app, replace the loop above with:
            # ffmpeg.run(stream.output(self.output_path, **output_options), overwrite_output=True)

            self.finished_signal.emit({
                'success': True,
                'output_path': self.output_path
            })

        except ffmpeg.Error as e:
            error_message = e.stderr.decode('utf8') if getattr(e, 'stderr', None) else "Unknown FFmpeg error."
            self.finished_signal.emit({
                'success': False,
                'message': f"FFmpeg Error: {error_message}"
            })
        except Exception as e:
            self.finished_signal.emit({
                'success': False,
                'message': f"A Python error occurred: {str(e)}"
            })
