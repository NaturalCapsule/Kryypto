import importlib, inspect

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

import tokenize
import io

_cache = {}
_cache_size_limit = 20

def list_classes_functions(code_text):
    func_class_instances = {}

    prev = None
    state = None

    if code_text in _cache:
        return _cache[code_text]
    
    # if len(code_text) > 100000:
    #     return {}

    func_class_instances = {}
    
    if not code_text.strip():
        return func_class_instances

    tokens = list(tokenize.generate_tokens(io.StringIO(code_text).readline))

    for i, (tok_type, tok_str, *_ ) in enumerate(tokens):
        # ---------- Class detection ----------
        if tok_type == tokenize.NAME and tok_str == "class":
            state = "class"
            continue
        elif state == "class" and tok_type == tokenize.NAME:
            func_class_instances[tok_str] = 'class'
            state = None

        # ---------- Function detection ----------
        if tok_type == tokenize.NAME and tok_str == "def":
            state = "def"
            continue
        elif state == "def" and tok_type == tokenize.NAME:
            func_class_instances[tok_str] = 'function'
            state = None

        # ---------- Imports ----------
        # if tok_type == tokenize.NAME and tok_str == "import":
        #     if state == "from":  # skip from-import
        #         state = None
        #         continue
        #     else:  # plain import
        #         state = "import"
        #         continue

        # elif tok_type == tokenize.NAME and tok_str == "from":
        #     # Skip from-import entirely
        #     state = "skip_from"
        #     continue

        # elif state == "import" and tok_type == tokenize.NAME:
        #     func_class_instances[tok_str] = 'import'

        # elif state == "from_import" and tok_type == tokenize.NAME:
        #     # tok_str is the imported name (Y)
        #     # current_from holds the module name parts ['X', ...]
        #     module_name = ".".join(current_from)  
        #     typ = classify_import(module_name, tok_str)
        #     func_class_instances[tok_str] = typ



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
                module_name = ".".join(current_from)
                typ = classify_import(module_name, tok_str)
                func_class_instances[tok_str] = typ
            elif tok_type == tokenize.OP and tok_str == ",":
                # multiple imports, just continue
                pass
            elif tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                state = None
            continue

        elif tok_type == tokenize.NAME and tok_str == "import":
            state = "import"
            continue

        elif state == "import":
            if tok_type == tokenize.NAME:
                func_class_instances[tok_str] = 'import'
            elif tok_type == tokenize.OP and tok_str == ",":
                pass  # multiple imports separated by commas
            elif tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                state = None
            continue


        # End of an import statement
        if tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
            state = None

        # ---------- Method calls ----------
        if (
            tok_type == tokenize.NAME
            and prev
            and prev[1] == "."
            and i + 1 < len(tokens)
            and tokens[i + 1][1] == "("  # ensure it's followed by '('
        ):
            func_class_instances[tok_str] = 'method'

        prev = (tok_type, tok_str)

    # tokens = tokenize.generate_tokens(io.StringIO(code_text).readline)

    # for tok_type, tok_str, *_ in tokens:
    #     # ---------- Class detection ----------
    #     if tok_type == tokenize.NAME and tok_str == "class":
    #         state = "class"
    #         continue
    #     elif state == "class" and tok_type == tokenize.NAME:
    #         func_class_instances[tok_str] = 'class'
    #         state = None

    #     # ---------- Function detection ----------
    #     if tok_type == tokenize.NAME and tok_str == "def":
    #         state = "def"
    #         continue
    #     elif state == "def" and tok_type == tokenize.NAME:
    #         func_class_instances[tok_str] = 'function'
    #         state = None

    #     # ---------- Imports ----------
    #     if tok_type == tokenize.NAME and tok_str == "import":
    #         if state == "from":  # skip from-import
    #             state = None
    #             continue
    #         else:  # plain import
    #             state = "import"
    #             continue

    #     elif tok_type == tokenize.NAME and tok_str == "from":
    #         # Skip from-import entirely
    #         state = "skip_from"
    #         continue

    #     elif state == "import" and tok_type == tokenize.NAME:
    #         func_class_instances[tok_str] = 'import'

    #     # End of an import statement
    #     if tok_type in (tokenize.NEWLINE, tokenize.ENDMARKER):
    #         state = None

    #     # ---------- Method calls ----------
    #     # if tok_type == tokenize.NAME and prev and prev[1] == ".":
    #     #     func_class_instances[tok_str] = 'method'

    #     if (
    #         tok_type == tokenize.NAME
    #         and prev
    #         and prev[1] == "."
    #         and i + 1 < len(tokens)
    #         and tokens[i + 1][1] == "("  # ensure it's followed by '('
    #     ):
    #         func_class_instances[tok_str] = 'method'

    #     prev = (tok_type, tok_str)

    if len(_cache) >= _cache_size_limit:
        _cache.pop(next(iter(_cache)))
    _cache[code_text] = func_class_instances
    
        # return func_class_instances

    return func_class_instances


