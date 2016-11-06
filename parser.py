### Lisp Intrepreter in Python
## Parser

from functools import reduce
import re

def bracket_parser(data):
    if data[0] == '(':
        return [data[0], data[1:]]

def space_parser(data):
    space_reg_ex = re.compile('\s+')
    space_match = space_reg_ex.match(data)
    if space_match:
        return [data[:space_match.end()], data[space_match.end():]]

def number_parser(data):
    number_reg_ex = re.compile('\d+')
    number_match = number_reg_ex.match(data)
    if number_match:
        return[data[:number_match.end()], data[number_match.end():]]

def identifier_parser(data):
    pass

keywords_li = ['define', 'lambda', '*', '+', '-', '/', '<', '>', '<=', '>=', '%', 'if',
               'length', 'abs', 'append', 'pow', 'min', 'max', 'round', 'not', 'quote']

def keyword_parser(data):
    for item in keywords_li:
        if data.startswith(item):
            return key_parser(data)

def declarator_parser(data):
    if data[:6] == 'define':
        return ['define', data[6:]]

def lambda_parser(data):
    if data[:6] == 'lambda':
        return ['lambda', data[6:]]

arithmetic_operators = ['*', '+', '-', '/', '%']

def arithemetic_parser(data):
    for item in arithmetic_operators:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

binary_operations = ['<=', '>=', '<', '>', 'pow', 'append']

def binary_parser(data):
    for item in binary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

unary_operations = ['length', 'abs', 'round', 'not']

def unary_parser(data):
    for item in unary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

def if_parser(data):
    if data[:2] == 'if':
        return [data[:2], data[2:]]

def se_parser(data):
    pass

def atom(s):
    try: return int(s)
    except TypeError:
        return s
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

def expression_parser(data):
    res = value_parser(data)
    rest = res.pop(1)
    token = res.pop(0)
    if token == '(':
        L = []
        while rest[0] != ')':
            nex = expression_parser(rest)
            rest = nex.pop(1)
            token = nex.pop(0)
            if token[0] == ' ' or token == '\n':
                continue
            L.append(atom(token))
        rest = rest[1:]
        return [L, rest]
    else:
        return [token, rest]

def any_one_parser_factory(*args):
    return lambda data: (reduce(lambda f, g: f if f(data)  else g, args)(data))

value_parser = any_one_parser_factory(space_parser, bracket_parser, keyword_parser, number_parser)
key_parser = any_one_parser_factory(declarator_parser, lambda_parser, if_parser,
                                    binary_parser, arithemetic_parser, unary_parser)

def main():
    file_name = input()
    with open(file_name, 'r') as f:
        data = f.read().strip()
    print(expression_parser(data))

if __name__ == "__main__":
    main()


