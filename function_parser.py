import re
from iterator import forEach


class FunctionParser:
    def __init__(self):
        self.symbols = (
            ('^',),
            ('*', '/'),
            ('+', '-'),
            ('<', '>', '<=', '>='),
        )
        self.functions = (
            'sin',
            'cos',
            'tg',
            'ctg'
        )

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
                    in which first element is function and rest of them are function arguments"""

        result = expression[:]
        for index, item in enumerate(result):
            # remove empty elements
            if item == '':
                result.remove(item)

            # join functions' braces to functions
            for f in self.functions:
                if item == f:
                    result[index] = [result[index], result[index + 1]]
                    del result[index+1]
                    index -= 1

        print("Before")
        for a, b in enumerate(result):
            print(a, ": ", b)
        for symbol in self.symbols:
            for index, item in enumerate(result):
                if item in symbol:
                    for a, b in enumerate(result):
                        print(a, ": ", b)
                    result[index-1] = [result[index], result[index - 1], result[index + 1]]
                    for a, b in enumerate(result):
                        print(a, ": ", b)
                    del result[index]
                    for a, b in enumerate(result):
                        print(a, ": ", b)
                    del result[index]
                    for a, b in enumerate(result):
                        print(a, ": ", b)
                    index += 3

        return result

    def parse(self, expression):
        result = self.remove_spaces(expression)
        # make sure result is list
        if type(result) is not list:
            result = [result]

        result = re.split(re.compile("([^a-zA-Z0-9.])"), expression)
        result = self.remove_empty_elements(result)
        result = self.remove_braces(result)
        result = forEach(result, self.join)
        return result


if __name__ == "__main__":
    parser = FunctionParser()
    test_data = (
        "3+(4+(4-23)+23) < x^2",
        "x+3<  100",
        "x^2 + 3*x + (4 + x*8) * x <= 100",
        "x^3+x<99",
        "sin(x)<0.6"
    )

    for data in test_data:
        print(data + "  ->  ")
        print(parser.parse(data))
