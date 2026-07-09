import whisper

model = whisper.load_model("small")


def transcribe_audio(audio_path):

    result = model.transcribe(
        audio_path,
        word_timestamps=True
    )

    transcript = result["text"]

    segments = result["segments"]

    return transcript, segments