# import parso


# import importlib
# import inspect

# _cache = {}
# _cache_size_limit = 20

# check_class = []

# def classify_import(module_name, attr_name):
#     try:
#         mod = importlib.import_module(module_name)
#         obj = getattr(mod, attr_name)
#         if inspect.isclass(obj):
#             return "class"
#         elif inspect.isfunction(obj):
#             return "function"
#         else:
#             return "variable"
#     except Exception:
#         return "import"

# def list_classes_functions(code):
#     try:
#         if code in _cache:
#             return _cache[code]
        
#         if len(code) > 100000:
#             return {}

#         func_class_instances = {}
        
#         if not code.strip():
#             return func_class_instances
        
#         try:
#             tree = parso.parse(code)
#         except Exception:
#             return {}
        
#         node_count = 0
#         max_nodes = 10000
        
#         def process_node(node, in_class=False, current_scope="", depth=0):
#             nonlocal node_count
            
#             # Safety checks
#             if node_count > max_nodes or depth > 50:
#                 return
#             node_count += 1
            
#             node_type = node.type

#             if node_type in ('funcdef', 'async_funcdef'):
#                 func_name_node = node.children[1]
#                 if hasattr(func_name_node, 'value'):
#                     func_name = func_name_node.value
#                     if in_class:
#                         func_class_instances[func_name] = 'method'
#                     else:
#                         func_class_instances[func_name] = 'function'

            
#             elif node_type == 'classdef':
#                 class_name_node = node.children[1]
#                 if hasattr(class_name_node, 'value'):
#                     class_name = class_name_node.value
#                     func_class_instances[class_name] = 'class'

#                 # Process all children inside the class with in_class=True
#                 if hasattr(node, 'children'):
#                     for child in node.children:
#                         process_node(child, in_class=True, current_scope=class_name, depth=depth + 1)
#                 return

#             elif node_type == 'expr_stmt' and len(node.children) >= 3:
#                 if (len(node.children) >= 3 and 
#                     node.children[1].type == 'operator' and 
#                     node.children[1].value == '='):
                    
#                     rhs = node.children[2]
                    
#                     if rhs.type == 'power' and len(rhs.children) >= 2:
#                         has_call = False
#                         for child in rhs.children:
#                             if child.type == 'trailer' and len(child.children) >= 2:
#                                 if (child.children[0].type == 'operator' and 
#                                     child.children[0].value == '('):
#                                     has_call = True
#                                     break
                        
#                         if has_call:
#                             first_child = rhs.children[0]
#                             if first_child.type == 'name':
#                                 func_name = first_child.value
#                                 func_class_instances[func_name] = 'class'
#                                 if current_scope:
#                                     full_name = f"{current_scope}.{func_name}"
#                                     func_class_instances[full_name] = 'class'
            
