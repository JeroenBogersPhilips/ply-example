# implementation of lexer and parser for simple calculator, using ply (lex and yacc)

import ply.lex as lex
import ply.yacc as yacc

# lexing

tokens = (
    "NUMBER",
    "EQUALS",
    "PLUS",
    "MINUS",
    "MULTIPLICATION",
    "DIVISION",
    "NAME",
    "LPAREN",
    "RPAREN")

t_ignore = ' \t'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value))

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# parsing

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times_factor(p):
    'term : term MULTIPLICATION factor'
    p[0] = p[1] * p[3]

def p_term_divided_by_factor(p):
    'term : term DIVISION factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expression(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    raise TypeError("Syntax error in input!")

# tests

import unittest

class TestLexer(unittest.TestCase):
    def test_lexing_of_simple_calculation(self):
        lex.lex()
        lex.input("x = 3 * (4 + 5) * 6")

        actual = [(tok.type, tok.value) for tok in iter(lex.token, None)]

        expected = [('NAME', 'x'),
                    ('EQUALS', '='),
                    ('NUMBER', 3),
                    ('MULTIPLICATION', '*'),
                    ('LPAREN', '('),
                    ('NUMBER', 4),
                    ('PLUS', '+'),
                    ('NUMBER', 5),
                    ('RPAREN', ')'),
                    ('MULTIPLICATION', '*'),
                    ('NUMBER', 6)]

        self.assertEqual(actual, expected)


class TestParser(unittest.TestCase):
    def test_without_parenthesis(self):
        parser = yacc.yacc()

        input = "3 * 4 + 5 * 6"

        actual = parser.parse(input)

        self.assertEqual(actual, 42)

    def test_with_parenthesis(self):
        parser = yacc.yacc()

        input = "3 * (4 + 5) * 6"

        actual = parser.parse(input)

        self.assertEqual(actual, 162)

    def test_unbalanced_parenthesis_gives_syntax_error(self):
        parser = yacc.yacc()
        input = "3 * (4 + 5) * 6)"

        with self.assertRaises(TypeError):
            parser.parse(input)

if __name__ == '__main__':
    unittest.main()
