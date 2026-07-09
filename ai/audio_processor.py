from pydub import AudioSegment


def preprocess_audio(input_file):

    audio = AudioSegment.from_file(input_file)

    audio = audio.set_channels(1)

    audio = audio.set_frame_rate(16000)

    output_file = input_file.replace(".", "_processed.")

    audio.export(output_file, format="wav")

    return output_file