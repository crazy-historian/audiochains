import json
import wave
from typing import Union, Optional

import sounddevice as sd
from jsonschema import validate
from chains import ChainOfMethods
from schemas import stream_parameters_schema

input_output_sampwidth = {
    1: ('int8', 'int8'),
    2: ('int16', 'int16'),
    3: ('int24', 'int24'),
    4: ('float32', 'float32')
}


class StreamWithChain(sd.RawStream):
    """
    An overridden sd.RawStream class containing the ChainOfMethods instance and
    related methods.
    """

    def __init__(self, json_file: str = None, sampwidth=2, chain_of_methods: ChainOfMethods = None, *args,
                 **kwargs):
        """
         This class can be initialized by passing the json file name with necessary parameters.

         Example
         ------
            with open("test_config.json", "w") as write_file:
                json.dump(test_config, write_file)

            with StreamWithChain(json_file='test_config.json') as stream:
                while True:
                    stream.write(stream.read(stream.blocksize)[0])

        Parameters
        ----------
        json_file: a json file name containing necessary parameters
        chain_of_methods: an instance of the ChainOfMethods class
        *args, **kwargs: parameters for base sd.RawStream class
        """

        if json_file:
            super().__init__(*args, **self.from_json(json_file), **kwargs)
        else:
            super().__init__(*args, dtype=input_output_sampwidth[sampwidth], **kwargs)
        self.chain_of_methods = chain_of_methods

    @staticmethod
    def from_json(json_file: str):
        """
        Loads json_file and changes the legacy code style keys to SoundDevice style
        """
        with open(json_file, 'r') as json_file:
            stream_config = json.load(json_file)
            validate(instance=stream_config, schema=stream_parameters_schema)
            stream_config['samplerate'] = stream_config.pop('framerate')
            stream_config['blocksize'] = stream_config.pop('chunk_size')
            stream_config['device'] = stream_config.pop('device_id')
            stream_config['dtype'] = input_output_sampwidth[stream_config['sampwidth']]
            stream_config.pop('sampwidth')

            return stream_config

    def set_chain(self, chain_of_methods: ChainOfMethods):
        """
        Passing an existing instance of ChainOfMethods class
        """
        self.chain_of_methods = chain_of_methods

    def set_methods(self, *args):
        """
        Initializing the ChainOfMethods attributes by passing
        the list of BlockAudioMethod instances

        """
        self.chain_of_methods = ChainOfMethods(*args)

    def get_iterations(self, seconds: int) -> Union[int, float]:
        """
        Return the amount of iteration which is mapped to passed amount of second
        :param seconds:
        :return:
        """
        if seconds:
            return int((self.samplerate / self.blocksize) * seconds)
        else:
            return float('inf')

    def read(self, frames):
        """
        Overridden base class method where cffi buffer object
        is unpacked to bytes
        """
        return memoryview(sd.RawStream.read(self, frames=frames)[0]).tobytes()

    def apply(self):
        """
        Calling the ChainOfMethods attributes which processes the raw audio data
        :return:
        """
        in_data = self.read(self.blocksize)
        return self.chain_of_methods(in_data)


class StreamFromFile:
    """
    Realization of playback WAV file by block(chunk) of frames for the sake of testing
    """

    def __init__(self,
                 filename: str,
                 blocksize: int = 1024,
                 chain_of_methods: Optional[ChainOfMethods] = None):
        self.chain_of_methods = chain_of_methods
        self.blocksize = blocksize
        self.filename = filename
        self.iterations = None
        self.wav_file = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return True

    def open(self) -> None:
        self.wav_file = wave.open(self.filename, 'rb')

    def close(self) -> None:
        self.wav_file.close()

    def read(self, frames):
        return self.wav_file.readframes(frames)

    def apply(self):
        return self.chain_of_methods(in_data=self.read(self.blocksize))

    def get_iterations(self) -> int:
        frames = self.wav_file.getnframes()
        iterations = frames // self.blocksize
        if frames % self.blocksize != 0:
            iterations += 1
        return iterations


if __name__ == "__main__":
    with StreamWithChain(json_file=r'E:\runtime_audio_processing\test\test_config.json', sampwidth=2) as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)
