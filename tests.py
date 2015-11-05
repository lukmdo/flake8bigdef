from flake8bigdef import Checker, ast

FUNCTION = (
    'def f():\n' +
    '\tb = 1\n' * 50 +
    '\treturn b')
METHOD = (
    'class A(object):\n'
    '\tdef m(self):\n' +
    '\t\tb = 1\n' * 50 +
    '\t\treturn b')


def check(code_str, name, length=None, line=1, col=0):
    if not length:
        length = len(code_str.splitlines()) - 1
    tree = ast.parse(code_str)
    checker = Checker(tree)
    msg = checker.format_message(name, length)
    list(checker.run()) == [(1, 0, msg, Checker)]
    expected_errors = [(line, col, msg, Checker)]

    return list(checker.run()), expected_errors


def test_no_error():
    got, _ = check('def a(): return 42', 'a')
    assert got == []


def test_long_function():
    got, expected = check(FUNCTION, 'f')
    assert got == expected


def test_long_method():
    got, expected = check(METHOD, 'A.m', 51, 2, 1)
    assert got == expected
