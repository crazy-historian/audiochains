from block_methods import (
    UnpackRawInInt16,
    RMSFromBytes,
    RMSFromArray
)
from streams import StreamFromFile


def test_rms_from_bytes():
    with StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        file_stream.set_methods(
            RMSFromBytes()
        )
        for _ in range(file_stream.get_iterations()):
            file_stream.apply()


def test_rms_from_array():
    with StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        file_stream.set_methods(
            UnpackRawInInt16(),
            RMSFromArray()
        )
        for _ in range(file_stream.get_iterations()):
            file_stream.apply()