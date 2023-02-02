from __future__ import annotations


class TokenTag:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, __o: TokenTag) -> bool:
        return self.name == __o.name

    def __ne__(self, __o: TokenTag) -> bool:
        return self.name != __o.name

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


class TokenTags:
    STARTLINE = TokenTag("STARTLINE")
    ENDLINE = TokenTag("ENDLINE")
    VARIABLE = TokenTag("VARIABLE")
    NUMBER = TokenTag("NUMBER")
    OPERAND = TokenTag("OPERAND")
    BINARY = TokenTag("BINARY")
    LCURLY = TokenTag("LCURLY")
    RCURLY = TokenTag("RCURLY")
    LROUND = TokenTag("LROUND")
    RROUND = TokenTag("RROUND")
