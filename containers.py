from dependency_injector import containers, providers
from stream import AudioStream
from callbacks.chains import VoicePowerChain
from microphone import IMicrophone
from source import AudioFromMicrophone, AudioFromFile
from exceptions.handlers import exception_handler

test_config = {
    'recording': {
        'framerate': 44800,
        'chunk_size': 1024,
        'channels': 1,
        'device_id': IMicrophone().get_default_input_device_info()['index'],
        'duration': None,
        'silence': [0, 500],
        'whisper': [501, 1000],
        'normal': [1001, 2000],
        'loud': [2001, 5000]
    },
    'playback': {
        'file_name': 'test.wav',
        'chunk_size': 1024
    }
}


class VoicePowerAudioProcessing(containers.DeclarativeContainer):
    config = providers.Configuration()

    callback = providers.Container(
        VoicePowerChain,
        config=config.recording,
    )

    audio_from_microphone = providers.Singleton(
        AudioFromMicrophone,
        framerate=config.recording.framerate,
        chunk_size=config.recording.chunk_size,
        channels=config.recording.channels,
        duration=config.recording.duration,
        device_id=config.recording.duration,
        callback=callback.filtered
    )

    audio_from_microphone_game = providers.Singleton(
        AudioFromMicrophone,
        framerate=config.recording.framerate,
        chunk_size=config.recording.chunk_size,
        channels=config.recording.channels,
        duration=config.recording.duration,
        device_id=config.recording.duration,
        callback=callback.voice_threshold
    )

    audio_from_file = providers.Singleton(
        AudioFromFile,
        file_name=config.playback.file_name,
        chunk_size=config.playback.chunk_size,
        # callback=callback.filtered
        callback=callback.voice_threshold
    )

    stream = providers.Singleton(
        AudioStream,
        source=audio_from_microphone
    )

    file = providers.Singleton(
        AudioStream,
        source=audio_from_file
    )

    game = providers.Singleton(
        AudioStream,
        source=audio_from_microphone_game
    )


@exception_handler
def stream_main():
    container = VoicePowerAudioProcessing()
    container.config.from_dict(test_config)
    with container.stream() as stream:
        for i in range(stream.get_iterations(seconds=2)):
            print(stream.read())


@exception_handler
def file_main():
    container = VoicePowerAudioProcessing()
    container.config.from_dict(test_config)
    with container.file() as stream:
        for i in range(stream.get_iterations(seconds=2)):
            print(stream.read())