#             elif node_type == 'import_from':
#                 module_parts = []
#                 imported_names = []
                
#                 for child in node.children:
#                     if child.type == 'dotted_as_names' or child.type == 'import_as_names':
#                         for subchild in child.children:
#                             if subchild.type == 'name':
#                                 imported_names.append(subchild.value)
#                             elif subchild.type == 'dotted_as_name' or subchild.type == 'import_as_name':
#                                 for name_node in subchild.children:
#                                     if name_node.type == 'name':
#                                         imported_names.append(name_node.value)
#                                         break
#                     elif child.type == 'dotted_name':
#                         # Extract module name
#                         for subchild in child.children:
#                             if subchild.type == 'name':
#                                 module_parts.append(subchild.value)
#                     elif child.type == 'name' and child.value not in ('from', 'import'):
#                         if not module_parts:
#                             module_parts.append(child.value)
#                         else:
#                             imported_names.append(child.value)
                
#                 module_name = '.'.join(module_parts)
                
#                 for import_name in imported_names:
#                     if import_name and module_name:
#                         type_ = classify_import(module_name, import_name)
#                         func_class_instances[import_name] = type_
            
#             elif node_type == 'import_name':
#                 for child in node.children:
#                     if child.type == 'dotted_as_names':
#                         for subchild in child.children:
#                             if subchild.type == 'name':
#                                 func_class_instances[subchild.value] = 'module'
#                             elif subchild.type == 'dotted_as_name':
#                                 for name_node in subchild.children:
#                                     if name_node.type == 'name':
#                                         func_class_instances[name_node.value] = 'module'
#                                         break
            
#             elif node.type == 'trailer' and len(node.children) >= 2:
#                 first = node.children[0]
#                 second = node.children[1]

#                 if first.type == 'operator' and first.value == '.' and second.type == 'name':
#                     parent_children = getattr(node.parent, 'children', [])
#                     try:
#                         idx = parent_children.index(node)
#                         if (idx + 1 < len(parent_children) and
#                             parent_children[idx + 1].type == 'trailer' and
#                             parent_children[idx + 1].children[0].value == '('):
#                             # method_calls.append(second.value)
#                             func_class_instances[second.value] = 'method'

#                     except ValueError:
#                         pass

#             if hasattr(node, 'children'):
#                 for child in node.children:
#                     process_node(child, in_class, current_scope, depth + 1)
        
#         process_node(tree)
        
#         # Cache management
#         if len(_cache) >= _cache_size_limit:
#             _cache.pop(next(iter(_cache)))
#         _cache[code] = func_class_instances
        
#         return func_class_instances
        
#     except Exception as e:
#         print(f"Parso analysis error: {e}")
#         return {}

# import ast
# import importlib
# import inspect

# _cache = {}
# _cache_size_limit = 20  # Reduced cache size for better memory usage

# check_class = []

# def classify_import(module_name, attr_name):
#     try:
#         mod = importlib.import_module(module_name)
#         obj = getattr(mod, attr_name)
#         if inspect.isclass(obj):
#             return "class"
#         elif inspect.isfunction(obj):
#             return "function"
#         else:
#             return "variable"
#     except Exception:
#         return "import"

# def list_classes_functions(code):
#     try:
#         if code in _cache:
#             return _cache[code]
        
#         if len(code) > 100000:
#         # if len(code) > 2000:

#             return {}


#         func_class_instances = {}
        
#         if not code.strip():
#             return func_class_instances
            
#         tree = ast.parse(code)
        
#         scope_stack = []
#         node_count = 0
#         max_nodes = 10000
        
#         def process_node(node, in_class=False, current_scope="", depth=0):
#             nonlocal node_count
            
#             if node_count > max_nodes:
#                 return
                
#             if depth > 50:
#                 return
                
#             node_count += 1
                
#             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
#                 if in_class:
#                     method_name = node.name
#                     func_class_instances[method_name] = 'method'
                
