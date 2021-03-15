from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader

if __name__ == "__main__":
    string = 'abb(a|b)*'
    regex = 'abbab'
    print('EXPRESIÓN:', string)
    reader = Reader(string)
    tokens = reader.CreateTokens()
    parser = Parser(tokens)
    tree = parser.Parse()

    print(f'''
            Parsed tree: {tree}
            ''')

#     ddfa = DDFA(tree, reader.GetSymbols())
#     ddfa.GraphDFA()

    # NFA
    _nfa = NFA(tree, reader.GetSymbols(), regex)
    _nfa.WriteNFADiagram()
    nfa_regex = _nfa.EvalRegex()
    print(nfa_regex)

    # DFA
    # _dfa = DFA(_nfa.trans_func, _nfa.symbols,
    #            _nfa.curr_state, _nfa.final_states)

    # _dfa.TransformNFAToDFA()
    # _dfa.GraphDFA()

    # DIRECT DFA
    # reader = DirectReader(string)
    # tokens = reader.CreateTokens()
    # parser = Parser(tokens)
    # tree = parser.Parse()
    # ddfa = DDFA(tree, reader.GetSymbols())
    # ddfa.GraphDFA()
