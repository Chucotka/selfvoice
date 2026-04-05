import streamlit as st
import os
import tempfile
from cloner import VoiceCloner
from processor import AudioProcessor

st.set_page_config(page_title="SoulSurfer Voice Clone", layout="wide")

@st.cache_resource
def load_model():
    return VoiceCloner()

cloner = load_model()

st.title("🎙️ Профессиональное Клонирование Голоса")
st.markdown("Загрузите образец (6-10 сек) и введите текст для синтеза.")

# Function to cleanup temporary files
def cleanup_files(*filepaths):
    for fp in filepaths:
        if fp and os.path.exists(fp):
            try:
                os.remove(fp)
            except Exception:
                pass

# Сайдбар с настройками
with st.sidebar:
    st.header("Настройки звука")

    # Выбор языка
    lang_option = st.selectbox(
        "Язык синтеза",
        ("Russian (ru)", "English (en)", "German (de)", "Spanish (es)")
    )
    lang_code = lang_option.split("(")[1].replace(")", "")

    speed = st.slider("Скорость (Tempo)", 0.5, 2.0, 1.0, 0.1)
    pitch = st.slider("Тон (Pitch)", -12, 12, 0, 1)
    volume = st.slider("Усиление (dB)", -20, 20, 0, 1)

    if st.button("Очистить данные сессии"):
        st.session_state.clear()
        st.success("Данные удалены.")

# Основная область
uploaded_file = st.file_uploader("Загрузите файл образца (.wav, .mp3, .flac)", type=["wav", "mp3", "flac"])

if uploaded_file:
    # We do not save to disk immediately to avoid disk space leaks on every Streamlit re-run.
    # Instead, we play from memory.
    st.audio(uploaded_file.getvalue(), format='audio/wav')

    # We write it to a temp file *just* for validation, and delete it immediately.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_val:
        tmp_val.write(uploaded_file.getvalue())
        val_path = tmp_val.name

    valid, msg = AudioProcessor.validate_reference(val_path)
    cleanup_files(val_path)

    if not valid:
        st.error(msg)
    else:
        st.success("Образец готов.")

    text_input = st.text_area("Введите текст на выбранном языке:",
                             placeholder="Привет! Я твой клонированный голос. Как дела?")

    if st.button("Сгенерировать голос"):
        if text_input and valid:
            with st.spinner("Синтезирую (это может занять время)..."):
                # Use secure temporary files
                tmp_ref = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                tmp_preprocessed = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                tmp_raw_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                tmp_final_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

                ref_path = tmp_ref.name
                preprocessed_path = tmp_preprocessed.name
                raw_output = tmp_raw_output.name
                final_output = tmp_final_output.name

                # Close the open file handles so other libraries can open them
                tmp_ref.close()
                tmp_preprocessed.close()
                tmp_raw_output.close()
                tmp_final_output.close()

                try:
                    # Write the uploaded file to disk
                    with open(ref_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    # 0. Preprocess the reference audio
                    AudioProcessor.preprocess_audio(ref_path, preprocessed_path)

                    # 1. Generate Voice using the preprocessed reference
                    cloner.clone_and_generate(text_input, preprocessed_path, raw_output, language=lang_code)

                    # 2. Apply Post-processing
                    AudioProcessor.apply_post_processing(
                        raw_output, final_output,
                        speed=speed, pitch_semitones=pitch, volume_db=volume
                    )

                    # Read final audio into memory so we can delete the file and stream from memory
                    with open(final_output, "rb") as f:
                        final_audio_bytes = f.read()

                    st.success("Генерация завершена!")
                    st.audio(final_audio_bytes, format='audio/wav')
                    st.download_button("Скачать результат", final_audio_bytes, file_name="cloned_voice.wav")

                except Exception as e:
                    st.error(f"Ошибка при генерации: {e}")
                finally:
                    # Privacy First: Always clean up files after generation
                    cleanup_files(ref_path, preprocessed_path, raw_output, final_output)
        else:
            st.warning("Пожалуйста, введите текст и проверьте аудио-образец.")