#                 for child in node.body:
#                     process_node(child, in_class, current_scope, depth + 1)
                    
#             elif isinstance(node, ast.Assign):
#                 for target in node.targets:
#                     if isinstance(target, ast.Name):
#                         if isinstance(node.value, ast.Call):
#                             if isinstance(node.value.func, ast.Name):
#                                 func_name = node.value.func.id
#                                 func_class_instances[func_name] = 'class'
#                                 print(func_name)
#                                 if current_scope:
#                                     full_func_name = f"{current_scope}.{func_name}"
#                                     func_class_instances[full_func_name] = 'class'

#                             elif isinstance(node.value.func, ast.Attribute):
#                                 attr_name = node.value.func.attr
#                                 func_class_instances[attr_name] = 'function'
#                                 if current_scope:
#                                     full_attr_name = f"{current_scope}.{attr_name}"
#                                     func_class_instances[full_attr_name] = 'function'

#             # elif isinstance(node, ast.ImportFrom) and isinstance(node, ast.Attribute):
#             #     print("True")
#             #     for alias in node.names:
#             #         import_name = alias.name
#             #         # check_class.append(import_name)
#             #         func_class_instances[import_name] = 'function'
#             #         print(import_name)
#             #         if current_scope:
#             #             func_class_instances[import_name] = 'function'


#             # elif isinstance(node, ast.ImportFrom):
#             #     for alias in node.names:
#             #         import_name = alias.name
#             #         check_class.append(import_name)
#             #         if import_name not in func_class_instances or func_class_instances[import_name] != 'function':
#             #             func_class_instances[import_name] = 'import'
#             #             if current_scope:
#             #                 func_class_instances[import_name] = 'import'


#             elif isinstance(node, ast.ImportFrom):
#                 module_name = node.module




#                 for alias in node.names:
#                     import_name = alias.name
#                     type_ = classify_import(module_name, import_name)
#                     func_class_instances[import_name] = type_
#                     # obj = getattr(module, import_name, None)

#                     # if inspect.isclass(obj):
#                     #     func_class_instances[import_name] = 'class'
#                     # elif inspect.isfunction(obj):
#                     #     func_class_instances[import_name] = 'function'
#                     # else:
#                     #     func_class_instances[import_name] = 'variable'

#         # elif isinstance(node, ast.Import):
#         #     for alias in node.names:
#         #         func_class_instances[alias.name] = 'module'


#             elif isinstance(node, ast.Call):
#                 if isinstance(node.func, ast.Name):
#                     func_name = node.func.id
#                     if func_name not in check_class:
#                         # print(func_name)
#                         func_class_instances[func_name] = 'function'
#                         if current_scope:
#                             full_func_name = f"{current_scope}.{func_name}"
#                             func_class_instances[full_func_name] = 'function'
#                 elif isinstance(node.func, ast.Attribute):
#                     attr_name = node.func.attr
#                     func_class_instances[attr_name] = 'method'
#                     if current_scope:
#                         full_attr_name = f"{current_scope}.{attr_name}"
#                         func_class_instances[full_attr_name] = 'method'
                        
#             elif isinstance(node, ast.Attribute):
#                 attr_name = node.attr
#                 if attr_name not in func_class_instances or func_class_instances[attr_name] != 'method':
#                     func_class_instances[attr_name] = 'attribute'
#                     # print(func_name)

#                     if current_scope:
#                         full_attr_name = f"{current_scope}.{attr_name}"
#                         func_class_instances[full_attr_name] = 'attribute'
            
#             for child in ast.iter_child_nodes(node):
#                 process_node(child, in_class, current_scope, depth + 1)
        
#         for node in tree.body:
#             process_node(node)
        
#         if len(_cache) >= _cache_size_limit:
#             _cache.pop(next(iter(_cache)))
#         _cache[code] = func_class_instances
#         return func_class_instances
#     except Exception:
#         return {}




