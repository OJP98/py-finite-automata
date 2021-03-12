
class DDFA:
    def __init__(self, tree):
        self.tree = tree
        self.nodes = list()
        self.table = dict()
        self.iter = 1
        self.ParseTree(tree)
        self.CalcFollowPos()

        print(self.nodes)

    def CalcFollowPos(self):
        for node in self.nodes:
            if node.value == '*':
                for i in node.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.firstpos
            elif node.value == '.':
                for i in node.c1.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.c2.firstpos

    def ParseTree(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        new_node = Node(self.iter, [self.iter], [self.iter], value=node.value)
        self.nodes.append(new_node)
        # self.table[self.iter] = node.value
        return new_node

    def OrNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.firstpos + node_b.lastpos

        self.nodes.append(Node('|', firstpos, lastpos, is_nullable, '|'))
        return Node('|', firstpos, lastpos, is_nullable, '|')

    def AppendNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        self.nodes.append(
            Node('.', firstpos, node_b.lastpos, is_nullable, '.', node_a, node_b))

        return Node('.', firstpos, node_b.lastpos, is_nullable, '.', node_a, node_b)

    def KleeneNode(self, node):
        node_a = self.ParseTree(node.a)
        firstpos = node_a.firstpos
        lastpos = node_a.lastpos
        self.nodes.append(Node('*', firstpos, lastpos, True, '*'))
        return Node('*', firstpos, lastpos, True, '*')

    def PlusNode(self, node):
        self.ParseTree(node.a)

    def QuestionNode(self, node):
        self.ParseTree(node.a)


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
    {self.firstpos} | {self.value} | {self.lastpos}'''
