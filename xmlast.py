from xml.sax.saxutils import escape


def pyAST2XML(pyAST):
    if isinstance(pyAST, str):
        return escape(pyAST)
    if isinstance(pyAST, tuple):
        result = "<" + pyAST[0].replace("_", "-") + ">"
        for e in pyAST[1:]:
            result += pyAST2XML(e)
        result += "</" + pyAST[0].replace("_", "-") + ">"
    else:
        result = ""
        for e in pyAST:
            result += pyAST2XML(e)
    return result
