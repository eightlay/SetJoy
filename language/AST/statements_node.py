from typing import Iterator

from . import ExpressionNode
from ..tokens import TokenTags


class StatementsNode(ExpressionNode):
    def __init__(self) -> None:
        super().__init__()
        self.lines: list[ExpressionNode] = []

    @property
    def extensions(self) -> set[TokenTags]:
        if len(self.lines):
            return self.lines[-1].extensions
        return set()

    def add_node(self, node: ExpressionNode) -> None:
        self.lines.append(node)

    def __repr__(self) -> str:
        return str(self.lines)

    def __iter__(self) -> Iterator[ExpressionNode]:
        return iter(self.lines)
