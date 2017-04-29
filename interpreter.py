from executor import Executor
from sys import exit


class Interpreter:
    def __init__(self):
        self.executor = Executor()
        self.commands = {
            'add': self.executor.add,
            'del': self.executor.remove,
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
        for index, item in enumerate(self.executor.equations):
            print(index, ':', item)

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
            args.append(command[1])
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
