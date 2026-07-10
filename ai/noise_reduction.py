import os
import librosa
import soundfile as sf
import noisereduce as nr


def reduce_noise(audio_path):

    signal, sr = librosa.load(audio_path, sr=None)

    reduced = nr.reduce_noise(

        y=signal,

        sr=sr,

        stationary=False,

        prop_decrease=0.9

    )

    output_path = audio_path.replace(".wav", "_clean.wav")

    sf.write(

        output_path,

        reduced,

        sr

    )

    return output_path