import sys
stack=[]
store={}
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
#for pop we can just use python's pop
def dup():
    stack.append(stack[0])
#TODO: JZ label, jnz label, jmp label
def store():
    b = safe_pop()
    a = safe_pop()
    store[a]=i
def strip_comments(text):
    lines = text.split('\n')
    cleaned = [line.split('#', 1)[0] for line in lines]
    return '\n'.join(cleaned)
