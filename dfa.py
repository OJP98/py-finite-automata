from pprint import pprint

STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DFA:
    def __init__(self, trans_func, symbols, states):
        self.trans_func = trans_func
        self.symbols = symbols
        self.states = states

    def Move(self, init_state, transitions, eval_symbol):
        _set = self.trans_func[init_state]

        for symbol, next_states in transitions.items():
            for state in next_states:
                # if there's an epsilon in the next iterated state
                if eval_symbol in self.trans_func[state]:
                    new = self.trans_func[state][eval_symbol]
                    _set[symbol] += new

        return list(set(_set[eval_symbol]))

    def TransformNFAToDFA(self):
        pprint(self.trans_func)
        eclosure = self.Move('2', self.trans_func['2'], 'a')
        print(eclosure)
        # for s in range(self.states):
