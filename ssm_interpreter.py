import sys
stack=[]
store={}
ARG_OPS = {'ildc', 'jz', 'jnz', 'jmp'}
NOARG_OPS = {'iadd','isub','imul','idiv','imod','pop','dup','swap','load','store'}
def error(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)
def safe_pop():
    if not stack:
        error("pop from empty stack")
    return stack.pop()
def ildc(a):
    try:
        int(a)
        stack.append(int(a))
    except (ValueError, TypeError):
        return
def iadd(a,b):
    b = safe_pop()
    a = safe_pop()
    stack.append(a + b)
def isub(a,b):
    b = safe_pop()
    a = safe_pop()
    stack.append(a - b)
def imul(a,b):
    b = safe_pop()
    a = safe_pop()
    stack.append(a * b)
def idiv(a,b):
    b = safe_pop()
    a = safe_pop()
    if b == 0:
        error("division by zero")
    stack.append(a// b)
def imod(a,b):
    b = safe_pop()
    a = safe_pop()
    stack.append(a % b)
def load():
    a = safe_pop()
    if a not in store:
        error("uninitialized store access")
    stack.append(store[a])
def dup():
    stack.append(stack[0])
#TODO: JZ label, jnz label, jmp label
def store():
    i = safe_pop()
    a = safe_pop()
    store[a]=i
def strip_comments(text):
    lines = text.split('\n')
    cleaned = [line.split('#', 1)[0] for line in lines]
    return '\n'.join(cleaned)

def valid_integer(tok):
    if tok.startswith('-'):
        return len(tok) > 1 and tok[1:].isdigit()
    return tok.isdigit()

def valid_label_name(name):
    return len(name) > 0 and name[0].isalpha() and all(c.isalnum() or c == '_' for c in name )

def build_program(tokens):
    instructions=[]
    labels={}
    i=0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith(":"):
            name= tok[:-1]
            if not valid_label_name(name):
                error(f"invalid variable name: {tok}")
            if name in labels:
                error(f"duplicate label: {name}")
                labels[name] = len(instructions)
                i+=1
                continue
            if tok in ARG_OPS:
                if i+1>= len(tokens):
                    error(f"missing argument for {tok}")
                arg_tok= tokens[i+1]
                if tok == 'ildc':
                    if not valid_integer(arg_tok):
                        error(f"invalid integer: {arg_tok}")
                    arg = int(arg_tok)
                else:  # jz/jnz/jmp take a label name
                    arg = arg_tok
                instructions.append((tok, arg))
                i += 2
            elif tok in NOARG_OPS:
                instructions.append((tok, None))
                i += 1
            else:
                error(f"unknown token: {tok}")
             # second pass: make sure every jump target actually exists
            for opcode, arg in instructions:
                if opcode in ('jz', 'jnz', 'jmp') and arg not in labels:
                    error(f"undefined label: {arg}")

            return instructions, labels

def main():
    filename = argv
    txt = open(filename)

    print(txt)
