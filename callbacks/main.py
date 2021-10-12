import numpy as np
# import aubio
import numpy.typing as npt

from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod

# np_int16_array = npt.NDArray[np.int16]
# np_float32_array = npt.NDArray[np.float32]    # FIXME: replace to universal numpy type

np_int16_array = np.array
np_float32_array = np.array


@dataclass
class FourierTuple:
    amplitude: np.ndarray
    frequency: np.ndarray


class CallbackFilter(ABC):
    @abstractmethod
    def __call__(self, in_data):
        ...


class CallbackWriter(CallbackFilter):
    def __call__(self, in_data) -> None:
        ...


class CallbackChainOfFilters:
    def __init__(self, *chain):
        self.chain = chain

    def __call__(self, in_data):
        for callback_filter in self.chain:
            in_data = callback_filter(in_data)
        return in_data
