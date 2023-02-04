import re
from .tokens import Token, TokenTypes


class Lexer:
    def __init__(self, code: str) -> None:
        begin_endlines = re.search("^\n+", code)
        if begin_endlines:
            self.line = begin_endlines.end() + 1
        else:
            self.line = 1
        
        self.code = code.strip() + '\n'
        self.pos = 0
        self.line_pos = 0
        self.tokens: list[Token] = []

    def analyze(self) -> list[Token]:
        while (self.next_token()):
            pass
        return self.tokens.copy()

    def next_token(self) -> bool:
        if self.pos >= len(self.code):
            return False

        for type_ in TokenTypes.values():
            found = re.search(type_.regex, self.code[self.pos:])

            if found:
                text = found.group(0)

                is_endline = type_ == TokenTypes.ENDLINE
                endline_flag = (
                    not len(self.tokens)
                    or
                    (
                        not is_endline
                        or
                        self.tokens[-1].type != TokenTypes.ENDLINE
                    )
                )

                if type_ != TokenTypes.SPACE and endline_flag:
                    self.tokens.append(Token(
                        type_,
                        text,
                        self.line,
                        self.line_pos,
                    ))

                text_len = len(text)
                self.pos += text_len

                if is_endline:
                    self.line += 1
                    self.line_pos = 0
                else:
                    self.line_pos += text_len

                return True

        raise Exception((
            f"[{self.line}:{self.line_pos}] unkown token "
            f"near `{self.code[self.pos]}`"
        ))
