
from typing import Optional
from colorama import Style

class BoxStyle:
    VERTICAL_LINE: str = ...
    HORIZONTAL_LINE: str = ...

    TOP_LEFT_CORNER: str = ...
    TOP_RIGHT_CORNER: str = ...
    BOTTOM_LEFT_CORNER: str = ...
    BOTTOM_RIGHT_CORNER: str = ...

    class Ascii:
        VERTICAL_LINE = '│'
        HORIZONTAL_LINE = '─'

        TOP_LEFT_CORNER = '*'
        TOP_RIGHT_CORNER = '*'
        BOTTOM_LEFT_CORNER = '*'
        BOTTOM_RIGHT_CORNER = '*'

    class Thin:
        VERTICAL_LINE = '│'
        HORIZONTAL_LINE = '─'

        TOP_LEFT_CORNER = '┌'
        TOP_RIGHT_CORNER = '┐'
        BOTTOM_LEFT_CORNER = '└'
        BOTTOM_RIGHT_CORNER = '┘'

    class Thick:
        VERTICAL_LINE = '┃'
        HORIZONTAL_LINE = '━'

        TOP_LEFT_CORNER = '┏'
        TOP_RIGHT_CORNER = '┓'
        BOTTOM_LEFT_CORNER = '┗'
        BOTTOM_RIGHT_CORNER = '┛'

    class Double:
        VERTICAL_LINE = '║'
        HORIZONTAL_LINE = '═'

        TOP_LEFT_CORNER = '╔'
        TOP_RIGHT_CORNER = '╗'
        BOTTOM_LEFT_CORNER = '╚'
        BOTTOM_RIGHT_CORNER = '╝'

    class Round:
        VERTICAL_LINE = '│'
        HORIZONTAL_LINE = '─'

        TOP_LEFT_CORNER = '╭'
        TOP_RIGHT_CORNER = '╮'
        BOTTOM_LEFT_CORNER = '╰'
        BOTTOM_RIGHT_CORNER = '╯'

class Box:
    def __init__(self,
                 text: str,
                 *,
                 style: Optional[BoxStyle] = BoxStyle.Thin,
                 color: Optional[str] = '',
                 ) -> None:
        self.text = text
        self.style = style
        self.color = color

    def __str__(self) -> str:
        VERTICAL_LINE = self.style.VERTICAL_LINE
        HORIZONTAL_LINE = self.style.HORIZONTAL_LINE
        TOP_LEFT_CORNER = self.style.TOP_LEFT_CORNER
        TOP_RIGHT_CORNER = self.style.TOP_RIGHT_CORNER
        BOTTOM_LEFT_CORNER = self.style.BOTTOM_LEFT_CORNER
        BOTTOM_RIGHT_CORNER = self.style.BOTTOM_RIGHT_CORNER

        text = self.text.splitlines()
        width = len(max(text, key=len))
        color = self.color

        box = [color + TOP_LEFT_CORNER + (HORIZONTAL_LINE * width) + TOP_RIGHT_CORNER]
        for line in text:
            box.append(color
                       + VERTICAL_LINE
                       + Style.RESET_ALL
                       + line
                       + color
                       + VERTICAL_LINE)
        box.append(color + BOTTOM_LEFT_CORNER + (HORIZONTAL_LINE * width) + BOTTOM_RIGHT_CORNER)

        return '\n'.join(box)