from graphviz import Digraph
from nodes import Or
from tokens import TokenType
from utils import WriteToFile


class NFA:
    def __init__(self, init_node):
        self.dot = Digraph(comment='Diagrama NFA')
        self.init_node = init_node
        self.AppendNode(self.init_node)
        source = self.dot.source

        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)

    def Calc(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def OrNode(self, node):
        self.dot.node('s0')
        self.dot.node('s1', shape='doublecircle')
        self.dot.edge('s0', 's1', str(node.a))
        self.dot.edge('s0', 's1', str(node.b))

    def AppendNode(self, node):
        self.dot.node('s0')
        self.dot.node('s1')
        self.dot.node('s2', shape='doublecircle')
        self.dot.edge('s0', 's1', str(node.a))
        self.dot.edge('s1', 's2', str(node.b))

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
