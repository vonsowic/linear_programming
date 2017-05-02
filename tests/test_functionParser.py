from unittest import TestCase
from executor import Executor


class TestFunctionParser(TestCase):
    def test_parse(self):
        executor = Executor()
        parser = executor.parser
        parser.functions = executor.get_functions()

        test_data = (
            "((((((x+1))))+x2))",
            "(-1)*x1 + 3*x2 <= 12",
            "3+(4+(4-23)+23) <= x^2",
            "x+3<=  100",
            "x^2 + 3*x + (4 + x*8 + cos(x)) * x <= 100",
            # "x^2 + 3*x + 4 + x*8 * x <= 100",
            "x^3+x<=99",
            "sin(x)==0.6",
            "sin(x1)==0.6"
        )

        for data in test_data:
            print(data + "  ->  ")
            print(parser.parse(data))

