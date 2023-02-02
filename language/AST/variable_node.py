from . import ExpressionNode
from .. import Token, TokenTags


class VariableNode(ExpressionNode):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.variable = token

    @property
    def extensions(self) -> set[TokenTags]:
        return self.variable.extensions

    def is_variable(self) -> bool:
        return True

    def __repr__(self) -> str:
        return self.variable.text
    