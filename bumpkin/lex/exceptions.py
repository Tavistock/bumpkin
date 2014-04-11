from bumpkin.errors import BError


class LexException(BError):
    """Error during the Lexing of a Bumpkin expression."""
    def __init__(self, message, lineno, colno):
        super(LexException, self).__init__(message)
        self.message = message
        self.lineno = lineno
        self.colno = colno
        self.source = None
        self.filename = '<stdin>'

    def __str__(self):

        # line = self.lineno
        # start = self.colno

        # result = ""

        # source = self.source.split("\n")

        # if line > 0 and start > 0:
        #     result += '  File "%s", line %d, column %d\n\n' % (self.filename,
        #                                                        line,
        #                                                        start)

        #     if len(self.source) > 0:
        #         source_line = source[line-1]
        #     else:
        #         source_line = ""

        #     result += '  %s\n' % (source_line)
        #     result += '  %s%s\n' % (' '*(start-1), '^')

        result = "LexException: %s\n\n" % (self.message)

        return result


class PrematureEndOfInput(LexException):
    """We got a premature end of input"""
    def __init__(self, message):
        super(PrematureEndOfInput, self).__init__(message, -1, -1)
