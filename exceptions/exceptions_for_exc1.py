"""Исключения для первого задания."""


class InputParameterVerificationError(Exception):
    """Ошибка верификации входного параметра верифицируемой функции."""

    def __init__(self, param: dict, message: str = "Верификация входных данных не пройдена.") -> None:
        """Принимает верифицируемый параметр и, при необходимости, кастомное уведомление."""
        super().__init__()
        self.param = param
        self.message = message

    def __str__(self) -> str:
        """Выводит уведомление и поступившие в параметре данные."""
        return f'{self.message}\nНекорректные данные:\n{self.param}\n'


class ResultVerificationError(Exception):
    """Ошибка верификации результата выполнения верифицируемой функции."""

    def __init__(self, result: str, message: str = "Верификация результата выполнения функции не пройдена.") -> None:
        """Принимает результат и, при необходимости, кастомное уведомление."""
        super().__init__()
        self.result = result
        self.message = message

    def __str__(self) -> str:
        """Выводит уведомление и поступившие в параметре данные."""
        return f'{self.message}\nНекорректный результат:\n{self.result}\n'


class NullRepeatError(Exception):
    """Ошибка, если параметр количества повторений был установлен равным нулю."""

    def __str__(self) -> str:
        """Выводит сообщение об ошибке."""
        return 'Нельзя устанавливать нулевое количество повторений'
