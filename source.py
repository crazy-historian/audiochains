import wave
import pyaudio
import app_logger

from exceptions.main import AppException
from typing import Callable, Optional
from abc import ABC, abstractmethod

logger = app_logger.get_logger(__name__)


class AudioSource(ABC):
    @abstractmethod
    def open(self):
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def read(self):
        ...

    @abstractmethod
    def get_iterations(self, seconds: int):
        ...


class AudioFromMicrophone(AudioSource):
    def __init__(self,
                 framerate: int = 44800,
                 chunk_size: int = 1024,
                 channels: int = 1,
                 duration: float = None,
                 device_id: int = None,
                 callback: Optional[Callable] = None):
        self.pyaudio = pyaudio.PyAudio()
        self.callback = callback
        self.stream = None
        self.framerate = framerate
        self.channels = channels
        self.chunk_size = chunk_size
        self.duration = duration
        self.iterations = None
        self.device_id = device_id or self.pyaudio.get_default_input_device_info()['index']

    def __repr__(self):
        return f"AudioFromMicrophone object (framerate: {self.framerate}, " \
               f"channels: {self.channels}, " \
               f"chunk_size: {self.chunk_size}, " \
               f"device_name: {self.pyaudio.get_device_info_by_index(self.device_id)['name']} )"

    def open(self):
        try:
            self.stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                input=True,
                output=True,
                rate=self.framerate,
                channels=self.channels,
                frames_per_buffer=self.chunk_size,
                input_device_index=self.device_id
            )
            logger.info(f"{self.stream} was initialized")
        except IOError or EOFError as exp:
            error_description = f'{self} failed the PyAudio initialization due to PortAudio error: {exp}'
            logger.error(error_description)
            raise AppException.PyAudioException(
                description=error_description
            )
        except Exception as exp:
            error_description = f'Unknown PyAudioError: {exp}'
            logger.error(error_description)
            raise AppException.PyAudioException(
                description=error_description
            )

    def read(self):
        if self.callback:
            return self.callback(self.stream.read(self.chunk_size))
        return self.stream.read(self.chunk_size)

    def get_iterations(self, seconds: int):
        if seconds is not None:
            return int((self.framerate / self.chunk_size) * seconds)
        else:
            return float('inf')

    def close(self):
        if self.stream is not None:
            self.stream.close()
            logger.info(f'{self.stream} was closed.')
            self.stream = None


class AudioFromFile(AudioSource):
    def __init__(self,
                 file_name: str,
                 chunk_size: int = 1024,
                 callback: Optional[Callable] = None):
        self.callback = callback
        self.chunk_size = chunk_size
        self.file_name = file_name
        self.iterations = None

    def open(self) -> None:
        try:
            self.wave_file = wave.open(self.file_name, 'rb')
            logger.info(f'WAV file {self.file_name} was opened')
        except IOError or EOFError as exp:
            error_desc = f'AudioFromFile object cannot open file {self.file_name} with exception: {exp}'
            logger.error(error_desc)
            raise AppException.WAVFileException(description=error_desc)

    def close(self) -> None:
        try:
            self.wave_file.close()
            logger.info(f'WAV file {self.file_name} was closed')
        except IOError or EOFError as exp:
            error_desc = f'AudioFromFile object cannot close file {self.file_name} with exception: {exp}'
            logger.error(error_desc)
            raise AppException.WAVFileException(description=error_desc)

    def read(self):
        if self.callback:
            return self.callback(in_data=self.wave_file.readframes(self.chunk_size))
        return self.wave_file.readframes(self.chunk_size)

    def get_iterations(self, seconds) -> int:
        frames = self.wave_file.getnframes()
        iterations = frames // self.chunk_size
        if frames % self.chunk_size != 0:
            iterations += 1
        return iterations
