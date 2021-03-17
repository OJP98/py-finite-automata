from pythomata import SimpleDFA
from graphviz import Digraph
from utils import WriteToFile
from pprint import pprint

RAW_STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DDFA:
    def __init__(self, tree, symbols, regex):
        self.tree = tree
        self.symbols = symbols
        self.symbols.remove('e')
        self.nodes = list()
        self.states = list()
        self.table = dict()
        self.final_states = set()
        self.hash = None
        self.iter = 1
        self.regex = regex
        self.STATES = iter(RAW_STATES)

        self.ParseTree(self.tree)
        print('\nEL ÁRBOL DE SINTAXIS ES:')
        print(self.nodes)
        self.CalcFollowPos()

        print('\n ESTADOS:')
        pprint(self.states)

        print('\nFUNCIÓN DE TRANSICIÓN')
        pprint(self.table)

        print(self.nodes)
        print(self.final_states)

    def CalcFollowPos(self):
        # print(f'\nFOLLOWPOS EN EL ÁRBOL DE SINTAXIS')
        for node in self.nodes:
            if node.value == '*':
                for i in node.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.firstpos
                # print(
                    # '\tSe encuentra nodo * calcular followpos de los hijos')
            elif node.value == '.':
                for i in node.c1.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.c2.firstpos
                # print(
                    # '\tSe encuentra nodo ., calcular followpos de los hijos')

        # Initiate state generation
        initial_state = self.nodes[-1].firstpos
        # Filter the nodes that have a symbol
        self.nodes = list(filter(lambda x: x._id, self.nodes))
        self.hash = self.nodes[-1]._id

        # print('\nFOLLOWPOS FINAL:')
        # print(self.nodes)

        # print('\nGENERACIÓN DE ESTADOS')
        # Recursion
        self.CalcNewStates(initial_state, next(self.STATES))

    def CalcNewStates(self, state, curr_state):

        if not self.states:
            self.states.append(set(state))
            if self.hash in state:
                self.final_states.update(curr_state)

        # print('\tEN EL ESTADO', state)
        for symbol in self.symbols:

            # Get all the nodes with the same symbol in followpos
            same_symbols = list(
                filter(lambda x: x.value == symbol and x._id in state, self.nodes))

            # Create a new state with the nodes
            new_state = set()
            for node in same_symbols:
                new_state.update(node.followpos)

            print(f'\t{state} -> {symbol} -> {new_state}')
            # new state is not in the state list
            if new_state not in self.states and new_state:

                self.states.append(new_state)
                next_state = next(self.STATES)

                try:
                    self.table[next_state]
                except:
                    self.table[next_state] = dict()

                try:
                    existing_states = self.table[curr_state]
                except:
                    self.table[curr_state] = dict()
                    existing_states = self.table[curr_state]

                existing_states[symbol] = next_state
                self.table[curr_state] = existing_states

                if self.hash in new_state:
                    self.final_states.update(next_state)

                # print(
                #     f'\t{new_state} es un estado nuevo, se iterará por cada símbolo\n')
                self.CalcNewStates(new_state, next_state)

            elif new_state:
                for i in range(0, len(self.states)):

                    if self.states[i] == new_state:
                        state_ref = RAW_STATES[i]
                        break

                try:
                    existing_states = self.table[curr_state]
                except:
                    self.table[curr_state] = {}
                    existing_states = self.table[curr_state]

                # print(
                #     f'\t{new_state} ya existe, se agrega la transición {curr_state} -> {symbol} -> {state_ref}\n')
                existing_states[symbol] = state_ref
                self.table[curr_state] = existing_states

    def ParseTree(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        new_node = Node(self.iter, [self.iter], [self.iter], value=node.value)
        self.nodes.append(new_node)
        return new_node

    def OrNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        self.nodes.append(Node(None, firstpos, lastpos,
                               is_nullable, '|', node_a, node_b))
        return Node(None, firstpos, lastpos, is_nullable, '|', node_a, node_b)

    def AppendNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        self.nodes.append(
            Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b))

        return Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b)

    def KleeneNode(self, node):
        node_a = self.ParseTree(node.a)
        firstpos = node_a.firstpos
        lastpos = node_a.lastpos
        self.nodes.append(Node(None, firstpos, lastpos, True, '*', node_a))
        return Node(None, firstpos, lastpos, True, '*', node_a)

    def PlusNode(self, node):
        self.ParseTree(node.a)

    def QuestionNode(self, node):
        self.ParseTree(node.a)

    def EvalRegex(self):
        curr_state = 'A'
        for symbol in self.regex:

            if not symbol in self.symbols:
                return 'No'
            # print(f'\nEvaluando {symbol} en {curr_state}')
            try:
                curr_state = self.table[curr_state][symbol]
                # print(f'Nuevo estado: {curr_state}')
            except:
                # print(f'{symbol} no está en {curr_state}')
                if curr_state in self.final_states:
                    # print(
                    #     f'se acepta porque está en estado final (iniciando de nuevo...)')
                    curr_state = self.table['A'][symbol]
                else:
                    return 'No'

        return 'Yes' if curr_state in self.final_states else 'No'

    def GraphDFA(self):
        states = set(self.table.keys())
        alphabet = set(self.symbols)
        initial_state = 'A'

        dfa = SimpleDFA(states, alphabet, initial_state,
                        self.final_states, self.table)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DirectDFA.gv', source)
        graph.render('./output/DirectDFA.gv', format='pdf', view=True)


class Node:
    def __init__(self, _id, firstpos=None, lastpos=None, nullable=False, value=None, c1=None, c2=None):
        self._id = _id
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = list()
        self.nullable = nullable
        self.value = value
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f'''
    id: {self._id}
    value: {self.value}
    firstpos: {self.firstpos}
    lastpos: {self.lastpos}
    followpos: {self.followpos}
    '''
