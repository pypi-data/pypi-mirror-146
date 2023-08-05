
from colorama import Fore, Style
from typing import Optional
import os
import sys

INPUT = f'{Fore.YELLOW} > {Style.RESET_ALL}'

class InputDontMatchCheck(Exception):
    pass

class Terminal:
    _instances = []

    def __init__(self) -> None:
        if len(Terminal._instances) != 0:
            return Terminal._instances[0]
        Terminal._instances.append(self)
        sys.excepthook = self._except_hook
        Terminal._global_error_handlers = {}

    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def input(text: str, *, check: callable[bool] = None) -> str:
        Terminal.clear()
        print(text)
        inp = input(INPUT)
        if check is not None:
            if not check(inp):
                raise InputDontMatchCheck(f'Input does not match check: {check.__name__}')
        return inp


    def global_error_handler(self, error: Exception) -> callable:
        def decorator(func):
            Terminal._global_error_handlers[error] = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _except_hook(self, exctype, value, traceback):
        for error, func in self._global_error_handlers.items():
            if exctype == error:
                func(error, value, traceback)
                return
        sys.__excepthook__(exctype, value, traceback)


class Choises:
    @staticmethod
    def choise(choises: list[str], text: Optional[str] = None) -> int:
        Terminal.clear()
        if text:
            print(text)
        for i, c in enumerate(choises):
            print(
                f'{Fore.RED}[{Fore.YELLOW}{i+1}{Fore.RED}]{Style.RESET_ALL} {c}')
        inp = input(INPUT)
        if not inp.isdigit():
            Terminal.clear()
            return Choises.choise_input(choises, text)
        inp = int(inp)
        if inp < 1 or inp > len(choises):
            Terminal.clear()
            return Choises.choise_input(choises, text)
        Terminal.clear()
        return inp-1
