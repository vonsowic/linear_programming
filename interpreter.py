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
            'execute': self.executor.execute,
            'clear': self.executor.clear,
            'show': self.show,
            'help': self.print_help,
            'exit': exit,
        }

    def print_help(self):
        for command in self.commands.keys():
            print(command)

    def show(self):
        print("Equations:")
        for index, item in enumerate(self.executor.equations):
            print(index, ':', item)
        print("End function:", self.executor.end_function)
        print("Epsilon:", self.executor.epsilon)

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
    while True:
        print("\n> ", end="")
        cmd = input()
        interpreter.execute(cmd)
