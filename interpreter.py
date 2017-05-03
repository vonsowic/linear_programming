#!/usr/bin/env python

from executor import Executor
from sys import exit, argv
from function_parser import FunctionParser as Parser


class Interpreter:
    def __init__(self):
        self.executor = Executor()
        self.commands = {
            'add': self.executor.add,
            'end': self.executor.set_end_function,
            'epsilon': self.executor.set_epsilon,
            'radian': lambda radian: self.executor.set_radian(float(radian)),
            'range': lambda begging, end: self.executor.set_range(float(begging), float(end)),
            'del': self.executor.remove,
            'load': self.load,
            'custom': self.executor.create_custom_function,
            'maximize': self.set_end_func_type,
            'multithreading': self.set_multi_threading_type,
            'sizethreads': lambda size: self.executor.set_number_of_threads(int(size)),
            'execute': self.executor.execute,
            'calculate': self.executor.calculate,
            'clear': self.executor.clear,
            'show': self.show,
            'help': self.print_help,
            'exit': exit,
            '#': self.ignore,
            '': self.ignore,
        }

    def ignore(self, *args): pass

    def set_end_func_type(self, boolean): self.executor.maximize = self.set_bool_type(boolean)

    def set_multi_threading_type(self, boolean): self.executor.multi_threading = self.set_bool_type(boolean)

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
        print("Radian:", self.executor.radian)
        print("Epsilon:", self.executor.epsilon)
        print("Multi threading:", self.executor.multi_threading)

    @staticmethod
    def unknown_command(command): print("Unknown command: " + command + ". Type 'help' for help.")

    def load(self, filename):
        try:
            with open(filename) as file:
                for line in file.readlines():
                    self.execute(line.rstrip('\n'))
        except FileNotFoundError as e:
            print(str(e))

    def execute(self, command):
        command = command.split(' ', 1)
        args = []
        if len(command) is 2:
            command[1] = Parser.remove_spaces(command[1])
            args.extend(command[1].split('|'))

        command = command[0]

        result = None
        try:
            result = self.commands[command](*args)
        except KeyError:
            print(self.unknown_command(command))
        except TypeError as e:
            print(command + ": " + str(e))

        if result is not None:
            print(str(result))


if __name__ == "__main__":
    interpreter = Interpreter()

    for arg in argv[1:]:
        interpreter.execute("load " + arg)

    while True:
        interpreter.execute(input("> "))
