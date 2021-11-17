from typing import Callable
from threading import Thread, Event


def in_thread(target_function: Callable[..., None]) -> Callable[..., None]:
    """
    This function is used as decorator for concurrent audio processing

    :param target_function: real-time audio recording method
    :return:
    """

    def wrapper(*args, **kwargs):
        current_thread = Thread(target=target_function,
                                args=args, kwargs=kwargs)
        current_thread.start()

    return wrapper


class AudioInThread(Thread):
    """
    This class is aimed to wrap the audio recording in thread executing with possibility
    to send stop signal.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()
        self.daemon = True

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()
