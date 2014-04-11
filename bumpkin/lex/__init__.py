from rply.errors import LexingError

from bumpkin.lex.exceptions import LexException, PrematureEndOfInput
from bumpkin.lex.lexer import lexer
from bumpkin.lex.parser import parser


def tokenize(buf):
    """
    Tokenize a Lisp file or string buffer into internal Bumpkin objects.
    """
    try:
        return parser.parse(lexer.lex(buf))
    except LexingError as e:
        pos = e.getsourcepos()
        raise LexException("Could not identify the next token.",
                           pos.lineno, pos.colno)
