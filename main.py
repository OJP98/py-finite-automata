from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from test import DirectReader

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

if __name__ == "__main__":
    string = '(a|b)*abb'
    print(string)
    # reader = Reader(string)
    reader = DirectReader(string)
    tokens = reader.CreateTokens()
    parser = Parser(tokens)
    tree = parser.Parse()

    print(f'''
            tokens: {list(Reader(string).CreateTokens())}
            parsed tree: {tree}
            symbols: {reader.GetSymbols()}
            ''')

    ddfa = DDFA(tree)


# # NFA
# _nfa = NFA(tree, reader.GetSymbols())
# _nfa.Render(tree)
# final_states = _nfa.GetFinalStates()
# _nfa.WriteNFADiagram()

# trans_table = _nfa.GetTransitionTable()
# total_states = _nfa.GetFinalStates()
# symbols = _nfa.symbols

# # DFA
# _dfa = DFA(trans_table, symbols, total_states, final_states)
# _dfa.TransformNFAToDFA()
# _dfa.GraphDFA()
