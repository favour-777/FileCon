# 🦅 FileCon - The Ultimate File Converter

FileCon is a professional-grade, offline-first file conversion utility designed for speed, privacy, and ease of use. Built with Python and featuring a modern, sleek interface, FileCon allows you to convert images, audio, video, and documents in bulk without ever needing an internet connection.

---

## ✨ Key Features

- **Modern UI/UX**: A clean, intuitive interface built with `CustomTkinter` that supports both **Light** and **Dark** modes.
- **Privacy First**: 100% offline processing. Your files never leave your computer.
- **Drag & Drop**: Effortlessly add files by dragging them directly into the application.
- **Batch Conversion**: Convert hundreds of files simultaneously with real-time progress tracking.
- **Cross-Platform**: Designed to run seamlessly on Windows, macOS, and Linux.

---

## 🛠 Supported Formats

FileCon is designed to be an all-in-one solution for your conversion needs:

| Category | Supported Formats |
| :--- | :--- |
| **Images** | PNG, JPEG, WEBP, ICO, BMP, GIF |
| **Audio** | MP3, WAV, FLAC, OGG, AAC, M4A |
| **Video** | MP4, MKV, MOV, AVI, WEBM (plus Audio Extraction) |
| **Documents** | PDF (from DOCX, TXT, MD) |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for high-performance audio and video processing.
  - *Windows*: `choco install ffmpeg`
  - *macOS*: `brew install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/favour-777/FileCon.git
   cd FileCon
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch FileCon**:
   ```bash
   python main.py
   ```

---

## 🏗 Project Architecture

FileCon follows a modular design for easy extensibility:

- `main.py`: The central hub orchestrating the UI and conversion threads.
- `converters/`: Contains specialized logic for each file type (Image, Audio, Video, Document).
- `ui/`: Custom widgets and theme definitions for a consistent look and feel.
- `assets/`: Directory for branding assets and icons.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new formats or features, feel free to open an issue or submit a pull request.

---

*FileCon - Inspired by speed, built for precision.*
