from function_parser import FunctionParser as Parser
from iterator import forEach
import math
from random import uniform
from threading import Thread
from threading import Lock
from queue import Queue


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
            'inf': math.inf,
            'nan': math.nan,
            'tau': math.tau,
        }

        self.equations = []
        self.end_function = None
        self.epsilon = None
        self.number_of_threads = None
        self.maximize = True
        self.multi_threading = True
        self.radian = None
        self.centre = None
        self.initialize()

    def initialize(self):
        self.end_function = None
        self.epsilon = 0.1 ** 6
        self.number_of_threads = 10
        self.maximize = True
        self.multi_threading = True
        self.radian = 1000.0
        self.centre = 0.0

    def add(self, equation):
        u"""Adds "subject to" function"""
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
        if type(body) is str:
            body = self.parser.parse(body)

        function_name = name

        exec("def " + function_name + "(*args):\n\tvar = self.get_decisibody ")
        self.functions[function_name] = name

    def clear(self):
        self.equations.clear()

    def clear_all(self):
        self.clear()
        self.initialize()

    def get_operators(self):
        return self.functions.keys()

    def get_functions(self):
        return [key for key, func in self.functions.items() if key not in self.operators]

    def set_number_of_threads(self, size):
        self.number_of_threads = size

    def set_range(self, begging, end):
        self.radian = abs(end - begging) / 2
        self.centre = (end - begging)

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
        if type(equation) is str:
            result = self.parser.parse(equation)
        else:
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

        initial_point = {key: self.centre for key in variables}

        fields = self.ExecuteFields(
            initial_point,
            self.calculate(self.fill_variables(end_function, initial_point))
        )

        lock = Lock()
        if self.multi_threading:

            def threads_task():
                while True:
                    with lock:
                        next_iteration = fields.task_index > 0
                        print("Next iteration", next_iteration)

                    if next_iteration:
                        print("Next iteration is true")
                        with lock:
                            fields.task_index -= 1
                        find_possible_result()

            threads = []
            for i in range(self.number_of_threads):
                print("initialize thread")
                t = Thread(target=threads_task)
                t.daemon = True
                threads.append(t)
                t.start()

        def number_of_samples():
            return int((radian * 2.5 + 100) ** len(variables))

        def random_values():
            """:return point inside figure, where best_solution is center"""
            return {key: uniform(fields.best_point[key] - radian, fields.best_point[key] + radian) for key in variables}

        def find_possible_result():
            point = random_values()
            if all([self.calculate(self.fill_variables(equation, point)) for equation in equations]):
                tmp_result = self.calculate(self.fill_variables(end_function, point))

                with lock:
                    if self.maximize:
                        is_positive_difference = tmp_result > fields.best_result
                    else:
                        is_positive_difference = tmp_result < fields.best_result

                    if is_positive_difference:
                        fields.best_point = point
                        fields.best_result = tmp_result

        # end of initialization

        while radian - self.epsilon > 0:

            if self.multi_threading:
                fields.task_index = number_of_samples()
                print("Task index assging:", fields.task_index)
            else:
                for index in range(number_of_samples()):
                    find_possible_result()

            if self.multi_threading:
                for thread in threads:
                    print("wait to join")
                    thread.join()

            print(radian, ":", fields.best_point, " - times:", number_of_samples())
            radian *= 0.925

        return fields.best_point

    class ExecuteFields:

        def __init__(self, point, result):
            self.best_point = point
            self.best_result = result
            self.task_index = 0
