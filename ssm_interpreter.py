#!/usr/bin/env python3
"""
CSE 304
Assignment 01

Names: Kushagra Taneja netid: kutaneja 116646299, Christopher Guayara netid: cguayara 112881441
"""

import sys

stack = []       # operand stack
store_mem = {}   # directly-addressed store (dict: address -> value)

ARG_OPS = {'ildc', 'jz', 'jnz', 'jmp'}
NOARG_OPS = {'iadd', 'isub', 'imul', 'idiv', 'imod',
             'pop', 'dup', 'swap', 'load', 'store'}


def error(msg): #error handling
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)
def safe_pop():
    if not stack:
        error("attempted to pop from an empty stack")
    return stack.pop()
def ildc(arg):
    stack.append(arg)
def iadd():
    b = safe_pop()
    a = safe_pop()
    stack.append(a + b)
def isub():
    b = safe_pop()
    a = safe_pop()
    stack.append(a - b)
def imul():
    b = safe_pop()
    a = safe_pop()
    stack.append(a * b)

def idiv():
    b = safe_pop()
    a = safe_pop()
    if b == 0:
        error("division by zero")
    stack.append(int(a / b))
def imod():
    b = safe_pop()
    a = safe_pop()
    if b == 0:
        error("division by zero")
    q = int(a / b)           
    stack.append(a - q * b)
def pop_op():
    safe_pop()
def dup():
    if not stack:
        error("attempted to dup an empty stack")
    stack.append(stack[-1])
def swap():
    if len(stack) < 2:
        error("swap requires at least two elements on the stack")
    stack[-1], stack[-2] = stack[-2], stack[-1]
def load():
    a = safe_pop()
    if a not in store_mem:
        error(f"uninitialized store access at address {a}")
    stack.append(store_mem[a])


def store_op():
    i = safe_pop()
    a = safe_pop()
    store_mem[a] = i


DISPATCH = {
    'iadd': iadd,
    'isub': isub,
    'imul': imul,
    'idiv': idiv,
    'imod': imod,
    'pop': pop_op,
    'dup': dup,
    'swap': swap,
    'load': load,
    'store': store_op,
}

# parsing logic
def strip_comments(text):
    lines = text.split('\n')
    cleaned = [line.split('#', 1)[0] for line in lines]
    return '\n'.join(cleaned)
def tokenize(text):
    text = strip_comments(text)
    return text.split()   # splits on any run of whitespace: space, tab, newline
def valid_integer(tok):
    if tok.startswith('-'):
        return len(tok) > 1 and tok[1:].isdigit()
    return tok.isdigit()

def valid_label_name(name):
    return (len(name) > 0
            and name[0].isalpha()
            and all(c.isalnum() or c == '_' for c in name))

def build_program(tokens):
    instructions = []   # list of (opcode, arg_or_None)
    labels = {}          # label name indexed into instructions

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok.endswith(':'):
            name = tok[:-1]
            if not valid_label_name(name):
                error(f"improperly formed label: {tok}")
            if name in labels:
                error(f"duplicate label: {name}")
            labels[name] = len(instructions)
            i += 1
            continue

        if tok in ARG_OPS:
            if i + 1 >= len(tokens):
                error(f"missing argument for instruction: {tok}")
            arg_tok = tokens[i + 1]
            if tok == 'ildc':
                if not valid_integer(arg_tok):
                    error(f"invalid integer argument: {arg_tok}")
                arg = int(arg_tok)
            else:  # jz / jnz / jmp take a label name as argument
                arg = arg_tok
            instructions.append((tok, arg))
            i += 2
        elif tok in NOARG_OPS:
            instructions.append((tok, None))
            i += 1
        else:
            error(f"invalid instruction: {tok}")

    # Second pass: every jump target must resolve to a defined label.
    # (Must happen after the whole program is built, since a jump may
    # reference a label that appears later in the file.)
    for opcode, arg in instructions:
        if opcode in ('jz', 'jnz', 'jmp') and arg not in labels:
            error(f"undefined label used as jump target: {arg}")

    return instructions, labels

# Execution
def run(instructions, labels):
    ip = 0
    while ip < len(instructions):
        opcode, arg = instructions[ip]

        if opcode == 'ildc':
            ildc(arg)
            ip += 1
        elif opcode == 'jmp':
            ip = labels[arg]
        elif opcode == 'jz':
            v = safe_pop()
            ip = labels[arg] if v == 0 else ip + 1
        elif opcode == 'jnz':
            v = safe_pop()
            ip = labels[arg] if v != 0 else ip + 1
        elif opcode in DISPATCH:
            DISPATCH[opcode]()
            ip += 1
        else:
            error(f"unknown opcode: {opcode}")

    if not stack:
        error("stack is empty at end of program; nothing to print")
    print(stack[-1])

def main():
    if len(sys.argv) < 2:
        error("usage: python3 ssm_interpreter.py <input_file>")

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            text = f.read()
    except OSError as e:
        error(f"could not open file {filename}: {e}")

    tokens = tokenize(text)
    instructions, labels = build_program(tokens)
    run(instructions, labels)


if __name__ == "__main__":
    main()