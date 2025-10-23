import importlib, inspect
import io
import tokenize
import ast

_cache = {}
_cache_size_limit = 1000


class UnusedVariableFinder(ast.NodeVisitor):
    def __init__(self):
        self.assigned = set()
        self.used = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assigned.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):  
            self.used.add(node.id)
        self.generic_visit(node)

def classify_import(module_name, attr_name):
    try:
        mod = importlib.import_module(module_name)
        obj = getattr(mod, attr_name)
        if inspect.isclass(obj):
            return "class"
        elif inspect.isfunction(obj):
            return "function"
    except Exception:
        return "import"


def list_classes_functions(code_text: str):
    if not code_text or not code_text.strip():
        return {}

    func_class_instances = {}
    state = None
    current_func = None
    collecting_args = False
    args = []
    prev = None

    seen = set()

    try:



        tree = ast.parse(code_text)
        finder = UnusedVariableFinder()
        finder.visit(tree)

        unused = finder.assigned - finder.used
        for unuse in unused:
            func_class_instances[unuse] = 'unused'


        tokens = list(tokenize.generate_tokens(io.StringIO(code_text).readline))

        for i, (tok_type, tok_str, *_ ) in enumerate(tokens):
            # ---------- class ----------
            if tok_type == tokenize.NAME and tok_str == "class":
                state = "class"
                continue
            elif state == "class" and tok_type == tokenize.NAME:
                func_class_instances[tok_str] = "class"
                state = None
                continue

            # ---------- def ----------
            if tok_type == tokenize.NAME and tok_str == "def":
                state = "def"
                continue
            elif state == "def" and tok_type == tokenize.NAME:
                current_func = tok_str
                func_class_instances[current_func] = "function"
                args = []
                collecting_args = False
                state = None
                continue

            # ---------- args collection ----------
            if current_func and tok_str == "(":
                collecting_args = True
                continue
            if current_func and tok_str == ")":
                if args:
                    for a in args:
                        if a not in seen:
                            func_class_instances[a] = "args"
                current_func = None
                collecting_args = False
                args = []
                continue
            if collecting_args and tok_type == tokenize.NAME:
                args.append(tok_str)
                continue

            # ---------- imports (static, no importlib) ----------
            if tok_type == tokenize.NAME and tok_str == "from":
                state = "from"
                current_from = []
                continue
            elif state == "from" and tok_type == tokenize.NAME and tok_str != "import":
                current_from.append(tok_str)
                continue
            elif state == "from" and tok_type == tokenize.NAME and tok_str == "import":
                state = "from_import"
                continue
            elif state == "from_import":
                if tok_type == tokenize.NAME:
                    # typ = classify_import(tok_str)  # heuristic only
                    try:
                        mod = importlib.import_module(tok_str)
                        # obj = getattr(mod, attr_name)


                        if inspect.isclass(mod):
                            func_class_instances[tok_str] = 'class'
                            # return "class"
                        elif inspect.isfunction(mod):
                            func_class_instances[tok_str] = 'function'
                            # return "function"
                    except Exception:
                        func_class_instances[tok_str] = 'import'
                        # return "import"



                    # func_class_instances[tok_str] = typ

                    seen.add(tok_str)
                elif tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                    state = None
                continue

            if tok_type == tokenize.NAME and tok_str == "import":
                state = "import"
                continue
            elif state == "import":
                if tok_type == tokenize.NAME:
                    # we don’t try to decide function vs class here
                    func_class_instances[tok_str] = "import"
                    seen.add(tok_str)
                elif tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                    state = None
                continue

            # ---------- method calls (foo.bar(...)) ----------
            if (
                tok_type == tokenize.NAME
                and prev
                and prev[0] == tokenize.OP
                and prev[1] == "."
            ):
                next_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                if next_tok and next_tok[1] == "(":
                    func_class_instances[tok_str] = "method"

            # reset on newline
            if tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                state = None

            prev = (tok_type, tok_str)

    except tokenize.TokenError:
        # pass
        return func_class_instances

    return func_class_instances


# import importlib.util, io, tokenize, ast, hashlib

# _last_code_hash = None
# _last_result = None

# class UnusedVariableFinder(ast.NodeVisitor):
#     def __init__(self):
#         self.assigned, self.used = set(), set()
#     def visit_Assign(self, node):
#         for t in node.targets:
#             if isinstance(t, ast.Name):
#                 self.assigned.add(t.id)
#         self.generic_visit(node)
#     def visit_Name(self, node):
#         if isinstance(node.ctx, ast.Load):
#             self.used.add(node.id)

# def list_classes_functions(code_text: str):
#     global _last_code_hash, _last_result

#     if not code_text.strip():
#         return {}

#     code_hash = hashlib.sha1(code_text.encode()).hexdigest()
#     if code_hash == _last_code_hash:
#         return _last_result

#     func_class_instances = {}
#     seen = set()

#     try:
#         # Parse AST once
#         tree = ast.parse(code_text)
#         finder = UnusedVariableFinder()
#         finder.visit(tree)
#         unused = finder.assigned - finder.used
#         for unuse in unused:
#             func_class_instances[unuse] = 'unused'

#         # Tokenize efficiently
#         tokens = tokenize.generate_tokens(io.StringIO(code_text).readline)
#         prev = None
#         state = None
#         current_func, collecting_args, args = None, False, []

#         for tok_type, tok_str, *_ in tokens:
#             if tok_type == tokenize.NAME and tok_str in ("class", "def", "from", "import"):
#                 state = tok_str
#                 continue

#             # Handle class/function names
#             if state == "class":
#                 func_class_instances[tok_str] = "class"
#                 state = None
#             elif state == "def":
#                 current_func = tok_str
#                 func_class_instances[current_func] = "function"
#                 state = None
#             elif state == "from":
#                 state = "from_import"
#             elif state == "from_import" and tok_type == tokenize.NAME:
#                 if importlib.util.find_spec(tok_str):
#                     func_class_instances[tok_str] = "import"
#                 seen.add(tok_str)
#             elif state == "import" and tok_type == tokenize.NAME:
#                 if importlib.util.find_spec(tok_str):
#                     func_class_instances[tok_str] = "import"
#                 seen.add(tok_str)

#             # Collect function args
#             if current_func:
#                 if tok_str == "(":
#                     collecting_args = True
#                 elif tok_str == ")":
#                     for a in args:
#                         func_class_instances[a] = "args"
#                     current_func = None
#                     args.clear()
#                     collecting_args = False
#                 elif collecting_args and tok_type == tokenize.NAME:
#                     args.append(tok_str)

#             # Detect methods (obj.method())
#             if tok_type == tokenize.NAME and prev and prev[1] == ".":
#                 func_class_instances[tok_str] = "method"

#             prev = (tok_type, tok_str)

#     except Exception:
#         pass

#     _last_code_hash = code_hash
#     _last_result = func_class_instances
#     return func_class_instances
