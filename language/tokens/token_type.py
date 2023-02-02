from __future__ import annotations
import re
from typing import Iterator

from . import TokenTag, TokenTags


class TokenType:
    def __init__(
        self,
        name: str,
        regex: str,
        tags: set[TokenTag],
        extensions: set[TokenTag],
        add_extensions: set[TokenTags] = set(),
    ) -> None:
        self.name = name
        self.regex = re.compile('^' + regex)
        self.tags = tags
        self.extensions = extensions.copy()
        self.add_extensions = add_extensions.copy()

    def __eq__(self, __o: TokenType) -> bool:
        return self.name == __o.name

    def __ne__(self, __o: TokenType) -> bool:
        return self.name != __o.name

    def __repr__(self) -> str:
        return self.name


class TokenTypes:
    ENDLINE = TokenType(
        name="ENDLINE",
        regex="\n",
        tags={TokenTags.ENDLINE},
        extensions={},
    )
    NUMBER = TokenType(
        name="NUMBER",
        regex="[0-9]+",
        tags={TokenTags.NUMBER, TokenTags.OPERAND},
        extensions={
            TokenTags.ENDLINE, TokenTags.BINARY,
            TokenTags.RROUND, TokenTags.RCURLY,
        },
    )
    VARIABLE = TokenType(
        name="VARIABLE",
        regex="[a-zA-Z][a-zA-Z1-9_]*",
        tags={
            TokenTags.VARIABLE, TokenTags.STARTLINE,
            TokenTags.OPERAND,
        },
        extensions={
            TokenTags.ENDLINE, TokenTags.BINARY,
            TokenTags.LROUND, TokenTags.RROUND,
            TokenTags.RCURLY,
        },
    )
    SPACE = TokenType(
        name="SPACE",
        regex="[ \t\r]+",
        tags={},
        extensions={},
    )
    ASSIGN = TokenType(
        name="ASSIGN",
        regex="=",
        tags={TokenTags.BINARY},
        extensions={TokenTags.OPERAND, TokenTags.LROUND, TokenTags.LCURLY},
    )
    LCURLY = TokenType(
        name="LCURLY",
        regex="{",
        tags={TokenTags.LCURLY},
        extensions={TokenTags.OPERAND, TokenTags.LROUND, TokenTags.LCURLY},
        add_extensions={
            TokenTags.NUMBER,
            TokenTags.VARIABLE,
            TokenTags.LROUND,
        }
    )
    RCURLY = TokenType(
        name="RCURLY",
        regex="}",
        tags={TokenTags.RCURLY},
        extensions={TokenTags.ENDLINE, TokenTags.BINARY, TokenTags.RROUND},
    )
    LROUND = TokenType(
        name="LROUND",
        regex="\(",
        tags={TokenTags.LROUND},
        extensions={
            TokenTags.OPERAND, TokenTags.LROUND,
            TokenTags.LCURLY,
        },
        add_extensions={
            TokenTags.NUMBER,
            TokenTags.VARIABLE,
            TokenTags.LROUND,
        },
    )
    RROUND = TokenType(
        name="RROUND",
        regex="\)",
        tags={TokenTags.RROUND},
        extensions={
            TokenTags.ENDLINE, TokenTags.BINARY,
            TokenTags.LROUND, TokenTags.RROUND,
            TokenTags.RCURLY,
        },
    )
    UNION = TokenType(
        name="UNION",
        regex="\|",
        tags={TokenTags.BINARY},
        extensions={TokenTags.OPERAND, TokenTags.LROUND, TokenTags.LCURLY},
    )
    INTERSECTION = TokenType(
        name="INTERSECTION",
        regex="\&",
        tags={TokenTags.BINARY},
        extensions={TokenTags.OPERAND, TokenTags.LROUND, TokenTags.LCURLY},
    )

    @classmethod
    def values(cls) -> Iterator[TokenType]:
        return iter(
            v
            for k, v in cls.__dict__.items()
            if not k.startswith("_") and k != "values"
        )


TagsPairs = {
    TokenTags.LCURLY: TokenTypes.RCURLY,
    TokenTags.LROUND: TokenTypes.RROUND,
}
