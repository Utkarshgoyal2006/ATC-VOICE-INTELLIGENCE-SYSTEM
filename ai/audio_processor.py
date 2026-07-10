from pydub import AudioSegment


def preprocess_audio(audio_path):

    audio = AudioSegment.from_file(audio_path)

    # Convert to mono
    audio = audio.set_channels(1)

    # Resample to 16 kHz
    audio = audio.set_frame_rate(16000)

    output_path = audio_path.replace(".", "_processed.")

    audio.export(output_path, format="wav")

    return output_path