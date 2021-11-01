"""
    The definition of BlockAudioMethod possible output data types.
"""

import numpy as np
from dataclasses import dataclass
from enum import IntEnum

np_int16_array = np.ndarray
np_float32_array = np.ndarray


@dataclass
class FourierTuple:
    amplitude: np.ndarray
    frequency: np.ndarray


class VoiceRange(IntEnum):
    SILENCE = 0
    WHISPER = 1
    NORMAL = 2
    LOUD = 3
