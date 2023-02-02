from . import ExpressionNode
from .. import TokenTags


class SequenceNode(ExpressionNode):
    def __init__(
        self,
        sequence: list[ExpressionNode],
    ) -> None:
        super().__init__()
        if not len(sequence):
            raise Exception("sequences with no elements are not allowed")
        self.sequence = sequence

    @property
    def extensions(self) -> set[TokenTags]:
        return self.sequence[-1].extensions

    def add(self, node: ExpressionNode) -> None:
        self.sequence.append(node)

    def __repr__(self) -> str:
        return (
            f"{self.sequence}"
            .replace("[", "")
            .replace("]", "")
            .replace(",", "")
        )
