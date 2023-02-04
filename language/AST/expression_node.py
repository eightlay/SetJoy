from abc import ABC, abstractproperty

from ..tokens import TokenTags


class ExpressionNode(ABC):
    @abstractproperty
    def extensions(self) -> set[TokenTags]:
        return set()

    def is_variable(self) -> bool:
        return False