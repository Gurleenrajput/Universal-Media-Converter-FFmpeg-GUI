# Universal Media Converter (FFmpeg GUI)

A cross-platform desktop application built with Python and PySide6 to provide a user-friendly graphical interface for the FFmpeg multimedia framework. This tool simplifies common media tasks like format conversion, video trimming, and audio extraction, all while running conversion jobs in the background to keep the interface responsive.

## ✨ Features

* **Universal Conversion:** Convert audio and video files between popular formats (MP4, MP3, MKV, AVI, etc.).
* **Background Processing:** Utilizes PySide6 threading to prevent the GUI from freezing during long encoding jobs.
* **Real-time Progress:** Displays the status and progress of the FFmpeg job.
* **Advanced Control:** Allows users to set output resolution and codec.
* **Dependency Check:** Verifies FFmpeg installation on launch.

## 🛠️ Requirements

1.  **Python 3.9+**
2.  **FFmpeg:** Must be installed and accessible in your system's PATH.
    * *Note:* The application will check for FFmpeg at runtime.
3.  **Python Packages:** Install via the requirements file:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/Universal-Media-Converter.git
    cd Universal-Media-Converter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

4.  Use the interface to select your input file, choose output settings, and click "Start Conversion."

---

## 🛡️ Copyright Notice

**© 2025 Gurleen Rajput. All Rights Reserved.**  

This software, its documentation, and all associated files are the exclusive intellectual property of **Gurleen Rajput (Owner)**.  
Unauthorized copying, modification, redistribution, or usage of this software, in whole or in part, is strictly prohibited without explicit written permission from the owner.  

**Official Website:** [https://gurleenrajput.online](https://gurleenrajput.online)
