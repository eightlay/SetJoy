from . import ExpressionNode
from .. import Token, TokenTags


class BinaryNode(ExpressionNode):
    def __init__(
        self,
        token: Token,
        left_node: ExpressionNode,
        right_node: ExpressionNode,
    ) -> None:
        super().__init__()
        self.operator = token
        self.left_node = left_node
        self.right_node = right_node

    @property
    def extensions(self) -> set[TokenTags]:
        return self.right_node.extensions

    def __repr__(self) -> str:
        return f"{self.left_node} {self.operator.text} {self.right_node}"
