from reader import Reader
from parsing import Parser

while True:
    string = input('Type an expression to evaluate: ')
    if string == 'exit':
        break

    reader = Reader(string)
    tokens = reader.CreateTokens()
    parser = Parser(tokens)
    tree = parser.Parse()
    # interpreter = Interpreter()
    # res = interpreter.Calc(tree)

    print(f'''
            tokens: {list(Reader(string).CreateTokens())}
            parsed tree: {tree}
            ''')

exit(1)
