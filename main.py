from pprint import pprint

from language import Lexer, Parser


code = """
a = {{1} 2}
a = {(1 2) 3 | 4 & {5 4}}


"""


def main():
    lexer = Lexer(code)
    tokens = lexer.analyze()
    parser = Parser(tokens)
    ast = parser.parse_code()
    pprint(ast)
    

if __name__ == "__main__":
    main()
