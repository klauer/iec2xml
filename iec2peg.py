# IEC grammar language to pyPEG compiler

from pyPEG import parse

import re
r = re.compile

import fileinput

def comment(): return r(r"\#.*")

terminal_symbol = r(r"\$?('.*?'" + r'|".*?")')
non_terminal_symbol = r(r"[a-z_][a-z0-9_]*")

def regex(): return "<", r(r"((\\\>)|[^>])+"), ">"
def production(): return non_terminal_symbol, "::=", [alternation, concat], ";"
def concat(): return -2, [regex, terminal_symbol, non_terminal_symbol, parentheses, closure, option]
def _extended_structure(): return [alternation, regex, terminal_symbol, non_terminal_symbol, parentheses, closure, option]
_S = -2, _extended_structure

def parentheses(): return "(", _S, ")"
def closure(): return "{", _S, "}"
def option(): return "[", _S, "]"
def alternation(): return concat, -2, ("|", concat)

iecpeg = -2, production

files = fileinput.input("iec.grammar")
ast = parse(iecpeg, files, True, comment)

def genPEG(obj, genparens = True):
    result = ""
    if type(obj) == type([]):
        for e in range(len(obj)):
            text = genPEG(obj[e])
            m = re.compile(r"def [a-z_0-9]+\(\)\:").match(text)
            if e == 0:
                if not m and len(obj)>1 and genparens: result += "("
            result += text
            if e < len(obj) - 1:
                if m:
                    result += "\n"
                else:
                    result += ", "
            else:
                if not m and len(obj)>1 and genparens: result += ")"
    elif type(obj) == type((None,)):
        name = obj[0]
        if name == 'production':
            result += "def " + obj[1][0] + "(): return "
            for e in range(1,len(obj[1])):
                result += genPEG(obj[1][e])
                if e < len(obj[1]) - 1:
                    result += ", "
        elif name == "regex":
            result += 're.compile(r"' + obj[1][0] + '")'
        elif name == 'parentheses':
            for e in range(1,len(obj)):
                result += genPEG(obj[e])
        elif name == 'closure':
            result += "-1, "
            for e in range(1,len(obj)):
                result += genPEG(obj[e])
        elif name == 'option':
            result += "0, "
            for e in range(1,len(obj)):
                result += genPEG(obj[e])
        elif name == 'alternation':
            result += "["
            for e in range(1,len(obj)):
                result += genPEG(obj[e], False)
            result += "]"
        elif name == 'concat':
            for e in range(1,len(obj)):
                result += genPEG(obj[e])
    elif type(obj) == type(""):
        if obj[0] == "$":
            result += 'keyword(' + obj[1:] + ')'
        else:
            result += obj
    return result

# print ast
print "import re\nfrom pyPEG import keyword\n"
print genPEG(ast)

