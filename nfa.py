from graphviz import Digraph
from nodes import Or
from tokens import TokenType
from utils import WriteToFile


class NFA:
    def __init__(self, init_node, symbols):
        self.dot = Digraph(comment='Diagrama NFA')
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')
        # self.dot.node('0')
        self.init_node = init_node
        self.final_states = []
        self.symbols = symbols
        self.curr_state = 0
        self.prev_state = 0
        self.final_state = None

    def Test(self, node):
        # self.trans_table[self.curr_state]['a'].add(0)
        return str(node.a), str(node.b)

    def Calc(self, node):
        self.prev_state = self.curr_state
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        return node.value

    def OrNode(self, node):
        initial_node = self.curr_state
        mid_node = None

        # from initial to first epsilon
        self.curr_state += 1
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )

        # from epsilon to first
        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Calc(node.a)
        )

        mid_node = self.curr_state

        # from first to second epsilone
        self.curr_state += 1
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )

        # from epsilon to second
        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Calc(node.b)
        )

        # from first to last epsilon
        self.curr_state += 1
        self.dot.edge(
            str(mid_node),
            str(self.curr_state),
            'e'
        )

        # from second to last epsilon
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'e'
        )

        # return self.Calc(node.a) + self.Calc(node.b)

    def AppendNode(self, node):

        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            # str(self.prev_state - 1),
            str(self.curr_state),
            self.Calc(node.a)
        )

        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Calc(node.b)
        )

    def KleeneNode(self, node):
        self.dot.node('s4')
        self.dot.node('s5')
        self.dot.node('s6')
        self.dot.node('s7')
        self.dot.edge('s4', 's5', 'e')
        self.dot.edge('s5', 's6', str(node.a))
        self.dot.edge('s6', 's7', 'e')
        self.dot.edge('s7', 's5', 'e')
        self.dot.edge('s4', 's7', 'e')
        return self.Calc(node.a)

    def WriteNFADiagram(self):
        source = self.dot.source
        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)


class NFADiagram:
    def __init__(self, tokens):
        self.dot = Digraph(comment='Diagrama NFA')
        self.dot.attr(rankdir='LR')
        self.curr_state = 0
        self.start_node = 1
        self.final_states = []
        self.tokens = iter(tokens)
        self.last_symbol = None
        self.Next()

    def Next(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def Diagram(self):
        if self.curr_token == None:
            return None

        while self.curr_token != None:
            self.Iterate()
            self.Next()

        self.WriteNFADiagram()

    def Iterate(self):

        if self.curr_token != None and self.curr_token.type == TokenType.LETTER:
            self.last_symbol = self.curr_token.value
            self.LetterNode()

    def LetterNode(self):
        self.curr_state += 1
        self.dot.node(str(self.curr_state), shape='circle')
        self.dot.edge(str(self.curr_state - 1), str(
            self.curr_state), str(self.last_symbol))

    def OrNode(self):
        print()
        # if (self.curr_state == 0)
        # self.dot.subgraph()

    def WriteNFADiagram(self):
        source = self.dot.source
        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)
