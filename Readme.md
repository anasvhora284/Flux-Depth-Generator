# DepthAnything V2 – Local Batch 3D Generator

A modern, local web app to batch-generate **depth maps** and **3D photos** from your images using [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2).

![UI Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white) ![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

## ✨ Features

- **Batch Processing**: Upload hundreds of JPG/PNG images at once.
- **Dual Output**:
  - `_depth.png`: High-quality normalized depth map.
  - `_3d.jpg`: JPEG with embedded **Google GDepth XMP** metadata (compatible with Android Photos, Quest, and 3D viewers).
- **Privacy First**: Runs 100% offline on your CPU/GPU.
- **Live Monitoring**: Real-time CPU and RAM usage tracking.
- **Modern UI**: Clean, dark-themed interface powered by Streamlit.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the repository
```
git clone https://github.com/YOUR_USERNAME/depthanything-v2-3d-batch.git
cd depthanything-v2-3d-batch
```

### 2. Setup Environment
Run the included setup script for your OS:

**Linux / macOS:**
```
chmod +x setup.sh
./setup.sh
```

**Windows:**
Double-click `setup_windows.bat`.

*This will create a virtual environment, install dependencies, and launch the app.*

## 📦 Manual Setup

If you prefer to set it up manually:

1. **Create venv**: `python -m venv .venv`
2. **Activate**: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
3. **Install deps**: `pip install -r requirements.txt`
4. **Run**: `streamlit run app.py`

## 🛠 Tech Stack & Credits

This tool wraps several amazing open-source projects:

- **Core Model**: [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) (Apache 2.0)
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **Image Processing**: [Pillow](https://python-pillow.org/) & [NumPy](https://numpy.org/)
- **System Stats**: [psutil](https://psutil.readthedocs.io/)

## 📄 License

This project is licensed under the **Apache License 2.0**. See `LICENSE` for details.

---
*Made with ❤️ for the open source community.*
