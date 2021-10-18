import numpy as np
from audioop import rms
from scipy.signal import butter, filtfilt
from abc import ABC, abstractmethod
from librosa.feature import mfcc
from typing import Union, List

from output_types import (
    FourierTuple,
    VoiceRange,
    np_int16_array,
    np_float32_array
)


class BlockAudioMethod(ABC):
    @abstractmethod
    def __call__(self, in_data):
        ...


class UnpackRawInInt16(BlockAudioMethod):
    def __call__(self, in_data: bytes) -> np_int16_array:
        return np.frombuffer(in_data, np.int16)


class UnpackRawInFloat32(BlockAudioMethod):
    def __call__(self, in_data: bytes) -> np_float32_array:
        max_int16_value = 2 ** 15
        data = np.frombuffer(in_data, np.int16)
        return data.astype(np.float32) / max_int16_value


class RMSFromBytes(BlockAudioMethod):
    def __init__(self, width: int = 2):
        self.width = width

    def __call__(self, in_data: bytes) -> int:
        return rms(in_data, self.width)


class RMSFromArray(BlockAudioMethod):
    def __call__(self, in_data: Union[np_int16_array, np_float32_array]) -> int:
        in_data = in_data.astype(np.float32)
        return round(np.sqrt((in_data * in_data).sum() / len(in_data)))


class HammingWindow(BlockAudioMethod):
    def __call__(self, data: Union[np_int16_array, np_float32_array]) -> np_float32_array:
        return data * np.hamming(len(data))


class FourierTransform(BlockAudioMethod):
    def __init__(self, framerate: int):
        self.framerate = framerate

    def __call__(self, in_data: np_float32_array) -> FourierTuple:
        n = len(in_data)
        d = 1 / self.framerate
        hs = np.abs(np.fft.rfft(in_data))
        fs = np.fft.rfftfreq(n, d)
        return FourierTuple(amplitude=hs, frequency=fs)


class MFCC(BlockAudioMethod):
    def __init__(self, n_mfcc: int, freq_rate: int):
        super().__init__()
        self.n_mfcc = n_mfcc
        self.freq_rate = freq_rate

    def __call__(self, data: Union[float, np.float32]):
        return mfcc(data, n_mfcc=self.n_mfcc, sr=self.freq_rate)


class BandPassFilter(BlockAudioMethod):
    def __init__(self,
                 sample_rate: int,
                 low_cut: int = 200,
                 high_cut: int = 1000,
                 order: int = 3,
                 out_type=np.int16):
        self.nyq_frequency = 0.5 * sample_rate
        self.low = low_cut / self.nyq_frequency
        self.high = high_cut / self.nyq_frequency
        self.b, self.a = butter(order, Wn=(self.low, self.high), btype='bandpass', analog=False)
        self.out_type = out_type

    def __call__(self, data: np_float32_array):
        return filtfilt(self.b, self.a, data).astype(self.out_type)


class SoundPressureThreshold(BlockAudioMethod):
    def __init__(self,
                 silence_diapason: List[int],
                 whisper_diapason: List[int],
                 normal_diapason: List[int],
                 loud_diapason: List[int]):
        self.silence_diapason = silence_diapason
        self.whisper_diapason = whisper_diapason
        self.normal_diapason = normal_diapason
        self.loud_diapason = loud_diapason

    def __call__(self, in_data: Union[int, np.float32]) -> VoiceRange:
        if in_data <= self.silence_diapason[1]:
            return VoiceRange.SILENCE
        elif self.whisper_diapason[0] <= in_data <= self.whisper_diapason[1]:
            return VoiceRange.WHISPER
        elif self.normal_diapason[0] <= in_data <= self.normal_diapason[1]:
            return VoiceRange.NORMAL
        elif self.loud_diapason[0] <= in_data:
            return VoiceRange.LOUD



