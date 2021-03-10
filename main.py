from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA

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

# string = input('Regular expression: ')
string = 'a*|b'
print(string)
reader = Reader(string)
tokens = reader.CreateTokens()
print(list(Reader(string).CreateTokens()))
parser = Parser(tokens)
tree = parser.Parse()

print(f'''
        tokens: {list(Reader(string).CreateTokens())}
        parsed tree: {tree}
        symbols: {reader.GetSymbols()}
        ''')

# NFA
_nfa = NFA(tree, reader.GetSymbols())
_nfa.Render(tree)
_nfa.GetFinalStates()
_nfa.WriteNFADiagram()

trans_table = _nfa.GetTransitionTable()
total_states = _nfa.GetFinalStates()
symbols = _nfa.symbols

# DFA
_dfa = DFA(trans_table, symbols, total_states)
_dfa.TransformNFAToDFA()
