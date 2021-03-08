from graphviz import Digraph
from nodes import Or
from tokens import TokenType
from utils import WriteToFile


class NFA:
    def __init__(self, init_node, symbols):
        self.dot = Digraph(comment='Diagrama NFA', strict=True)
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')
        self.init_node = init_node
        self.final_states = []
        self.symbols = symbols
        self.curr_state = 1

    def Render(self, node):
        self.prev_state = self.curr_state
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        return node.value

    def OrNode(self, node):
        initial_node = self.curr_state - 1
        mid_node = None

        # from initial to first epsilon
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )
        self.curr_state += 1

        # from epsilon to first
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        mid_node = self.curr_state
        self.curr_state += 1

        # from initial to second epsilone
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )

        self.curr_state += 1

        # from epsilon to second
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.b)
        )

        self.curr_state += 1

        # from first to last epsilon
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

    def AppendNode(self, node):

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.b)
        )

    def KleeneNode(self, node):

        # First epsilon
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'e'
        )

        first_node = self.curr_state - 1
        self.curr_state += 1

        # Render node
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        self.curr_state += 1

        # Second epsilon
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'e'
        )

        # First epsilon to last state
        self.dot.edge(
            str(first_node),
            str(self.curr_state),
            'e'
        )

        # Last state to first epsilon
        self.dot.edge(
            str(self.curr_state),
            str(first_node + 1),
            'e'
        )

    def PlusNode(self, node):
        self.KleeneNode(node)
        self.curr_state += 1

        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

    def QuestionNode(self, node):
        initial_node = self.curr_state - 1
        mid_node = None

        # from initial to first epsilon
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )
        self.curr_state += 1

        # from epsilon to first
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        mid_node = self.curr_state
        self.curr_state += 1

        # from initial to second epsilone
        self.dot.edge(
            str(initial_node),
            str(self.curr_state),
            'e'
        )

        self.curr_state += 1

        # from epsilon to second
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            'e'
        )

        self.curr_state += 1

        # from first to last epsilon
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

    def WriteNFADiagram(self):
        source = self.dot.source
        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)

    def GetFinalStates(self):
        self.dot.node(str(self.curr_state), shape='doublecircle')
        self.final_states.append(self.curr_state)
        return self.final_states
