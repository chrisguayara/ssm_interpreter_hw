import sys

stack=[]
store={}
def ildc(a):
    try:
        int(a)
        stack.append(a)
    except (ValueError, TypeError):
        return
def iadd(a,b):
    return a+b
def isub(a,b):
    return a-b
def imul(a,b):
    return a*b
def idiv(a,b):
    return a/b
def imod(a,b):
    return a%b
#for pop we can just use python's pop
def dup():
    stack.append(stack[0])
#TODO: JZ label, jnz label, jmp label
def store():
    i=stack.pop()
    a=stack.pop()
    store[a]=i
    


def main():
    filename = argv
    txt = open(filename)

    print(txt)
