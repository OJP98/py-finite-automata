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

    def NewSymbol(self):
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

    def NewOperator(self):
        res = self.NewSymbol()

        while self.curr_token != None and \
                (
                    self.curr_token.type == TokenType.KLEENE or
                    self.curr_token.type == TokenType.PLUS or
                    self.curr_token.type == TokenType.QUESTION
                ):
            if self.curr_token.type == TokenType.KLEENE:
                self.Next()
                res = Kleene(res)
            elif self.curr_token.type == TokenType.QUESTION:
                self.Next()
                res = Question(res)
            else:
                self.Next()
                res = Plus(res)

        return res

    def Expression(self):
        res = self.NewOperator()

        while self.curr_token != None and \
                (
                    self.curr_token.type == TokenType.APPEND or
                    self.curr_token.type == TokenType.OR
                ):
            if self.curr_token.type == TokenType.OR:
                self.Next()
                res = Or(res, self.NewOperator())

            elif self.curr_token.type == TokenType.APPEND:
                self.Next()
                res = Append(res, self.NewOperator())

        return res

    def Parse(self):
        if self.curr_token == None:
            return None

        res = self.Expression()

        return res
