
from colorama import Fore, Style
from typing import Optional
import os
import sys


class Terminal:
    _instances = []

    def __init__(self):
        if len(Terminal._instances) != 0:
            return Terminal._instances[0]
        Terminal._instances.append(self)
        sys.excepthook = self._except_hook
        Terminal._global_error_handlers = {}

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def global_error_handler(self, error: Exception):
        def decorator(func):
            if not Terminal.error_handling:
                raise Exception(
                    'Terminal custom error handling is not enabled!')
            Terminal._global_error_handlers[error] = func

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _except_hook(self, exctype, value, traceback):
        for error, func in self._global_error_handlers.items():
            if exctype == error:
                func(value, traceback)
                return
        sys.__excepthook__(exctype, value, traceback)


class Choises:
    choisefuncs = {}

    def __init__(self, *functions: list[callable]):
        self.functions = functions

    def __str__(self):
        s = ''
        for i, f in enumerate(self.functions):
            s += f"{Fore.RED}[{Fore.YELLOW}{i+1}{Fore.RED}]{Style.RESET_ALL} {self.choisefuncs[f]}"
        return s + '\n'

    def choise_func(self, text: Optional[str] = None):
        if text:
            print(text)
        print(self)
        inp = input(f'{Fore.YELLOW} > {Style.RESET_ALL}')
        if not inp.isdigit():
            Terminal.clear()
            return self.choise_input(text)
        inp = int(inp)
        if inp < 1 or inp > len(self.functions):
            Terminal.clear()
            return self.choise_input(text)
        Terminal.clear()
        return self.functions[inp-1]

    @staticmethod
    def choise_input(choises: list[str], text: Optional[str] = None):
        Terminal.clear()
        if text:
            print(text)
        for i, c in enumerate(choises):
            print(
                f'{Fore.RED}[{Fore.YELLOW}{i+1}{Fore.RED}]{Style.RESET_ALL} {c}')
        inp = input(f'{Fore.YELLOW} > {Style.RESET_ALL}')
        if not inp.isdigit():
            Terminal.clear()
            return Choises.choise_input(choises, text)
        inp = int(inp)
        if inp < 1 or inp > len(choises):
            Terminal.clear()
            return Choises.choise_input(choises, text)
        Terminal.clear()
        return inp-1

    @classmethod
    def choise(cls, *, name: Optional[str] = None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if name:
                    cls.choisefuncs[func] = name
                else:
                    cls.choisefuncs[func] = func.__name__
                return func(*args, **kwargs)
            return wrapper
        return decorator
