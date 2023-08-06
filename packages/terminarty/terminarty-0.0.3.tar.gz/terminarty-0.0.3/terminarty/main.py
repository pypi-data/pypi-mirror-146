from colorama import Fore, Style
from typing import Optional
import os
import sys


class InputDontMatchCheck(Exception):
    pass

class Terminal:
    _instances = []
    INPUT_STYLE = f'{Fore.YELLOW} > {Style.RESET_ALL}'

    def __init__(self) -> None:
        if len(Terminal._instances) != 0:
            raise RuntimeError('Only one instance of Terminal is allowed')
        Terminal._instances.append(self)
        sys.excepthook = self._except_hook
        self._global_error_handlers = {}

    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def input(text: str, *, check: callable = None) -> str:
        Terminal.clear()
        print(text)
        inp = input(Terminal.INPUT_STYLE)
        if check is not None:
            if not check(inp):
                raise InputDontMatchCheck(f'Input does not match check: {check.__name__}')
        Terminal.clear()
        return inp

    def global_error_handler(self, error: Exception) -> callable:
        def decorator(func):
            self._global_error_handlers[error] = func

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
    def choise(choises: list[str], text: Optional[str] = None) -> str:
        Terminal.clear()
        if text:
            print(text)
        for i, c in enumerate(choises):
            print(
                f'{Fore.RED}[{Fore.YELLOW}{i + 1}{Fore.RED}]{Style.RESET_ALL} {c}')
        inp = input(Terminal.INPUT_STYLE)
        if not inp.isdigit():
            Terminal.clear()
            return Choises.choise(choises, text)
        inp = int(inp)
        if inp < 1 or inp > len(choises):
            Terminal.clear()
            return Choises.choise(choises, text)
        Terminal.clear()
        return choises[inp - 1]
