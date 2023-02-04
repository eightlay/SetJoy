from typing import Iterable

from .AST import *
from .lexer import Lexer
from .tokens import Token, TokenTypes, TokenTag, TokenTags, TagsPairs


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.tokens = lexer.analyze()
        self.pos = 0
        self.line = 1
        self.stack: list[ExpressionNode] = []
        self.root = StatementsNode()

    def parse_code(self) -> StatementsNode:
        while self.pos < len(self.tokens):
            line = self.parse_line()
            self.add_line(line)
            self.clear_stack()
        return self.root

    def add_line(self, line: ExpressionNode) -> None:
        self.root.add_node(line)
        self.pos += 1
        self.line += 1

    def clear_stack(self) -> None:
        self.stack.clear()

    def parse_line(
        self,
        line_starts: set[TokenTag] = set([TokenTags.STARTLINE]),
        line_end: TokenTag = TokenTags.ENDLINE,
        add_extensions: set[TokenTags] = set(),
    ) -> ExpressionNode:
        while self.parse_token(line_starts, line_end, add_extensions):
            line_starts |= self.stack[-1].extensions
        return self.stack.pop()

    def parse_token(
        self,
        line_starts: set[TokenTag] = set([TokenTags.STARTLINE]),
        line_end: TokenTag = TokenTags.ENDLINE,
        add_extensions: set[TokenTags] = set(),
    ) -> bool:
        token, tag = self.match_tags(line_starts | add_extensions)

        if tag is None:
            token, _ = self.match_tags()
            raise Exception(f"{token.pos} unexpected token `{token.text}`")

        if TokenTags.VARIABLE in token.tags:
            line_starts = self.handle_variable(token)
        elif TokenTags.NUMBER in token.tags:
            line_starts = self.handle_number(token)
        elif tag == TokenTags.BINARY:
            self.handle_binary(token, line_end, add_extensions)
        elif tag in (TokenTags.LROUND, TokenTags.LCURLY):
            self.handle_brace(token, tag, add_extensions)
        elif tag == line_end:
            return self.handle_endline()
        else:
            raise Exception(f"{token.pos} unexpected token `{token.text}`")
        return True

    def handle_variable(self, token: Token) -> set[TokenTags]:
        self.stack.append(VariableNode(token))
        return token.extensions

    def handle_number(self, token: Token) -> set[TokenTags]:
        self.stack.append(NumberNode(token))
        return token.extensions

    def handle_binary(
        self,
        token: Token,
        line_end: TokenTag,
        add_extensions: set[TokenTag],
    ) -> None:
        # TODO: правильный порядок создания дерева
        # Сейчас `A & B | C` станет `A & (B | C)`
        # Нужно `(A & B) | C`
        # NOTE: Приоритет бинарных операций или на следуюзем этапе?
        # Например, `A | B & C` должно остаться `A | (B | C)`
        ind = len(self.stack) - 1
        exts = token.extensions
        right_node = self.parse_line(exts, line_end, add_extensions)
        self.stack[ind] = BinaryNode(token, self.stack[ind], right_node)
        del self.stack[ind + 1:]

    def handle_brace(
        self,
        token: Token,
        tag: TokenTag,
        add_extensions: set[TokenTag],
    ) -> None:
        ind = len(self.stack) + 1
        self.stack.append(None)
        pair = TagsPairs[tag]
        last_node = self.parse_line(
            token.extensions,
            pair,
            add_extensions | token.add_extensions,
        )
        self.pos += 1

        sequence = SequenceNode(self.stack[ind:] + [last_node])
        del self.stack[ind:]

        if pair == TokenTags.RROUND:
            self.handle_round_brace(token, sequence)
        else:
            self.handle_curly_brace(sequence)

    def handle_round_brace(
        self,
        token: Token,
        sequence: SequenceNode,
    ) -> None:
        if self.stack[-2] is not None and self.stack[-2].is_variable():
            self.stack[-2] = UnaryNode(self.stack[-2], sequence)
            del self.stack[-1:]
        else:
            token = Token(TokenTypes.VARIABLE, "", token.line, token.pos)
            operator = VariableNode(token)
            self.stack[-1] = UnaryNode(operator, sequence)

    def handle_curly_brace(self, sequence: SequenceNode) -> None:
        self.stack[-1] = SetNode(sequence)

    def handle_endline(self) -> bool:
        self.pos -= 1
        return False

    def match_tags(
        self,
        expected: Iterable[TokenTag] = [],
    ) -> tuple[Token, TokenTag] | tuple[None, None]:
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            token_tags = token.tags

            if not len(expected):
                expected = token_tags

            chosen_tag = None

            for tag in expected:
                if tag in token_tags:
                    chosen_tag = tag
                    break

            if chosen_tag is not None:
                self.pos += 1
                return token, chosen_tag

        return None, None
