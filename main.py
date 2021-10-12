"""
This file is dedicated for launching and testing audio processing functions.
"""
from containers import file_main
from stream import AudioStream
from source import AudioFromMicrophone
from callbacks.writers import WriterInWAV
from exceptions.handlers import exception_handler


@exception_handler
def audio_test():
    with AudioStream(source=AudioFromMicrophone()) as stream, WriterInWAV(
            file_name='test.wav',
            framerate=44800,
            channels=1,
            sampwidth=2,
    ) as write:
        for i in range(stream.get_iterations(seconds=2)):
            write(in_data=stream.read())


if __name__ == "__main__":
    file_main()
