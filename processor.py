import librosa
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import os

class AudioProcessor:
    @staticmethod
    def preprocess_audio(input_path, output_path):
        """
        Preprocesses audio: silence removal and normalization.
        """
        # Load audio
        y, sr = librosa.load(input_path, sr=None)

        # Remove silence (trim leading and trailing silence)
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)

        # Normalize audio (peak normalization)
        if len(y_trimmed) > 0:
            y_normalized = librosa.util.normalize(y_trimmed)
        else:
            y_normalized = y_trimmed

        # Save processed file
        sf.write(output_path, y_normalized, sr)
        return output_path

    @staticmethod
    def apply_post_processing(input_path, output_path, speed=1.0, pitch_semitones=0, volume_db=0):
        """
        Adjusts speed, pitch, and volume of the generated audio.
        """
        # Load audio
        y, sr = librosa.load(input_path, sr=None)

        # 1. Change Speed (Time Stretching)
        if speed != 1.0:
            y = librosa.effects.time_stretch(y, rate=speed)

        # 2. Change Pitch
        if pitch_semitones != 0:
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_semitones)

        # Save temporary processed file
        sf.write(output_path, y, sr)

        # 3. Change Volume using Pydub
        if volume_db != 0:
            audio = AudioSegment.from_file(output_path)
            audio = audio + volume_db
            audio.export(output_path, format="wav")

    @staticmethod
    def validate_reference(file_path):
        """Checks if the reference audio is suitable (length, etc.)"""
        duration = librosa.get_duration(path=file_path)
        if duration < 3.0:
            return False, "Audio is too short. Need at least 3 seconds."
        if duration > 20.0:
            return True, "Audio is long. Model will use the first 20 seconds."
        return True, "Audio OK."
