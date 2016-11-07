#interpreter

import math
import operator as op
from functools import reduce
from parser import expression_parser

lisp_to_python_dic = {
    '+':lambda *x: reduce(op.add, *x), '-':lambda *x: reduce(op.sub, *x),
    '*':lambda *x: reduce(op.mul, *x), '/':lambda *x: reduce(op.truediv, *x),
    '>':lambda *x: reduce(op.gt, *x), '<':lambda *x: reduce(op.lt, *x),
    '>=':lambda *x: reduce(op.ge, *x), '<=':lambda *x: reduce(op.le, *x),
    '=':lambda *x: reduce(op.eq, *x),
    'abs':     abs,
    'append':  lambda *x: reduce(op.add, *x),
    'apply':   lambda x: x[0](x[1:]),
    'begin':   lambda *x: x[-1],
    'car':     lambda x: x[0],
    'cdr':     lambda x: x[1:],
    'cons':    lambda x, y: [x] + y,
    'eq?':     op.is_,
    'equal?':  op.eq,
    'length':  len,
    'list':    lambda *x: list(x),
    'list?':   lambda x: isinstance(x, list),
    'map':     map,
    'max':     max,
    'min':     min,
    'not':     op.not_,
    'null?':   lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round':   round,
    'symbol?': lambda x: isinstance(x, str),
    }

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def eval(x, dic):
    if isinstance(x, str):
        return dic[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = eval(conseq,dic) if eval(test, dic) else eval(alt,dic)
        return eval(exp, dic)
    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'set!':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)
    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        return proc(args)

#print(eval(['define', 'x', 100], lisp_to_python_dic))

#print(eval(['define', 'y', 5], lisp_to_python_dic))

#print(eval(['lambda', ['x', 'y'], ['*', 'x', 'y'], 5, 2], lisp_to_python_dic))

#print(eval(['*', ['+', 5, 7], ['/', 4, 2]], lisp_to_python_dic))

#print(eval(['*', 'x', 'x'], lisp_to_python_dic))

#print(eval(expression_parser('(+ 5 (* 3 2) )')[0], lisp_to_python_dic))

#print(eval(['>', 5 ,10], lisp_to_python_dic))

#print(eval(['if', ['<', 5 ,10], ['+', 10, 5],['-', 10, 5]], lisp_to_python_dic))

def main():
    file_name = input()
    with open(file_name, 'r') as f:
        data = f.read().strip()
    print(eval(expression_parser(data).pop(0), lisp_to_python_dic))

if __name__ == "__main__":
    main()

