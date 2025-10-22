from collections import defaultdict
from pygments.lexers import BashLexer
from pygments import lex

def get_elements(code):
    types_elements = defaultdict(list)
    tokens = lex(code, BashLexer())

    for token_type, value in tokens:
        if value.strip():  # ignore whitespace
            types_elements[str(token_type)].append(value)

    return types_elements