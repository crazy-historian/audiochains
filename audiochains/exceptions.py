class AppExceptionCase(Exception):
    def __init__(self, description: str):
        self.exception_case = self.__class__.__name__
        self.description = description

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            f" - description ={self.description}>"
        )


class AppException:
    class ChainOfMethodsException(AppExceptionCase):
        def __init__(self, description: str = None):
            """
            PyAudio stream initializing was failed.
            """
            AppExceptionCase.__init__(self, description)

    class WAVFileException(AppExceptionCase):
        def __init__(self, description: str = None):
            """
            WAV file cannot be opened, closed or does not exist.
            """
            AppExceptionCase.__init__(self, description)
