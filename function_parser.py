import re
from iterator import forEach


class FunctionParser:
    def __init__(self):
        self.symbols = (
            ('^',),
            ('*', '/', '%'),
            ('+', '-'),
            ('<', '>', '<=', '>=', '==', '!='),
        )
        self.functions = []

    @staticmethod
    def remove_spaces(expression):
        return ''.join(expression.split(' '))

    @staticmethod
    def remove_braces(expression):
        result = expression[:]

        if ')' not in expression:
            return result

        start_x, end_x, x = 0, 0, 0
        again = True
        while again and x < len(result):
            if result[x] == ')':
                end_x = x
                again = False
            if result[x] == '(':
                start_x = x
            x += 1

        result[start_x] = result[start_x + 1:end_x]

        # delete unnecessary elements
        for x in range(start_x + 1, end_x + 1):
            del result[start_x + 1]

        if '(' in result:
            return FunctionParser.remove_braces(result)
        else:
            return result

    @staticmethod
    def remove_empty_elements(iterable):
        return [x for x in iterable if x != '' and x != ' ']

    def join(self, expression):
        u""":param expression is string representing equation
            :return list of list of list (and so on) of expression,
                    where the deepest list represent equation,
                    in which first element is function and second is list with function arguments"""

        result = expression[:]

        for index, item in enumerate(result):
            if type(item) is list:
                result[index] = self.join(item)

            # pack function arguments with function
            for f in self.functions:
                if item == f:
                    result[index] = [result[index], result[index + 1]]
                    del result[index + 1]
                    index -= 1

        for symbol in self.symbols:
            for index, item in enumerate(result):
                if item in symbol:
                    result[index - 1] = [result[index], [result[index - 1], result[index + 1]]]
                    del result[index]
                    del result[index]
                    index -= 2

        return result

    def parse(self, expression):
        result = self.remove_spaces(expression)
        result = re.split(re.compile("([^a-zA-Z0-9.])"), result)

        # make sure result is list
        if type(result) is not list:
            result = [result]

        result = self.remove_empty_elements(result)
        result = self.parse_inequalities(result)
        result = self.remove_braces(result)
        result = self.join(result)
        result = self.remove_surplus_lists(result)
        return result

    @staticmethod
    def parse_inequalities(expression):
        result = expression[:]
        for i in range(len(result)-1, -1, -1):
            if result[i] is '=':
                result[i] = result[i-1]+result[i]
                del result[i-1]
                return result
        return result

    def remove_surplus_lists(self, expression):
        if type(expression) is list:
            if len(expression) is 1:
                if type(expression[0]) is list:
                    if len(expression[0]) is 1:
                        return self.remove_surplus_lists(expression[0])
                    else:
                        return expression[0]

        return expression

    def get_operators(self):
        result = []
        for i in self.symbols:
            result.extend(i)
        return result
