from tokens import TokenType
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.Next()

    def Next(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def NewFactor(self):
        token = self.curr_token

        if token.type == TokenType.LPAR:
            self.Next()
            res = self.Expression()

            if self.curr_token.type != TokenType.RPAR:
                raise Exception('No right parenthesis for expression!')

            self.Next()
            return res

        elif token.type == TokenType.LETTER:
            self.Next()
            return Letter(token.value)

    def NewKleene(self):
        res = self.NewFactor()

        while self.curr_token != None and (self.curr_token.type == TokenType.KLEENE):
            self.Next()
            res = Kleene(res)

        return res

    def Expression(self):
        res = self.NewKleene()

        while self.curr_token != None and (self.curr_token.type == TokenType.OR or self.curr_token.type == TokenType.PLUS):
            if self.curr_token.type == TokenType.OR:
                self.Next()
                res = Or(res, self.NewKleene())

        return res

    def Parse(self):
        if self.curr_token == None:
            return None

        res = self.Expression()
        while self.curr_token != None:
            res = Expression(res, self.Expression())

        return res
