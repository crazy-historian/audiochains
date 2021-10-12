from source import AudioSource


class AudioStream:
    def __init__(self, source: AudioSource):
        self.source = source

    def open(self):
        self.source.open()

    def read(self):
        return self.source.read()

    def close(self):
        self.source.close()

    def get_iterations(self, seconds: int):
        return self.source.get_iterations(seconds)

    def __enter__(self):
        self.source.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.source.close()
        return True
