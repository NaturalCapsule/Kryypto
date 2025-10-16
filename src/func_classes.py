import importlib, inspect
import io
import tokenize
import ast

_cache = {}
_cache_size_limit = 1000

# class UsedVarsVisitor(ast.NodeVisitor):
#     def __init__(self):
#         self.used_vars = set()

#     def visit_Name(self, node):
#         if isinstance(node.ctx, ast.Load):
#             self.used_vars.add(node.id)
#         self.generic_visit(node)

#     def visit_Attribute(self, node):
#         if isinstance(node.ctx, ast.Load):
#             if isinstance(node.value, ast.Name):
#                 full_name = f"{node.value.id}.{node.attr}"
#                 self.used_vars.add(full_name)
#         self.generic_visit(node)

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
