from . import ExpressionNode
from ..tokens import Token, TokenTags


class NumberNode(ExpressionNode):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.number = token

    @property
    def extensions(self) -> set[TokenTags]:
        return self.number.extensions

    def __repr__(self) -> str:
        return self.number.text
