import sys
from io import StringIO

from .lexer import Lexer
from .parser import Parser


class Interpreter:
    def __init__(self) -> None:
        print("SetJoy\n(c) Timur Dzhalalov (github.com/eightlay)\nЯзык программирования для манипулирования множествами")

    def run(self) -> None:
        python3 = sys.stdout

        while True:
            code = input('>>> ')

            try:
                lexer = Lexer(code)
                parser = Parser(lexer)
                tree = parser.parse_code()

                for line in tree:
                    sys.stdout = setjoy = StringIO()
                    exec(str(line))
                    sys.stdout = python3
                    val = setjoy.getvalue()
                    print(val.replace(',', ''), end='')
            except Exception as e:
                print(e)
