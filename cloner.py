import torch
from TTS.api import TTS
import os

class VoiceCloner:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"-> Loading XTTS-v2 to {self.device}...")
        # Модель скачается автоматически при первом запуске (~2.5 ГБ)
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)

    def clone_and_generate(self, text, speaker_wav, output_path, language="ru"):
        """
        Генерация речи.
        Параметр language должен быть "ru" для русского или "en" для английского.
        """
        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=output_path
        )
        return output_path
