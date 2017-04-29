from function_parser import FunctionParser as Parser
import math


class Executor:
    def __init__(self):
        self.parser = Parser()
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tg': math.tan,
            '^': math.pow,
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }
        self.end_function = None
        self.equations = []

    def add(self, equation):
        self.equations.append(equation)

    def remove(self, index):
        try:
            del self.equations[int(index)]
        except TypeError:
            print("Index out of range")

    def clear(self):
        self.equations.clear()

    def operators(self):
        return self.functions.keys()

    def execute(self):
        pass

if __name__ == "__main__":
    pass
