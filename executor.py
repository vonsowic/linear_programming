from function_parser import FunctionParser as Parser
from iterator import forEach
import math
from random import uniform
import threading


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
            'sum': lambda *elements: sum(elements),
            'abs': lambda number: abs(number),
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
        self.epsilon = 0.1 ** 6
        self.number_of_threads = 10
        self.maximize = True
        self.multi_threading = False
        self.radian = 1000.0

    def add(self, equation):
        self.equations.append(equation)

    def set_radian(self, radian):
        self.radian = radian

    def remove(self, index):
        try:
            del self.equations[int(index)]
        except TypeError:
            print("Index out of range")

    def set_epsilon(self, eps):
        self.epsilon = float(eps)

    def set_end_function(self, equation):
        self.end_function = equation

    # TODO finish
    def create_custom_function(self, name, body):
        args = self.find_parameters(body)
        function_name = name[:]
        for arg in body:
            args += arg + ","
        args = args[:len(args) - 1]

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

        excluded = list(self.get_operators()) + list(self.symbols.keys())

        def find_operators(tmp_expression):
            tmp = set()
            for item in tmp_expression:
                if type(item) is list:
                    tmp.update(find_operators(item))
                elif item not in excluded and type(item) is str:
                    tmp.add(item)
            return tmp

        return find_operators(expression)

    @staticmethod
    def fill_variables(equation, values):
        """ :param equation: list representing equation
            :param values: map, where keys are variables like x or y and values are floats
        """
        return forEach(equation, lambda x: values[x], lambda x: x in values)

    def calculate(self, equation):
        result = equation[:]
        # FIXME: it can be better
        try:
            if type(result[1][0]) is list:
                result[1][0] = self.calculate(result[1][0])
        except TypeError:
            pass

        try:
            if type(result[1][1]) is list:
                result[1][1] = self.calculate(result[1][1])
        except TypeError:
            pass

        return self.functions[result[0]](*result[1])

    def execute(self):
        # initialize
        radian = self.radian

        # parse string equations to list representations
        equations = forEach(self.equations, lambda item: self.parser.parse(item), recursion=False)
        end_function = self.parser.parse(self.end_function)

        # change constant symbols to matching floats
        equations = self.fill_variables(equations, self.symbols)

        variables = self.get_decision_variables()

        best_result = {key: 0.0 for key in variables}
        best_solution = self.calculate(self.fill_variables(end_function, best_result))

        if self.multi_threading:
            threads = (threading.Thread(), ) * self.number_of_threads

        def number_of_samples():
            return int((radian * 2.5) ** len(variables))

        def random_values():
            """:return point inside figure, where best_solution is center"""
            return {key: uniform(best_result[key] - radian, best_result[key] + radian) for key in variables}

        # end of initialization

        while radian - self.epsilon > 0:
            points = [random_values() for i in range(number_of_samples())]

            solutions = []
            excluded = []
            for index, point in enumerate(points):
                if not self.multi_threading:
                    if all([self.calculate(self.fill_variables(equation, point)) for equation in equations]):
                        solutions.append(point)
                    else:
                        excluded.append(point)
                else:
                    pass

            for solution in solutions:
                tmp = self.calculate(self.fill_variables(end_function, solution))
                if self.maximize:
                    is_positive_difference = tmp > best_solution
                else:
                    is_positive_difference = tmp < best_solution

                if is_positive_difference:
                    best_solution = tmp
                    best_result = solution

            radian *= 0.925
            print(radian, ":", best_result)

        return best_result
