import wave


from callbacks.main import CallbackWriter


class WriterInWAV(CallbackWriter):
    """
    This class implement writing bytes-type data in WAV file
    """

    def __init__(self,
                 file_name: str,
                 framerate: int,
                 sampwidth: int,
                 channels: int):
        self.file_name = file_name
        self.framerate = framerate
        self.sampwidth = sampwidth
        self.file_name = file_name
        self.channels = channels
        self.open()

    def open(self) -> None:
        self.wav_file = wave.open(self.file_name, 'wb')
        self.wav_file.setnchannels(self.channels)
        self.wav_file.setsampwidth(self.sampwidth)
        self.wav_file.setframerate(self.framerate)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.wav_file:
            self.wav_file.close()
        return True

    def __call__(self, in_data) -> None:
        self.wav_file.writeframesraw(in_data)
