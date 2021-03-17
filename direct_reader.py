from tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz01234567890.'


class DirectReader:

    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.input = set()
        self.rparPending = False
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None

    def CreateTokens(self):
        while self.curr_char != None:

            if self.curr_char in LETTERS:
                self.input.add(self.curr_char)
                yield Token(TokenType.LETTER, self.curr_char)

                self.Next()

                # Finally, check if we need to add an append token
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            elif self.curr_char == '|':
                yield Token(TokenType.OR, '|')

                self.Next()

                if self.curr_char != None and self.curr_char not in '()':
                    yield Token(TokenType.LPAR)

                    while self.curr_char != None and self.curr_char not in ')*+?':
                        if self.curr_char in LETTERS:
                            self.input.add(self.curr_char)
                            yield Token(TokenType.LETTER, self.curr_char)

                            self.Next()
                            if self.curr_char != None and \
                                    (self.curr_char in LETTERS or self.curr_char == '('):
                                yield Token(TokenType.APPEND, '.')

                    if self.curr_char != None and self.curr_char in '*+?':
                        self.rparPending = True
                    elif self.curr_char != None and self.curr_char == ')':
                        yield Token(TokenType.RPAR, ')')
                    else:
                        yield Token(TokenType.RPAR, ')')

            elif self.curr_char == '(':
                self.Next()
                yield Token(TokenType.LPAR)

            elif self.curr_char in (')*+?'):

                if self.curr_char == ')':
                    self.Next()
                    yield Token(TokenType.RPAR)

                elif self.curr_char == '*':
                    self.Next()
                    yield Token(TokenType.KLEENE)

                elif self.curr_char == '+':
                    self.Next()
                    yield Token(TokenType.PLUS)

                elif self.curr_char == '?':
                    self.Next()
                    yield Token(TokenType.QUESTION)

                if self.rparPending:
                    yield Token(TokenType.RPAR)
                    self.rparPending = False

                # Finally, check if we need to add an append token
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            else:
                raise Exception(f'Invalid entry: {self.curr_char}')

        yield Token(TokenType.APPEND, '.')
        yield Token(TokenType.LETTER, '#')

    def GetSymbols(self):
        return self.input
