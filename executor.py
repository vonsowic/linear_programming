from function_parser import FunctionParser as Parser
import math


class Executor:
    def __init__(self):
        self.parser = Parser()
        self.operators = self.parser.get_operators()
        self.functions = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '^': lambda a, b: math.pow(a, b),
            '/': lambda a, b: a / b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
            'sin': math.sin,
            'asin': math.asin,
            'asinh': math.asinh,
            'cos': math.cos,
            'acos': math.acos,
            'acosh': math.acosh,
            'tg': math.tan,
            'atg': math.atan,
            'atgh': math.atanh,
            'max': max,
            'min': min,
            '!': math.factorial,
            'ln': math.log,
            'log': math.log,
            'log10': math.log10,
        }
        self.parser.functions = self.get_functions()
        self.symbols = {
            'pi': math.pi,
            'e': math.e,
        }
        self.end_function = None
        self.equations = []
        self.epsilon = 0.1

    def add(self, equation):
        self.equations.append(equation)

    def remove(self, index):
        try:
            del self.equations[int(index)]
        except TypeError:
            print("Index out of range")

    def set_epsilon(self, eps):
        self.epsilon = float(eps)

    def set_end_function(self, equation):
        self.end_function = equation

    @staticmethod
    def find_parameters(equation):
        result = []
        return result

    # TODO finish
    def create_custom_function(self, name, body):
        args = self.find_parameters(body)
        function_name = name[:]
        for arg in body:
            args += arg + ","
        args = args[:len(args)-1]

        exec("def " + function_name + "(" + args + "):\n\t")
        self.functions[function_name] = name

    def clear(self):
        self.equations.clear()

    def get_functions(self):
        return [key for key, func in self.functions.items() if key not in self.operators]

    def execute(self):
        pass


if __name__ == "__main__":
    executor = Executor()

