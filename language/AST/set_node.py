from . import ExpressionNode
from ..tokens import TokenTags


class SetNode(ExpressionNode):
    def __init__(
        self,
        sequence: ExpressionNode,
    ) -> None:
        super().__init__()
        self.sequence = sequence

    @property
    def extensions(self) -> set[TokenTags]:
        return self.sequence.extensions

    def __repr__(self) -> str:
        return f"{{{self.sequence}}}"
