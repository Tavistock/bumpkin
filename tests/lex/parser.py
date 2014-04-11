from bumpkin.models.expression import BExpression
from bumpkin.models.integer import BInteger
from bumpkin.models.float import BFloat
from bumpkin.models.complex import BComplex
from bumpkin.models.symbol import BSymbol

from bumpkin.lex import LexException, PrematureEndOfInput, tokenize


def test_lex_exception():
    """ Ensure tokenize throws a fit on a partial input """
    try:
        tokenize("(foo")
        assert True is False
    except PrematureEndOfInput:
        pass
    try:
        tokenize("{foo bar")
        assert True is False
    except LexException:  # wrong error
        pass
    try:
        tokenize("(defn foo [bar]")
        assert True is False
    except LexException:  # wrong error
        pass


def test_unbalanced_exception():
    """Ensure the tokenization fails on unbalanced expressions"""
    try:
        tokenize("(bar))")
        assert True is False
    except LexException:
        pass

    try:
        tokenize("(baz [quux]])")
        assert True is False
    except LexException:
        pass


def test_lex_expression_symbols():
    """ Make sure that expressions produce symbols """
    objs = tokenize("(foo bar)")
    assert objs == [BExpression([BSymbol("foo"), BSymbol("bar")])]


def test_lex_expression_integer():
    """ Make sure expressions can produce integers """
    objs = tokenize("(foo 2)")
    assert objs == [BExpression([BSymbol("foo"), BInteger(2)])]


def test_lex_symbols():
    """ Make sure that symbols are valid expressions"""
    objs = tokenize("foo ")
    assert objs == [BSymbol("foo")]


def test_lex_integers():
    """ Make sure that integers are valid expressions"""
    objs = tokenize("42 ")
    assert objs == [BInteger(42)]


def test_lex_expression_float():
    """ Make sure expressions can produce floats """
    objs = tokenize("(foo 2.)")
    assert objs == [BExpression([BSymbol("foo"), BFloat(2.)])]
    objs = tokenize("(foo -0.5)")
    assert objs == [BExpression([BSymbol("foo"), BFloat(-0.5)])]
    objs = tokenize("(foo 1.e7)")
    assert objs == [BExpression([BSymbol("foo"), BFloat(1.e7)])]


def test_lex_expression_complex():
    """ Make sure expressions can produce complex """
    objs = tokenize("(foo 2.j)")
    assert objs == [BExpression([BSymbol("foo"), BComplex(2.j)])]
    objs = tokenize("(foo -0.5j)")
    assert objs == [BExpression([BSymbol("foo"), BComplex(-0.5j)])]
    objs = tokenize("(foo 1.e7j)")
    assert objs == [BExpression([BSymbol("foo"), BComplex(1.e7j)])]
    objs = tokenize("(foo j)")
    assert objs == [BExpression([BSymbol("foo"), BSymbol("j")])]


def test_lex_line_counting():
    """ Make sure we can count lines / columns """
    entry = tokenize("(foo (one two))")[0]

    assert entry.start_line == 1
    assert entry.start_column == 1

    assert entry.end_line == 1
    assert entry.end_column == 15

    entry = entry[1]
    assert entry.start_line == 1
    assert entry.start_column == 6

    assert entry.end_line == 1
    assert entry.end_column == 14


def test_lex_line_counting_multi():
    """ Make sure we can do multi-line tokenization """
    entries = tokenize("""
(foo (one two))
(foo bar)
""")

    entry = entries[0]

    assert entry.start_line == 2
    assert entry.start_column == 1

    assert entry.end_line == 2
    assert entry.end_column == 15

    entry = entries[1]
    assert entry.start_line == 3
    assert entry.start_column == 1

    assert entry.end_line == 3
    assert entry.end_column == 9


def test_lex_line_counting_multi_inner():
    """ Make sure we can do multi-line tokenization (inner) """
    entry = tokenize("""(foo
    bar)""")[0]
    inner = entry[0]

    assert inner.start_line == 1
    assert inner.start_column == 2

    inner = entry[1]

    assert inner.start_line == 2
    assert inner.start_column == 5


def test_nospace():
    """ Ensure we can tokenize without spaces if we have to """
    entry = tokenize("(foo(one two))")[0]

    assert entry.start_line == 1
    assert entry.start_column == 1

    assert entry.end_line == 1
    assert entry.end_column == 14

    entry = entry[1]
    assert entry.start_line == 1
    assert entry.start_column == 5

    assert entry.end_line == 1
    assert entry.end_column == 13


# def test_escapes():
#     """ Ensure we can escape things """
#     entry = tokenize("(foo \"foo\\n\")")[0]
#     assert entry[1] == "foo\n"

#     entry = tokenize("(foo \"foo\s\")")[0]
#     assert entry[1] == "foo\\s"


# def test_unicode_escapes():
#     """Ensure unicode escapes are handled correctly"""
#     s = r'"a\xac\u1234\u20ac\U00008000"'
#     assert len(s) == 29
#     entry = tokenize(s)[0]
#     assert len(entry) == 5
#     assert [ord(x) for x in entry] == [97, 172, 4660, 8364, 32768]


def test_complex():
    """Ensure we tokenize complex numbers properly"""
    # This is a regression test for #143
    entry = tokenize("(1j)")[0][0]
    assert entry == BComplex("1.0j")
    entry = tokenize("(j)")[0][0]
    assert entry == BSymbol("j")
