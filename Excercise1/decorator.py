"""Демонстрация работы декоратора с входными параметрами-функциями и самописными эксепшенами."""

import re
from exceptions.exceptions_for_exc1 import (InputParameterVerificationError,
                                            NullRepeatError,
                                            ResultVerificationError)
from functools import wraps
from typing import Callable

from jsonschema import ValidationError, validate

SCHEMA = {
    "type": "object",
    "examples": [
        {
            "id": 5,
            "name": "Yuri",
            "age": 33,
            "gender": "male"
        }
    ],
    "required": [
        "id",
        "name",
        "age",
        "gender"
    ],
    "additionalProperties": False,
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "integer",
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
        },
        "age": {
            "$id": "#/properties/age",
            "type": "integer",
        },
        "gender": {
            "$id": "#/properties/gender",
            "type": "string",
        }
    }
}

json_file = {
            "id": 5,
            "name": "Yuri",
            "age": 33,
            "gender": "male"
        }


def param_validator(input_validation: Callable, result_validation: Callable,
                    on_fail_repeat_times: int = 1, default_behavior: Callable = None) -> Callable:
    """Декоратор для проверки атрибута оборачиваемой функции и результата её выполнения.

    Parameters:
        input_validation (Callable): функция для проверки входных параметров.
        result_validation (Callable): функция для проверки результата выполнения оборачиваемой декоратором функции.
        on_fail_repeat_times (int): количество раз повторения вызова функции при провале валидации результата.
            При установке параметра в значение 0 выдаёт исключение NullRepeatError.
            При отрицательном значении параметра функция, над которои стоит декоратор,
            выполнится пока результат не пройдёт условия проверки либо буде выполняться вечно.
        default_behavior (Callable): функция, которая выполнится при истечении дозволенного количества повторений
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(param: dict) -> None:

            # валидируем входной параметр
            try:
                is_input_valid = input_validation(param)
                if not is_input_valid:
                    raise InputParameterVerificationError(param)
            except InputParameterVerificationError:
                raise

            repeat = on_fail_repeat_times
            if repeat == 0:
                raise NullRepeatError
            while repeat != 0:
                repeat -= 1
                # выполняем основную функцию
                result = func(param)

                # валидируем результат выполнения основной функции
                try:
                    is_result_valid = result_validation(result)
                    if is_result_valid:
                        return result  # если результат валиден - возвращаем результат
                    else:
                        if repeat == 1:
                            if default_behavior:
                                default_behavior()
                            else:
                                raise ResultVerificationError(result)
                except ResultVerificationError:
                    raise
            return None
        return wrapper
    return decorator


def inp_val(json_data: dict) -> bool:
    """Валидация входящего параметра (json-словаря) другой функции."""
    try:
        return not bool(validate(json_data, SCHEMA))
    except ValidationError:
        return False


def res_val(result: str) -> bool:
    """Верификация результата выполнения другой функции (соответствие строки регулярному выражению)."""
    regex = re.compile("^[A-Z][a-z]{2,9}$")
    return bool(regex.match(result))


def def_behave() -> None:
    """Функция, срабатывающая, если не удалось верифицировать результат выполнения другой функции."""
    print('Верифицировать результат исполнения не получилось')


@param_validator(input_validation=inp_val, result_validation=res_val,
                 on_fail_repeat_times=3, default_behavior=def_behave)
def some_func(json_data: dict) -> str:
    """Оборачиваемая декоратором функция. Принимает на вход json-словарь, выдаёт содержимое словаря по ключу 'name'."""
    return json_data['name']


print(some_func(json_file))
