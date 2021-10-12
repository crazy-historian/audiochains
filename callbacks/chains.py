from dependency_injector import containers, providers
from callbacks.main import CallbackChainOfFilters
from callbacks.methods import (
    UnpackRawInInt16Callback,
    UnpackRawInFloat32Callback,
    RMSFromArrayCallback,
    RMSFromBytesCallback,
    BandPassCallback,
    VolumeCallback
)


class VoicePowerChain(containers.DeclarativeContainer):
    config = providers.Configuration()

    unpack_in_int16 = providers.Singleton(
        UnpackRawInInt16Callback
    )

    unpack_in_float32 = providers.Singleton(
        UnpackRawInFloat32Callback
    )

    rms_from_bytes = providers.Singleton(
        RMSFromBytesCallback
    )

    rms_from_array = providers.Singleton(
        RMSFromArrayCallback
    )

    bandpass = providers.Singleton(
        BandPassCallback,
        sample_rate=config.framerate
    )

    volume_threshold = providers.Singleton(
        VolumeCallback,
        silence_diapason=config.silence,
        whisper_diapason=config.whisper,
        normal_diapason=config.normal,
        loud_diapason=config.loud
    )

    from_bytes = providers.Callable(
        CallbackChainOfFilters,
        rms_from_bytes
    )

    filtered = providers.Callable(
        CallbackChainOfFilters,
        unpack_in_int16,
        bandpass,
        rms_from_array
    )

    voice_threshold = providers.Callable(
        CallbackChainOfFilters,
        filtered,
        volume_threshold
    )
