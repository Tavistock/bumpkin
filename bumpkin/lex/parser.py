from functools import wraps

from rply import ParserGenerator

from .lexer import lexer
from .exceptions import LexException, PrematureEndOfInput

from bumpkin.models.float import BFloat
from bumpkin.models.integer import BInteger
from bumpkin.models.complex import BComplex
from bumpkin.models.symbol import BSymbol
from bumpkin.models.expression import BExpression


pg = ParserGenerator([rule.name for rule in lexer.rules] + ['$end'],
                     cache_id="bumpkin_parser")


def set_boundaries(fun):
    @wraps(fun)
    def wrapped(p):
        start = p[0].source_pos
        end = p[-1].source_pos
        ret = fun(p)
        ret.start_line = start.lineno
        ret.start_column = start.colno
        if start is not end:
            ret.end_line = end.lineno
            ret.end_column = end.colno
        else:
            ret.end_line = start.lineno
            ret.end_column = start.colno + len(p[0].value)
        return ret
    return wrapped


@pg.production("main : list_contents")
def main(s):
    return s[0]


@pg.production("main : $end")
def main_empty(s):
    return []


@pg.production("term : paren")
@pg.production("term : identifier")
def term(s):
    return s[0]


@pg.production("paren : LPAREN list_contents RPAREN")
@set_boundaries
def paren(s):
    return BExpression(s[1])


@pg.production("paren : LPAREN RPAREN")
@set_boundaries
def empty_paren(s):
    return BExpression([])


@pg.production("identifier : IDENTIFIER")
@set_boundaries
def t_identifier(s):
    obj = s[0].value

    try:
        return BInteger(obj)
    except ValueError:
        pass

    try:
        return BFloat(obj)
    except ValueError:
        pass

    if obj != 'j':
        try:
            return BComplex(obj)
        except ValueError:
            pass

    table = {
        "true": "True",
        "false": "False",
        "nil": "None",
        "null": "None",
    }

    if obj in table:
        return BSymbol(table[obj])

    # if obj.startswith(":"):
    #     return BKeyword(obj)

    # if obj.startswith("&"):
    #     return BLambdaListKeyword(obj)

    # def mangle(p):
    #     if p.startswith("*") and p.endswith("*") and p not in ("*", "**"):
    #         p = p[1:-1].upper()

    #     if "-" in p and p != "-":
    #         p = p.replace("-", "_")

    #     if p.endswith("?") and p != "?":
    #         p = "is_%s" % (p[:-1])

    #     return p

    # obj = ".".join([mangle(part) for part in obj.split(".")])

    return BSymbol(obj)


@pg.production("list_contents : term list_contents")
def list_contents_single(s):
    return [s[0]] + s[1]


@pg.production("list_contents : term")
def list_contents(s):
    return [s[0]]


@pg.error
def error_handler(token):
    tokentype = token.gettokentype()
    if tokentype == '$end':
        raise PrematureEndOfInput("Premature end of input")
    else:
        raise LexException(
            "Ran into a %s where it wasn't expected." % tokentype,
            token.source_pos.lineno, token.source_pos.colno)


parser = pg.build()
