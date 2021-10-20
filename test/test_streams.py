import json
from writers import WriterInWAV
from streams import StreamWithChain, StreamFromFile, input_output_sampwidth


def test_stream_init():
    stream = StreamWithChain(samplerate=22000, blocksize=1024, channels=1)
    assert (stream.samplerate, stream.blocksize, stream.channels) == (22000.0, 1024, (1, 1))


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
    with StreamFromFile(filename='test_playback.wav', blocksize=1024) as file_stream:
        for _ in range(file_stream.get_iterations()):
            file_stream.read(file_stream.blocksize)


def test_stream_recording():
    with StreamWithChain(json_file='test_config.json') as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)


def test_stream_sampwidth():
    with StreamWithChain(json_file='test_config.json') as stream:
        for _ in range(stream.get_iterations(seconds=1)):
            stream.read(stream.blocksize)


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
