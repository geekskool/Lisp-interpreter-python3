### Lisp Intrepreter in Python
## Parser

from functools import reduce

def bracket_parser(data):
	if data[0]=='(' or data[0]==')':
	    return [data[0],data[1:]]
	    
#needs some fix		

def space_parser(data):
    if not data[0]:
		for i in range(len(data)):
			if data[i]:
				return ['',data[i:]]

nums='0123456789'

def number_parser(data):
	if data[0] in nums:
		for i in range(len(data)):
			if data[i] not in nums:
				return [data[:i],data[i:]]   
	
def identifier_parser(data):
	pass	

keywords = ['define', 'lambda', '*', '+', '-', '/', '<', '>', '<=', '>=', '%', 'if',
'length', 'abs', 'append', 'pow', 'min', 'max', 'round', 'not', 'quote']
	
def keyword_parser(data):
	for item in keywords:
		if data.startswith(item):
			return [data[:len(item)],data[len(item):]]

def declarator_parser(data):
	if data[:6]=='define':
		return ['define',data[6:]]
	
def lambda_parser(data):
	if data[:6]=='lambda':
		return ['lambda',data[6:]]

arithmetic_operators = ['*', '+', '-', '/', '%']
	
def arithemetic_parser(data):
	for item in arithmetic_operators:
		if data.startswith(item):
			return [data[:len(item)],data[len(item):]]

binary_operations = ['<=', '>=','<','>', 'pow', 'append']
			  
def binary_parser(data):
	for item in binary_operations:
		if data.startswith(item):
			return [data[:len(item)],data[len(item):]]
			
unary_operations = ['length', 'abs', 'round', 'not']
	
def unary_parser(data):
	for item in unary_operations:
		if data.startswith(item):
			return [data[:len(item)],data[len(item):]]
	
def if_parser(data):
	if data[:2]=='if':
		return [data[:2],data[2:]]
	
def atom_parser(data):
    pass
def expression_parser(data):
    pass
def se_parser(data):
    pass			

def atom(s):
    try: return int(s)
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

def lisp_parser(data):
    global rest
    if not len(data):
        raise SyntaxError("Unexpected EOF while reading.")
    res=value_parser(data)
    rest=res.pop(1).strip()
    token=res.pop(0)	
    if '(' ==token:
        L = []
        while rest[0] != ')':
            L.append(lisp_parser(rest))
        rest=rest[1:]
        return L
    elif token==')':
        raise SyntaxError("Wrong Syntax.")    
    else:
        return atom(token)
       	
def any_one_parser_factory(*args): 
    return lambda data:(reduce(lambda f,g:f if f(data) else g,args)(data))
         				               			
value_parser=any_one_parser_factory(bracket_parser,number_parser,declarator_parser,lambda_parser,if_parser,binary_parser,arithemetic_parser,unary_parser,keyword_parser)
		
def main():
    file_name=input()
    with open(file_name,'r') as f:
	    data=f.read().strip().replace('\n',' ')
    return print(lisp_parser(data))	

if __name__=="__main__":
	main()
