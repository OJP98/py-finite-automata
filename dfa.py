from pprint import pprint
from pythomata import SimpleDFA
from graphviz import Digraph
from utils import WriteToFile

STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DFA:
    def __init__(self, trans_table, symbols, states, final_dfa_state):
        self.trans_table = trans_table
        self.symbols = symbols
        self.final_dfa_state = final_dfa_state
        self.table = dict()
        self.states = dict()
        self.accepting_states = list()
        self.nodes = []
        self.iterations = 0

        try:
            self.symbols.remove('e')
        except:
            pass

    def MoveTo(self, node_id, eval_symbol='e', array=[], add_initial=False, move_once=False):

        arr = array
        node = self.nodes[node_id]
        if not node.visited and eval_symbol in node.next_states:
            node.Mark()
            next_states = [int(s) for s in node.next_states[eval_symbol]]
            if eval_symbol == 'e':
                arr = [*next_states]
            else:
                arr = [*next_states]

            if add_initial:
                arr = [*next_states, node_id]

            if not move_once:
                for new_node_id in node.next_states[eval_symbol]:
                    arr += [*self.MoveTo(int(new_node_id), eval_symbol, arr)]

        return list(set(arr))

    def EvaluateClosure(self, closure, node, symbols, curr_state):

        if not closure:
            closure = self.MoveTo(0, add_initial=True)
            closure.append(0)
            self.states[curr_state] = closure
            if self.final_dfa_state in closure:
                self.accepting_states.append(curr_state)

        print(closure)
        print(self.states)
        for symbol in symbols:
            symbol_closure = list()
            new_set = list()

            for value in closure:
                symbol_closure += self.MoveTo(value, symbol, move_once=True)
                [node.UnMark() for node in self.nodes]

            if symbol_closure:
                e_closure = list()
                for e_value in symbol_closure:
                    e_closure += self.MoveTo(e_value)
                    [node.UnMark() for node in self.nodes]

                new_set += list(set([*symbol_closure, *e_closure]))
                # print(f'en el estado {curr_state}, {symbol} generó {new_set}')

                if not new_set in self.states.values():
                    # print(f'{symbol} creó UN NUEVO ESTADO')
                    self.iterations += 1
                    new_state = STATES[self.iterations]

                    try:
                        curr_dict = self.table[curr_state]
                        curr_dict[symbol] = new_state
                    except:
                        self.table[curr_state] = {symbol: new_state}

                    try:
                        self.table[new_state]
                    except:
                        self.table[new_state] = {}

                    self.states[new_state] = new_set

                    if self.final_dfa_state in new_set:
                        self.accepting_states.append(new_state)

                    self.EvaluateClosure(
                        new_set, value, symbols, new_state)

                else:
                    for S, V in self.states.items():
                        if new_set == V:

                            try:
                                curr_dict = self.table[curr_state]
                            except:
                                self.table[curr_state] = {}
                                curr_dict = self.table[curr_state]

                            curr_dict[symbol] = S
                            self.table[curr_state] = curr_dict

    def GetDStates(self):
        for state, values in self.trans_table.items():
            self.nodes.append(Node(int(state), values))

    def TransformNFAToDFA(self):
        self.GetDStates()
        self.EvaluateClosure([], 0, self.symbols, 'A')
        pprint(self.states)
        pprint(self.table)

    def GraphDFA(self):
        states = set(self.table.keys())
        alphabet = set(self.symbols)
        initial_state = 'A'

        dfa = SimpleDFA(states, alphabet, initial_state,
                        set(self.accepting_states), self.table)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DFA.gv', source)
        graph.render('./output/DFA.gv', view=True)


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
