from Errors.error_library import get_error_lib
from Errors.log import Log


def conversion(infix, logs):

    specials = {'?': 5, '+': 4, '*': 3, '.': 2, '|': 1}
    single_symbols = ['.', '|']
    repetition_symbols = ['?','+','*']

    postfix = ""
    stack = ""
    prev = ""

    if infix[0] in specials:
        raise Log("e13", 0, [infix[0]])
    
    #a.(a|b*.b
    for c in infix:
        if c.isspace():
            logs.append(Log("w10", 1, []))
            break
        if c not in specials and c.isdigit() == False and c.isalpha() == False and c not in ['(', ')']:
            raise Log("e10", 1, [c])
        elif c == '(':
            stack = stack + c
            prev = c
        
        elif c == ')':
            if prev in single_symbols:
                raise Log('e15', 0, [])
            while stack != "":
                if stack[-1] == '(':
                    break
                postfix, stack = postfix + stack[-1], stack[:-1]
            if stack == "":
                raise Log("e11", 0, [])
            stack = stack[:-1]
            prev = c

        elif c in specials:
            if c in single_symbols and prev in single_symbols:
                raise Log("e14", 0, [prev, c])
            if prev == '(':
                raise Log('e15', 0, [])
            if prev in single_symbols:
                raise Log('e16', 0, [c, prev])
            if c in repetition_symbols and prev in repetition_symbols:
                raise Log('e17', 0, [])
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            
            stack = stack + c
            prev = c
        else:
            postfix = postfix + c
            prev = c

    while stack:
        if stack[-1] == '(':
            raise Log("e12", 0, [])
        postfix, stack = postfix + stack[-1], stack[:-1]

    return postfix


class state:
    label = None
    edge1 = None
    edge2 = None

class NFA:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def create(postfix):
    nfaStack = []

    for c in postfix:
        if c == '?':

            NFA1 = nfaStack.pop()

            initial = state()
            accept = state()

            initial.edge1 = NFA1.initial
            initial.edge2 = accept

            NFA1.accept.edge1 = accept

            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)

        elif c == '+':

            NFA1 = nfaStack.pop()

            #initial = state()
            accept = state()

            
            NFA1.accept.edge1 = NFA1.initial
            NFA1.accept.edge2 = accept

            newNFA = NFA(NFA1.initial, accept)
            nfaStack.append(newNFA)

        elif c == '*':

            NFA1 = nfaStack.pop()

            initial = state()
            accept = state()

            initial.edge1 = NFA1.initial
            initial.edge2 = accept

            NFA1.accept.edge1 = NFA1.initial
            NFA1.accept.edge2 = accept

            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)

        elif c == '.':

            NFA2 = nfaStack.pop()
            NFA1 = nfaStack.pop()

            NFA1.accept.edge1 = NFA2.initial

            newNFA = NFA(NFA1.initial, NFA2.accept)
            nfaStack.append(newNFA)

        elif c == '|':

            NFA2 = nfaStack.pop()
            NFA1 = nfaStack.pop()


            initial = state()

            initial.edge1 = NFA1.initial
            initial.edge2 = NFA2.initial

            accept = state()

            NFA1.accept.edge1 = accept
            NFA2.accept.edge1 = accept

            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)

        else:

            accept = state()
            initial = state()

            initial.label = c
            initial.edge1 = accept

            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)

    return nfaStack.pop()
            


#print(create(conversion('a.(a|b)*.b')))