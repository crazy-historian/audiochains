"""
    The definition of BlockAudioMethod possible output data types.
"""


import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from enum import IntEnum

np_int16_array = npt.NDArray[np.int16]
np_float32_array = npt.NDArray[np.float32]


@dataclass
class FourierTuple:
    amplitude: np.ndarray
    frequency: np.ndarray


class VoiceRange(IntEnum):
    SILENCE = 0
    WHISPER = 1
    NORMAL = 2
    LOUD = 3
