from . import TokenType, TokenTag


class Token:
    def __init__(
        self,
        type_: TokenType,
        text: str,
        line: int,
        line_pos: int,
    ) -> None:
        self.type = type_
        self.text = text.replace("\n", "\\n")
        self.line = line
        self.line_pos = line_pos
        
    @property
    def pos(self) -> str:
        return f"[{self.line}:{self.line_pos}]"

    @property
    def tags(self) -> set[TokenTag]:
        return self.type.tags

    @property
    def extensions(self) -> list[TokenTag]:
        return self.type.extensions

    @property
    def add_extensions(self) -> list[TokenTag]:
        return self.type.add_extensions

    def __repr__(self) -> str:
        return f"[{self.type.name}] ({self.pos}) {self.text}"
