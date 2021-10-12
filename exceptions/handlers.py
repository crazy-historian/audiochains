from exceptions.main import AppExceptionCase


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AppExceptionCase as exc:
            print("Сообщению пользователю об ошибке!")
            print(f"Приложение обрабатывает ошибку {exc}")

    return wrapper
