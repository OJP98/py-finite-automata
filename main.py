from reader import Reader
from parsing import Parser
from nfa import NFADiagram, NFA

# if __name__ == "__main__":

#     while True:
#         string = input('Type an expression to evaluate: ')
#         if string == 'exit':
#             break

#         reader = Reader(string)
#         tokens = reader.CreateTokens()
#         parser = Parser(tokens)
#         tree = parser.Parse()
#         _nfa = NFA(tree, reader.GetSymbols())

#         print(f'''
#                 tokens: {list(Reader(string).CreateTokens())}
#                 parsed tree: {tree}
#                 symbols: {reader.GetSymbols()}
#                 ''')

#         exit(1)

string = 'a'
reader = Reader(string)
tokens = reader.CreateTokens()
# list(tokens)
parser = Parser(tokens)
tree = parser.Parse()
_nfa = NFA(tree, reader.GetSymbols())
_nfa.Calc(tree)
_nfa.WriteNFADiagram()
print(f'''
        tokens: {list(Reader(string).CreateTokens())}
        parsed tree: {tree}
        symbols: {reader.GetSymbols()}
        ''')
