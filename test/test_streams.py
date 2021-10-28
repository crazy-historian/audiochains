import pytest

import json
from writers import WriterInWAV
from streams import StreamWithChain, StreamWithChainFromFile



def test_schema_validation():
    ...

@pytest.mark.parametrize("test_input, expected", [
    ({"samplerate": 8000, "blocksize": 512, "channels": 1}, (8000.0, 512, (1, 1))),
    ({"samplerate": 16000, "blocksize": 1024, "channels": 1}, (16000.0, 1024, (1, 1))),
    ({"samplerate": 22000, "blocksize": 1024, "channels": 1}, (22000.0, 1024, (1, 1))),
    ({"samplerate": 22050, "blocksize": 1024, "channels": 1}, (22050.0, 1024, (1, 1))),
    ({"samplerate": 44100, "blocksize": 1024, "channels": 1}, (44100.0, 1024, (1, 1))),
    ({"samplerate": 48000, "blocksize": 1024, "channels": 2}, (48000.0, 1024, (2, 2))),
])
def test_stream_init(test_input, expected):
    stream = StreamWithChain(**test_input)
    assert (stream.samplerate, stream.blocksize, stream.channels) == expected


def test_stream_init_from_json():
    with open('test_config.json', 'r') as file:
        test_config = json.load(file)
        stream = StreamWithChain(json_file='test_config.json')
        assert (
                   stream.samplerate,
                   stream.blocksize,
                   stream.channels,
                   stream.dtype
               ) == (
                   float(test_config['framerate']),
                   test_config['chunk_size'],
                   (test_config['channels'], test_config['channels']),
                   ('int16', 'int16')
               )


def test_stream_from_file_init():
    with StreamWithChainFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        for _ in range(file_stream.get_iterations()):
            file_stream.read(file_stream.blocksize)


def test_stream_recording():
    with StreamWithChain(json_file='test_config.json') as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)


@pytest.mark.parametrize("test_stream_parameters, expected", [
    ({"sampwidth": 1, "blocksize": 1024}, (1024, ("int8", "int8"))),
    ({"sampwidth": 2, "blocksize": 1024}, (2048, ("int16", "int16"))),
    ({"sampwidth": 3, "blocksize": 1024}, (3072, ("int24", "int24"))),
    ({"sampwidth": 4, "blocksize": 1024}, (4096, ("float32", "float32")))
])
def test_stream_sampwidth(test_stream_parameters, expected):
    with StreamWithChain(**test_stream_parameters) as stream:
        assert len(stream.read(stream.blocksize)), stream.dtype == expected


def test_file_recording():
    with StreamWithChain(json_file='test_config.json') as stream, \
            WriterInWAV(
                file_name='test_recording.wav',
                framerate=stream.samplerate,
                channels=stream.channels[0],
                sampwidth=2
            ) as writer:
        for _ in range(stream.get_iterations(seconds=1)):
            writer.write(stream.read(stream.blocksize))
