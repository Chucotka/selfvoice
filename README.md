# Voice Cloning App (XTTS-v2)

### Prerequisites
- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM (Recommended for CUDA)
- FFmpeg installed on your system

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   The first time you run the app, it will download ~2GB of model weights from HuggingFace automatically.

### Running the App
```bash
streamlit run app.py
```

### Best Results for Cloning

- Length: 6 to 12 seconds of clear speech.
- Quality: No background music or noise.
- Emotion: The model will clone the tone of the sample. If the sample is whispery, the output will be whispery.


### Key Technical Features:
* **Zero-Shot Cloning:** No training required. It uses the latent space of the speaker to map the new text immediately.
* **CUDA Support:** Automatically detects your GPU to ensure generation takes 2-3 seconds rather than minutes.
* **Privacy:** It uses `tempfile` for the reference audio and local storage for the output, ensuring no data leaves your machine.