# import importlib
# import inspect
# import parso

# _cache = {}
# _cache_size_limit = 20
# check_class = []

# def classify_import(module_name, attr_name):
#     try:
#         mod = importlib.import_module(module_name)
#         obj = getattr(mod, attr_name)
#         if inspect.isclass(obj):
#             return "class"
#         elif inspect.isfunction(obj):
#             return "function"
#         else:
#             return "variable"
#     except Exception:
#         return "import"

# def list_classes_functions(code):
#     try:
#         if code in _cache:
#             return _cache[code]

#         if len(code) > 100000:
#             return {}

#         func_class_instances = {}

#         if not code.strip():
#             return func_class_instances

#         # Parse code with parso
#         tree = parso.parse(code)

#         def process_node(node, in_class=False, current_scope="", depth=0):
#             if depth > 50:
#                 return

#             node_type = node.type
#             node_value = getattr(node, "value", None)

#             # Class definitions
#             if node_type == "classdef":
#                 class_name = node.name.value
#                 func_class_instances[class_name] = "class"
#                 for child in node.children:
#                     process_node(child, in_class=True, current_scope=class_name, depth=depth + 1)

#             # Function definitions
#             elif node_type == "funcdef":
#                 func_name = node.name.value
#                 if in_class:
#                     func_class_instances[func_name] = "method"
#                 else:
#                     func_class_instances[func_name] = "function"
#                 for child in node.children:
#                     process_node(child, in_class=in_class, current_scope=current_scope, depth=depth + 1)

#             # from ... import ...
#             elif node_type == "import_from":
#                 # print(module_name)
#                 module_name = ".".join(n.value for n in node.get_from_names() if hasattr(n, "value"))
#                 for alias in node.get_import_names():
#                     import_name = alias.value
#                     type_ = classify_import(module_name, import_name)
#                     func_class_instances[import_name] = type_
#                     print(import_name)

#             # import ...
#             elif node_type == "import_name":
#                 for alias in node.get_import_names():
#                     func_class_instances[alias.value] = "import"

#             # Attributes (obj.attr)
#             elif node_type == "atom_expr" and len(node.children) >= 2:
#                 # Detect attribute usage
#                 if node.children[1].type == "trailer" and node.children[1].children[0].value == ".":
#                     attr_name = node.children[1].children[1].value
#                     if attr_name not in func_class_instances:
#                         func_class_instances[attr_name] = "attribute"

#             # Recursive traversal
#             if hasattr(node, "children"):
#                 for child in node.children:
#                     process_node(child, in_class=in_class, current_scope=current_scope, depth=depth + 1)

#         process_node(tree)

#         # Cache result
#         if len(_cache) >= _cache_size_limit:
#             _cache.pop(next(iter(_cache)))
#         _cache[code] = func_class_instances
#         return func_class_instances

#     except Exception:
#         return {}



# import ast
# import importlib
# import importlib.util
# import inspect
# import re
# from functools import lru_cache

# _cache = {}
# _cache_size_limit = 20
# # optional: set False if you don't want runtime importing (safer, faster)
# ENABLE_RUNTIME_INTROSPECTION = False

# @lru_cache(maxsize=256)
# def classify_import_cached(module_name, attr_name):
#     """
#     Try to import module_name and inspect attr_name.
#     Returns one of: 'class', 'function', 'module' (submodule), 'variable', 'import' (fallback)
#     """
#     # quick guards
#     if not module_name or not attr_name or attr_name == '*':
#         return 'import'

#     if not ENABLE_RUNTIME_INTROSPECTION:
#         # heuristic fallback (UpperCamelCase -> class, lower_with_underscores -> function)
#         if attr_name[0].isupper():
#             return 'class'
#         if attr_name.islower():
#             return 'function'
#         return 'import'

