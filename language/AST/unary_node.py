from . import ExpressionNode
from .. import TokenTags


class UnaryNode(ExpressionNode):
    def __init__(
        self,
        operator: ExpressionNode,
        operand: ExpressionNode,
    ) -> None:
        super().__init__()
        self.operator = operator
        self.operand = operand

    @property
    def extensions(self) -> set[TokenTags]:
        return self.operand.extensions

    def __repr__(self) -> str:
        return f"{self.operator}({self.operand})"
