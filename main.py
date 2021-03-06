from reader import Reader
from parsing import Parser
from nfa import NFA


def main():
    string = 'a|b'
    reader = Reader(string)
    tokens = reader.CreateTokens()
    parser = Parser(tokens)
    tree = parser.Parse()
    _nfa = NFA(tree)

    print(f'''
            tokens: {list(Reader(string).CreateTokens())}
            parsed tree: {tree}
            ''')

# while True:
#     string = input('Type an expression to evaluate: ')
#     if string == 'exit':
#         break

#     reader = Reader(string)
#     tokens = reader.CreateTokens()
#     parser = Parser(tokens)
#     tree = parser.Parse()
#     # interpreter = Interpreter()

#     print(f'''
#             tokens: {list(Reader(string).CreateTokens())}
#             parsed tree: {tree}
#             ''')

# exit(1)


if __name__ == "__main__":
    main()
