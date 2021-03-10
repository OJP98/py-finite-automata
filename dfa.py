from pprint import pprint

STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DFA:
    def __init__(self, trans_table, symbols, states):
        self.trans_table = trans_table
        self.symbols = symbols
        self.states = states
        self.function = dict()
        self.states = dict()
        self.nodes = []

    def MoveTo(self, node_id, eval_symbol='e', array=[]):

        arr = array
        node = self.nodes[node_id]
        if not node.visited and eval_symbol in node.next_states:
            node.Mark()
            next_states = [int(s) for s in node.next_states[eval_symbol]]
            arr = [*next_states, node_id] if eval_symbol == 'e' else [*next_states]
            # arr = [*next_states, node_id]

            for new_node_id in node.next_states[eval_symbol]:
                arr += [*self.MoveTo(int(new_node_id), eval_symbol, arr)]

        return list(set(arr))

    def TransformNFAToDFA(self):

        for state, values in self.trans_table.items():
            self.nodes.append(Node(int(state), values))

        current_state = 0
        state = 0
        new_state = STATES[0]
        eclosure = self.MoveTo(0)
        [node.UnMark() for node in self.nodes]

        self.states[new_state] = eclosure
        pprint(self.states)

        for value in eclosure:
            for symbol in self.symbols:

                new_state = STATES[state]
                print(f'moviendo {value} con simbolo {symbol}')

                move_res = self.MoveTo(value, symbol)
                [node.UnMark() for node in self.nodes]

                closure = []
                print(move_res)
                for trans in move_res:
                    closure = self.MoveTo(trans)
                    [node.UnMark() for node in self.nodes]

                final_res = list(set([*move_res, *closure]))
                print(f'resultado: {final_res}')

                if final_res and final_res not in self.states.values():
                    state += 1
                    new_state = STATES[state]
                    self.states[new_state] = final_res

        pprint(self.states)


class Node:
    def __init__(self, num, next_states):
        self.num = num
        self.visited = False
        self.next_states = next_states

    def Mark(self):
        self.visited = True

    def UnMark(self):
        self.visited = False

    def __repr__(self):
        return f'{self.num} - {self.visited}: {self.next_states}'
