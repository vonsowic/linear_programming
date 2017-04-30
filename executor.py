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
            '^': math.pow,
            '/': lambda a, b: a / b,
            '%': lambda a, b: a % b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
            '!': math.factorial,
            'sum': sum,
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
        self.maximize = True
        self.multi_threading = False

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

    def get_operators(self):
        return self.functions.keys()

    def get_functions(self):
        return [key for key, func in self.functions.items() if key not in self.operators]

    def get_decision_variables(self, expression=None):
        if expression is None:
            expression = self.end_function

        if type(expression) is str:
            expression = self.parser.parse(expression)

        operators = self.get_operators()

        def find_operators(tmp_expression):
            tmp = set()
            for item in tmp_expression:
                if type(item) is list:
                    tmp.update(find_operators(item))
                elif item not in operators and not item.isdigit():
                    tmp.add(item)
            return tmp

        return find_operators(expression)

    def execute(self):
        pass


if __name__ == "__main__":
    executor = Executor()
    executor.end_function = "3*x^200+(2*y)+9*z"
    print(executor.get_decision_variables())

