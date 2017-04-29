from function_parser import FunctionParser as Parser
from executor import Executor


class Interpreter:
    def __init__(self):
        self.commands = {
            'help': self.print_help,
        }

    def print_help(self, args):
        for cmds in self.commands.keys():
            print(cmds + "\n")

    @staticmethod
    def unknown_command(command):
        print("Unknown command: " + command)

    @staticmethod
    def wrong_number():
        print("Wrong number of arguments.\n")

    def execute(self, args):
        pass

    def add(self, args):
        pass

    def execute(self, cmd):
        cmd = cmd.split(' ', 1)
        args = []
        try:
            args = cmd[1].split
            self.commands.get(cmd[0])(*args)
        except IndexError:
            return


if __name__ == "__main__":
    interpreter = Interpreter()
    parser = Parser()
    executor = Executor()
    while True:
        print("\n> ", end="")
        cmd = input()
        interpreter.execute(cmd)
