import librosa
import soundfile as sf
import noisereduce as nr
from scipy.signal import butter, filtfilt


def bandpass_filter(data, sr, lowcut=300, highcut=3400):

    nyquist = 0.5 * sr

    low = lowcut / nyquist

    high = highcut / nyquist

    b, a = butter(5, [low, high], btype="band")

    return filtfilt(b, a, data)


def reduce_noise(audio_path):

    audio, sr = librosa.load(audio_path, sr=None)

    # Normalize volume
    audio = audio / max(abs(audio))

    # Keep only ATC voice frequencies
    audio = bandpass_filter(audio, sr)

    # Reduce background noise
    clean_audio = nr.reduce_noise(
        y=audio,
        sr=sr,
        stationary=False,
        prop_decrease=1.0
    )

    output_path = audio_path.replace(".wav", "_clean.wav")

    sf.write(output_path, clean_audio, sr)

    return output_path