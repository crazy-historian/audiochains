import pytest
import wave
import json
from writers import WriterInWAV
from streams import IOStream, InputStream, StreamFromFile
from chains import ChainOfMethods
from block_methods import RMSFromArray, UnpackRawInFloat32


@pytest.mark.parametrize("test_input, expected", [
    ({"samplerate": 8000, "blocksize": 512, "channels": 1}, (8000.0, 512, (1, 1))),
    ({"samplerate": 16000, "blocksize": 1024, "channels": 1}, (16000.0, 1024, (1, 1))),
    ({"samplerate": 22000, "blocksize": 1024, "channels": 1}, (22000.0, 1024, (1, 1))),
    ({"samplerate": 22050, "blocksize": 1024, "channels": 1}, (22050.0, 1024, (1, 1))),
    ({"samplerate": 44100, "blocksize": 1024, "channels": 1}, (44100.0, 1024, (1, 1))),
    ({"samplerate": 48000, "blocksize": 1024, "channels": 2}, (48000.0, 1024, (2, 2))),
])
def test_io_stream_init(test_input, expected):
    stream = IOStream(**test_input)
    assert (stream.samplerate, stream.blocksize, stream.channels) == expected


@pytest.mark.parametrize("test_input, expected", [
    ({"samplerate": 8000, "blocksize": 512, "channels": 1}, (8000.0, 512, 1)),
    ({"samplerate": 16000, "blocksize": 1024, "channels": 1}, (16000.0, 1024, 1)),
    ({"samplerate": 22000, "blocksize": 1024, "channels": 1}, (22000.0, 1024, 1)),
    ({"samplerate": 22050, "blocksize": 1024, "channels": 1}, (22050.0, 1024, 1)),
    ({"samplerate": 44100, "blocksize": 1024, "channels": 1}, (44100.0, 1024, 1)),
    ({"samplerate": 48000, "blocksize": 1024, "channels": 2}, (48000.0, 1024, 2)),
])
def test_input_stream_init(test_input, expected):
    stream = InputStream(**test_input)
    assert (stream.samplerate, stream.blocksize, stream.channels) == expected


def test_io_stream_init_from_json():
    with open('test_config.json', 'r') as file:
        test_config = json.load(file)
        stream = IOStream(json_file='test_config.json')
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


def test_input_stream_init_from_json():
    with open('test_config.json', 'r') as file:
        test_config = json.load(file)
        stream = InputStream(json_file='test_config.json')
        assert (
                   stream.samplerate,
                   stream.blocksize,
                   stream.channels,
                   stream.dtype
               ) == (
                   float(test_config['framerate']),
                   test_config['chunk_size'],
                   test_config['channels'],
                   'int16',
               )


def test_stream_from_file_init():
    with wave.open('test_playback.wav', 'r') as wav_file, \
            StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        wav_parameters = wav_file.getparams()
        assert (
                   wav_parameters.nchannels,
                   wav_parameters.framerate,
                   1024
               ) == (
                   file_stream.channels,
                   file_stream.samplerate,
                   file_stream.blocksize
               )


def test_io_stream_recording():
    with IOStream(json_file='test_config.json') as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)


def test_input_stream_recording():
    with InputStream(json_file='test_config.json') as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)


def test_stream_from_file_recording():
    with StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        for _ in range(file_stream.get_iterations()):
            file_stream.read(file_stream.blocksize)


@pytest.mark.parametrize("test_stream_parameters, expected", [
    ({"sampwidth": 1, "blocksize": 1024}, (1024, ("int8", "int8"))),
    ({"sampwidth": 2, "blocksize": 1024}, (2048, ("int16", "int16"))),
    ({"sampwidth": 3, "blocksize": 1024}, (3072, ("int24", "int24"))),
    ({"sampwidth": 4, "blocksize": 1024}, (4096, ("float32", "float32")))
])
def test_stream_sampwidth(test_stream_parameters, expected):
    with IOStream(**test_stream_parameters) as stream:
        assert len(stream.read(stream.blocksize)), stream.dtype == expected


@pytest.mark.parametrize("test_stream_parameters, expected", [
    ({"sampwidth": 1, "blocksize": 1024}, (1024, "int8")),
    ({"sampwidth": 2, "blocksize": 1024}, (2048, "int16")),
    ({"sampwidth": 3, "blocksize": 1024}, (3072, "int24")),
    ({"sampwidth": 4, "blocksize": 1024}, (4096, "float32"))
])
def test_stream_sampwidth(test_stream_parameters, expected):
    with IOStream(**test_stream_parameters) as stream:
        assert len(stream.read(stream.blocksize)), stream.dtype == expected


def test_io_stream_file_recording():
    with IOStream(json_file='test_config.json') as stream, \
            WriterInWAV(
                file_name='test_recording.wav',
                framerate=stream.samplerate,
                channels=stream.channels[0],
                sampwidth=2
            ) as writer:
        for _ in range(stream.get_iterations(seconds=1)):
            writer.write(stream.read(stream.blocksize))


def test_input_stream_file_recording():
    with InputStream(json_file='test_config.json') as stream, \
            WriterInWAV(
                file_name='test_recording.wav',
                framerate=stream.samplerate,
                channels=stream.channels,
                sampwidth=2
            ) as writer:
        for _ in range(stream.get_iterations(seconds=1)):
            writer.write(stream.read(stream.blocksize))


def test_io_stream_set_methods():
    with IOStream(json_file='test_config.json') as stream:
        stream.set_methods(
            UnpackRawInFloat32(),
            RMSFromArray()
        )
        for _ in range(stream.get_iterations(seconds=1)):
            stream.apply()


def test_io_stream_set_chain():
    with IOStream(json_file='test_config.json') as stream:
        chain = ChainOfMethods(
            UnpackRawInFloat32(),
            RMSFromArray()
        )
        stream.set_chain(chain)
        for _ in range(stream.get_iterations(seconds=1)):
            stream.apply()


def test_input_stream_set_methods():
    with InputStream(json_file='test_config.json') as stream:
        stream.set_methods(
            UnpackRawInFloat32(),
            RMSFromArray()
        )
        for _ in range(stream.get_iterations(seconds=1)):
            stream.apply()


def test_input_stream_set_chain():
    with InputStream(json_file='test_config.json') as stream:
        chain = ChainOfMethods(
            UnpackRawInFloat32(),
            RMSFromArray()
        )
        stream.set_chain(chain)
        for _ in range(stream.get_iterations(seconds=1)):
            stream.apply()
