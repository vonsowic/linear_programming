from executor import Executor
from sys import exit
from function_parser import FunctionParser as Parser


class Interpreter:
    def __init__(self):
        self.executor = Executor()
        self.commands = {
            'add': self.executor.add,
            'end': self.executor.set_end_function,
            'epsilon': self.executor.set_epsilon,
            'del': self.executor.remove,
            'custom': self.executor.create_custom_function,
            'maximize': self.set_end_func_type,
            'multithreading': self.set_multi_threading_type,
            'execute': self.executor.execute,
            'clear': self.executor.clear,
            'show': self.show,
            'help': self.print_help,
            'exit': exit,
        }

    def set_end_func_type(self, boolean):
        self.executor.maximize = self.set_bool_type(boolean)

    def set_multi_threading_type(self, boolean):
        self.executor.multi_threading = self.set_bool_type(boolean)

    @staticmethod
    def set_bool_type(boolean):
        try:
            return bool(int(boolean))
        except ValueError:
            print("Type 1 for true or 0 for false")

    def print_help(self):
        print("Usage: <command> arg1 | arg2 | ...")
        print("Commands:")
        for command in self.commands.keys():
            print(" - ", command)

    def show(self):
        print("Equations:")
        for index, item in enumerate(self.executor.equations):
            print(index, ':', item)
        print("Maximize:", self.executor.maximize)
        print("End function:", self.executor.end_function)
        print("Epsilon:", self.executor.epsilon)
        print("Multi threading:", self.executor.multi_threading)

    @staticmethod
    def unknown_command(command):
        print("Unknown command:", command, ".Type 'help' for help.")

    @staticmethod
    def wrong_number():
        print("Wrong number of arguments.")

    def execute(self, command):
        command = command.split(' ', 1)
        args = []
        if len(command) is 2:
            command[1] = Parser.remove_spaces(command[1])
            args.extend(command[1].split('|'))

        command = command[0]

        try:
            self.commands[command](*args)
        except KeyError:
            print(self.unknown_command(command))
        except TypeError:
            print(self.wrong_number())


if __name__ == "__main__":
    interpreter = Interpreter()
    interpreter.execute("end 5*x1 + 4*x2 + 3*x3")
    interpreter.execute("add 2*x1 + 3*x2 + x3 <= 5")
    interpreter.execute("add 4*x1 + x2 + 2*x3 <= 11")
    interpreter.execute("add 3*x1 + 4*x2 + 2*x3 <= 8")
    interpreter.execute("add x1 >= 0")
    interpreter.execute("add x2 >= 0")
    interpreter.execute("add x3 >= 0")
    interpreter.execute("maximize 1")
    interpreter.execute("show")
    interpreter.execute("execute")
    while True:
        interpreter.execute(input("> "))
