import os
import librosa
import noisereduce as nr
import soundfile as sf
from scipy.signal import butter, filtfilt


def bandpass_filter(audio, sample_rate, lowcut=300, highcut=3400, order=5):
    nyquist = 0.5 * sample_rate

    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype="band")

    filtered_audio = filtfilt(b, a, audio)

    return filtered_audio


def reduce_noise(input_file):

    # Load audio
    audio, sample_rate = librosa.load(
        input_file,
        sr=16000,
        mono=True
    )

    # Normalize volume
    audio = librosa.util.normalize(audio)

    # Band-pass filter (ATC Voice Frequency)
    audio = bandpass_filter(audio, sample_rate)

    # Noise Reduction
    cleaned_audio = nr.reduce_noise(
        y=audio,
        sr=sample_rate,
        stationary=False,
        prop_decrease=0.9
    )

    # Output filename
    filename = os.path.splitext(input_file)[0]

    output_file = filename + "_clean.wav"

    # Save cleaned audio
    sf.write(
        output_file,
        cleaned_audio,
        sample_rate
    )

    return output_file