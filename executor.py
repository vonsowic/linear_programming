import math


class Executor:
    def __init__(self):
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tg': math.tan,
            '^': math.pow,
            '+': Executor.sum,
            '-': Executor.diff,
            '*': Executor.prod,
            '/': Executor.div,
        }
        self.end_function = None
        self.equations = []

    def add(self, equation):
        self.equations.append(equation)

    def remove(self, index):
        del self.equations[index]

    def clear(self):
        self.equations.clear()

    def operators(self):
        return self.functions.keys()

    def execute(self):
        pass

    @staticmethod
    def sum(x, y):
        return x + y

    @staticmethod
    def diff(x, y):
        return x - y

    @staticmethod
    def prod(x, y):
        return x * y

    @staticmethod
    def div(x, y):
        return x / y

if __name__ == "__main__":
    pass
