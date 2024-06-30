import numpy as np
import parselmouth

from audioop import rms
from math import log10
from scipy.signal import butter, filtfilt
from abc import ABC, abstractmethod
from librosa.feature import mfcc, zero_crossing_rate, yin

from typing import Union, List

from audiochains.output_types import (
    FourierTuple,
    VoiceRange,
    np_int16_array,
    np_float32_array
)


class BlockAudioMethod(ABC):
    """
    An abstract interface defining the functionality of audio processing unit.
    """

    @abstractmethod
    def __call__(self, in_data):
        """
        The developer have to override __call__ method
        which performs audio processing on data block (chunk)
        ----
        Parameters:
            in_data: input audio data block
        """
        ...


class UnpackRawInInt16(BlockAudioMethod):
    """
    Unpacking raw audio data (sequences of bytes) in numpy int16 array.
    """

    def __call__(self, in_data: bytes) -> np_int16_array:
        return np.frombuffer(in_data, np.int16)


class UnpackRawInFloat32(BlockAudioMethod):
    """
    Unpacking raw audio data (sequences of bytes) in the numpy float32 array.
    """

    def __call__(self, in_data: bytes) -> np_float32_array:
        max_int16_value = 2 ** 15
        data = np.frombuffer(in_data, np.int16)
        return data.astype(np.float32) / max_int16_value


class RMSFromBytes(BlockAudioMethod):
    """
    Calculating root mean square (RMS) value of the input raw audio block with a certain sample width.
    """

    def __init__(self, width: int = 2):
        self.width = width

    def __call__(self, in_data: bytes) -> int:
        return rms(in_data, self.width)


class RMSFromArray(BlockAudioMethod):
    """
    Calculating root mean square (RMS) value of the input numpy array.
    """

    def __call__(self, in_data: Union[np_int16_array, np_float32_array]) -> int:
        in_data = in_data.astype(np.float32)
        return round(np.sqrt((in_data * in_data).sum() / len(in_data)))


class DBLog10(BlockAudioMethod):
    """
    Calculating logarithmic relative value of input int vale
    """

    def __call__(self, in_data: int):
        if in_data > 0:
            return round(20 * log10(in_data), 2)
        else:
            return 0


class HammingWindow(BlockAudioMethod):
    """
    Superimposing the hamming window on the input numpy array.
    """

    def __call__(self, data: Union[np_int16_array, np_float32_array]) -> np_float32_array:
        return data * np.hamming(len(data))


class FourierTransform(BlockAudioMethod):
    """
    Calculating the fourier transform on the input numpy float32 array with a certain framerate.
    """

    def __init__(self, framerate: int):
        self.framerate = framerate

    def __call__(self, in_data: np_float32_array) -> FourierTuple:
        n = len(in_data)
        d = 1 / self.framerate
        hs = np.abs(np.fft.rfft(in_data))
        fs = np.fft.rfftfreq(n, d)
        return FourierTuple(amplitude=hs, frequency=fs)


class MFCC(BlockAudioMethod):
    """
    Calculating certain number of mfcc coefficients of the input numpy float32 array
    """

    def __init__(self, n_mfcc: int, freq_rate: int):
        super().__init__()
        self.n_mfcc = n_mfcc
        self.freq_rate = freq_rate

    def __call__(self, data: Union[float, np.float32]):
        return mfcc(data, n_mfcc=self.n_mfcc, sr=self.freq_rate)


class BandPassFilter(BlockAudioMethod):
    """
    Application of the butterworth bandpass filter
    """

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
    """
    Calculation of the threshold function to the RMS value of the input audio amplitude
    """

    def __init__(self,
                 silence_value: float,
                 whisper_value: float,
                 normal_value: float):
        self.silence_value = silence_value
        self.whisper_value = whisper_value
        self.normal_value = normal_value

    def __call__(self, in_data: Union[int, float, np.float32]) -> VoiceRange:
        if in_data <= self.silence_value:
            return VoiceRange.SILENCE
        elif in_data <= self.whisper_value:
            return VoiceRange.WHISPER
        elif in_data <= self.normal_value:
            return VoiceRange.NORMAL
        elif in_data > self.normal_value:
            return VoiceRange.LOUD
        
class ZeroCrossingRate(BlockAudioMethod):
    """
    Calculation of the rate at which a signal changes
    from positive to zero to negative or from negative to zero to positive
    """
    def __init__(
            self,
            frame_rate: int = 16000,
            frame_length: int = 1024,
            win_length: int = 512,
        ) -> None:
        super().__init__()
        self.frame_length = frame_length
        self.win_length = win_length
        self.frame_rate = frame_rate

    def __call__(self, in_data: np_float32_array) -> np_float32_array:
        avg_zcr = np.mean(zero_crossing_rate(
            y=in_data,
            frame_length=self.frame_length,
            hop_length=self.win_length,
            ))
        
        avg_zcr *= self.frame_length
        frame_duration = self.frame_length / self.frame_rate
        
        return avg_zcr / frame_duration

    
class YIN(BlockAudioMethod):
    """
    YIN, a fundamental frequency estimator for speech and music
    http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf
    """
    def __init__(
            self,
            frame_rate: int = 16000,
            f_min: int = 50,
            f_max: int = 500
            ) -> None:
        super().__init__()
        self.frame_rate = frame_rate
        self.f_min = f_min
        self.f_max = f_max


    def __call__(self, in_data: np_float32_array) -> np_float32_array:
        return np.mean(
            yin(
                in_data,
                fmin=self.f_min,
                fmax=self.f_max,
                sr=self.frame_rate
            )
        )
    
class PraatPitch(BlockAudioMethod):
    """
    Performs an access to Pratt commands for Pitch calculatiion
    """
    def __init__(self,
            frame_rate: int = 16000,
            f_min: int = 50,
            f_max: int = 500
        ) -> None:
        super().__init__()
        self.frame_rate = frame_rate
        self.f_min = f_min
        self.f_max = f_max

    def __call__(self, in_data: np_float32_array) -> np_float32_array:
        in_data = parselmouth.Sound(in_data, self.frame_rate)
        pitch = in_data.to_pitch(
            time_step=None,
            pitch_floor=self.f_min,
            pitch_ceiling=self.f_max,
        )

        pitch_values = pitch.selected_array['frequency']
        valid_pitch_values = pitch_values[pitch_values > 0]
    
        if len(valid_pitch_values) > 0:
            mean_pitch = np.mean(valid_pitch_values)
        else:
            mean_pitch = 0
        
        return mean_pitch
