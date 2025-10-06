import subprocess

def check_ffmpeg() -> dict:
    """Checks if the FFmpeg executable is available on the system PATH."""
    try:
        # Run a simple check command
        subprocess.run(['ffmpeg', '-version'],
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       timeout=5)
        return {'success': True, 'message': "FFmpeg is running correctly."}

    except FileNotFoundError:
        return {
            'success': False,
            'message': (
                "FFmpeg executable not found on system PATH.\n"
                "Please install FFmpeg and ensure its 'bin' directory "
                "is added to your system's environment variables."
            )
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'message': f"FFmpeg found but failed to run. Error: {e.stderr.decode('utf8')}"
        }
    except Exception as e:
        return {'success': False, 'message': f"An unexpected error occurred during check: {str(e)}"}
