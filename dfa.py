from pprint import pprint
from pythomata import SimpleDFA
from graphviz import Digraph
from utils import WriteToFile

STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DFA:
    def __init__(self, trans_table, symbols, states, final_nfa_state, regex):

        # Proveniente del NFA
        self.trans_table = trans_table
        self.final_nfa_state = final_nfa_state

        # Propiedades de un AF
        self.symbols = symbols
        self.trans_func = dict()
        self.states = dict()
        self.accepting_states = list()
        self.initial_state = 'A'

        try:
            self.symbols.remove('e')
        except:
            pass

        self.nodes = []
        self.iterations = 0
        self.regex = regex

    def MoveTo(self, node_id, eval_symbol='e', array=[], add_initial=False, move_once=False):

        arr = array
        node = self.nodes[node_id]
        # Recorremos el nodo si no está visitado
        if not node.visited and eval_symbol in node.next_states:

            # Marcamos el nodo
            node.Mark()
            # Obtenemos los siguientes estados
            next_states = [int(s) for s in node.next_states[eval_symbol]]
            if eval_symbol == 'e':
                arr = [*next_states]
            else:
                arr = [*next_states]

            # ¿Tenemos que agregar el nodo inicial?
            if add_initial:
                arr = [*next_states, node_id]

            # Si tenemos que movernos varias veces, habrá que hacerlo de forma recursiva
            if not move_once:
                for new_node_id in node.next_states[eval_symbol]:
                    arr += [*self.MoveTo(int(new_node_id), eval_symbol, arr)]

        return list(set(arr))

    def EvaluateClosure(self, closure, node,  curr_state):

        # Estado inicial no creado?
        if not closure:
            closure = self.MoveTo(0, add_initial=True)
            closure.append(0)
            self.states[curr_state] = closure
            if self.final_nfa_state in closure:
                self.accepting_states.append(curr_state)

        # Por cada símbolo dentro del set...
        for symbol in self.symbols:
            symbol_closure = list()
            new_set = list()

            # Clausura con el símbolo y el estado
            for value in closure:
                symbol_closure += self.MoveTo(value, symbol, move_once=True)
                [node.UnMark() for node in self.nodes]

            # Clausura con epsilon y el estado
            if symbol_closure:
                e_closure = list()
                for e_value in symbol_closure:
                    e_closure += self.MoveTo(e_value)
                    [node.UnMark() for node in self.nodes]

                new_set += list(set([*symbol_closure, *e_closure]))

                # Si este nuevo estado no existe es nuevo...
                if not new_set in self.states.values():
                    self.iterations += 1
                    new_state = STATES[self.iterations]

                    # Se crea la entrada en la función de transición
                    try:
                        curr_dict = self.trans_func[curr_state]
                        curr_dict[symbol] = new_state
                    except:
                        self.trans_func[curr_state] = {symbol: new_state}

                    try:
                        self.trans_func[new_state]
                    except:
                        self.trans_func[new_state] = {}

                    # Se agrega dicha entrada
                    self.states[new_state] = new_set

                    # Si posee el estado final del AFN, entonces agregarlo al set
                    if self.final_nfa_state in new_set:
                        self.accepting_states.append(new_state)

                    # Repetir con el nuevo set
                    self.EvaluateClosure(new_set, value, new_state)

                # Este estado ya existe, se agrega la transición.
                else:
                    for S, V in self.states.items():
                        if new_set == V:

                            try:
                                curr_dict = self.trans_func[curr_state]
                            except:
                                self.trans_func[curr_state] = {}
                                curr_dict = self.trans_func[curr_state]

                            curr_dict[symbol] = S
                            self.trans_func[curr_state] = curr_dict
                            break

    def EvalRegex(self):
        curr_state = 'A'

        for symbol in self.regex:
            # El símbolo no está dentro del set
            if not symbol in self.symbols:
                return 'No'
            # Intentamos hacer una transición a un nuevo estado
            try:
                curr_state = self.trans_func[curr_state][symbol]
            except:
                # Volvemos al inicio y verificamos que sea un estado de aceptacion
                if curr_state in self.accepting_states and symbol in self.trans_func['A']:
                    curr_state = self.trans_func['A'][symbol]
                else:
                    return 'No'

        return 'Yes' if curr_state in self.accepting_states else 'No'

    def GetDStates(self):
        for state, values in self.trans_table.items():
            self.nodes.append(Node(int(state), values))

    def TransformNFAToDFA(self):
        self.GetDStates()
        self.EvaluateClosure([], 0, 'A')

    def GraphDFA(self):
        states = set(self.trans_func.keys())
        alphabet = set(self.symbols)
        initial_state = 'A'

        dfa = SimpleDFA(states, alphabet, initial_state,
                        set(self.accepting_states), self.trans_func)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DFA.gv', source)
        graph.render('./output/DFA.gv', format='pdf', view=True)


class Node:
    def __init__(self, state, next_states):
        self.state = state
        self.visited = False
        self.next_states = next_states

    def Mark(self):
        self.visited = True

    def UnMark(self):
        self.visited = False

    def __repr__(self):
        return f'{self.state} - {self.visited}: {self.next_states}'
