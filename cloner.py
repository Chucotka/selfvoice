import torch
from TTS.api import TTS
import os
import platform

class VoiceCloner:
    def __init__(self):
        # Логика выбора устройства специально для Mac M1/M2/M3
        if torch.backends.mps.is_available():
            self.device = "mps"
            print("-> Использую Apple Metal Performance Shaders (MPS)")
        elif torch.cuda.is_available():
            self.device = "cuda"
            print("-> Использую NVIDIA CUDA")
        else:
            self.device = "cpu"
            print("-> Внимание: GPU не найден, использую CPU (будет медленно)")

        # Загрузка модели
        # Для M1 Max лучше использовать XTTS-v2, она хорошо оптимизирована
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
