class InputParameterVerificationError(Exception):
    def __init__(self, input_param, message="Верификация входных данных не пройдена"):
        super().__init__()
        self.input_parameter = input_param
        self.message = message

    def __str__(self):
        return f'{self.message}\nПолученные данные:\n{self.input_parameter}'


class ResultVerificationError(Exception):
    def __init__(self, output_param, message="Верификация результата выполнения функции не пройдена"):
        super().__init__()
        self.output_parameter = output_param
        self.message = message

    def __str__(self):
        return f'{self.message}\nПолученные данные:\n{self.output_parameter}'
