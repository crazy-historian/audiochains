AVAILABLE_FREQUENCIES = [8000, 16000, 22400, 44800]

import pathlib
from enum import IntEnum

project_path = pathlib.Path(__file__).parent


class VoiceRange(IntEnum):
    SILENCE = 0
    WHISPER = 1
    NORMAL = 2
    LOUD = 3


class VoiceTaskType(IntEnum):
    SINGLE = 0
    CONTINUOUS = 1
    DISCONTINUOUS = 2
