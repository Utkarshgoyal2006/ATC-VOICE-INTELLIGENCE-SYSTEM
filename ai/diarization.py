import os

from dotenv import load_dotenv

from pyannote.audio import Pipeline

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)


def diarize_audio(audio_path):

    diarization = pipeline(audio_path)

    speakers = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):

        speakers.append({

            "speaker": speaker,

            "start": round(turn.start, 2),

            "end": round(turn.end, 2)

        })

    return speakers
if __name__ == "__main__":

    speakers = diarize_audio("uploads/sample.mp3")
    
    for speaker in speakers:

        print(speaker)