#     try:
#         # try importing the module (may raise)
#         mod = importlib.import_module(module_name)

#         # attribute might be a submodule (from package import submodule)
#         # check if module_name.attr_name refers to a module
#         sub_spec = importlib.util.find_spec(f"{module_name}.{attr_name}")
#         if sub_spec is not None:
#             return 'import'   # treat submodule as import/module

#         obj = getattr(mod, attr_name, None)
#         if obj is None:
#             # maybe attribute not present; fallback to heuristic
#             if attr_name[0].isupper():
#                 return 'class'
#             if attr_name.islower():
#                 return 'function'
#             return 'import'

#         if inspect.isclass(obj):
#             return 'class'
#         if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isbuiltin(obj):
#             return 'function'
#         if inspect.ismodule(obj):
#             return 'import'
#         # other callables / descriptors
#         if callable(obj):
#             return 'function'
#         return 'variable'
#     except Exception:
#         # If import/inspection fails, use safe heuristic
#         if attr_name and attr_name[0].isupper():
#             return 'class'
#         if attr_name and attr_name.islower():
#             return 'function'
#         return 'import'


# def list_classes_functions(code):
#     try:
#         if code in _cache:
#             return _cache[code]

#         # if len(code) > 100000:
#         #     return {}

#         func_class_instances = {}

#         if not code.strip():
#             return func_class_instances

#         tree = ast.parse(code)
#         node_count = 0
#         max_nodes = 10000

#         def process_node(node, current_scope=""):
#             nonlocal node_count
#             if node_count > max_nodes:
#                 return
#             node_count += 1

#             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
#                 if current_scope:
#                     func_class_instances[node.name] = 'method'
#                 else:
#                     func_class_instances[node.name] = 'function'

#             # handle assignments like a = SomeClass()
#             elif isinstance(node, ast.Assign):
#                 # simple detection for var = ClassOrCall()
#                 if isinstance(node.value, ast.Call):
#                     if isinstance(node.value.func, ast.Name):
#                         func_name = node.value.func.id
#                         func_class_instances[func_name] = 'class'
#                     elif isinstance(node.value.func, ast.Attribute):
#                         func_class_instances[node.value.func.attr] = 'function'

#                     # elif isinstance(node.func, ast.Attribute):
#                     #     func_class_instances[node.func.attr] = 'function'

#             # handle "from X import A, B as C"
#             elif isinstance(node, ast.ImportFrom):
#                 module_name = node.module  # can be None for relative imports
#                 for alias in node.names:
#                     if alias.name == '*':
#                         continue
#                     original_name = alias.name
#                     used_name = alias.asname if alias.asname else original_name

#                     type_ = classify_import_cached(module_name or "", original_name)
#                     # record under the used name (respecting as alias)
#                     func_class_instances[used_name] = type_

#             # handle "import x, y as z"
#             elif isinstance(node, ast.Import):
#                 for alias in node.names:
#                     full_mod = alias.name  # can be 'package.submodule'
#                     top_name = full_mod.split('.')[0]
#                     used_name = alias.asname if alias.asname else top_name
#                     # an import like "import os.path" we classify as 'import'
#                     func_class_instances[used_name] = 'import'

#             # elif isinstance(node.func, ast.Attribute):
#             #     attr_name = node.func.attr
#             #     func_class_instances[attr_name] = 'method'
#             #     if current_scope:
#             #         full_attr_name = f"{current_scope}.{attr_name}"
#             #         func_class_instances[full_attr_name] = 'method'

#             # recurse children
#             for child in ast.iter_child_nodes(node):
#                 process_node(child, current_scope)

#         for node in tree.body:
#             process_node(node)

#         # maintain small cache for parsed code -> mapping
#         if len(_cache) >= _cache_size_limit:
#             _cache.pop(next(iter(_cache)))
#         _cache[code] = func_class_instances
#         return func_class_instances
#     except Exception:
#         return {}
