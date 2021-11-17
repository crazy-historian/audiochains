from audiochains.block_methods import (
    UnpackRawInInt16,
    RMSFromBytes,
    RMSFromArray,
    DBLog10,
    SoundPressureThreshold
)
from audiochains.output_types import VoiceRange
from audiochains.streams import StreamFromFile


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


def test_sound_pressure_threshold():
    with StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        file_stream.set_methods(
            RMSFromBytes(),
            DBLog10(),
            SoundPressureThreshold(
                silence_value=10.0,
                whisper_value=30.0,
                normal_value=50.0
            )
        )
        assert isinstance(file_stream.apply(), VoiceRange)
        for _ in range(file_stream.get_iterations()):
            file_stream.apply()
