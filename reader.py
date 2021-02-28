from tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz'


class Reader:
    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None

    def CreateTokens(self):
        while self.curr_char != None:
            if self.curr_char in LETTERS:
                yield self.CreateLetter()
            elif self.curr_char == '|':
                self.Next()
                yield Token(TokenType.OR, '|')
            elif self.curr_char == '':
                self.Next()
                yield Token(TokenType.APPEND, '')
            elif self.curr_char == '(':
                self.Next()
                yield Token(TokenType.LPAR)
            elif self.curr_char == ')':
                self.Next()
                yield Token(TokenType.RPAR)
            elif self.curr_char == '*':
                self.Next()
                yield Token(TokenType.KLEENE, '*')
            elif self.curr_char == '+':
                self.Next()
                yield Token(TokenType.PLUS, '+')
            else:
                raise Exception(f'Invalid entry: {self.curr_char}')

    def CreateLetter(self):
        exp = self.curr_char
        self.Next()

        while self.curr_char != None and self.curr_char in LETTERS:
            exp += self.curr_char
            self.Next()

        return Token(TokenType.LETTER, exp)
