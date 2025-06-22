import ast, jedi

# func_class_instances = {}

# def list_classes_functions(code):
#     try:
#         func_class_instances.clear()
#         tree = ast.parse(code)
#         script = jedi.Script(code)
#         names = script.get_names(all_scopes=True, definitions=True)

#         for name in names:
#             if name.type == 'class' or name.type == 'module':
#                 func_class_instances[name.name] = 'class'
#             elif name.type == 'function':
#                 func_class_instances[name.name] = 'function'

#         for node in ast.walk(tree):
#             if isinstance(node, ast.Assign):
#                 if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
#                     class_name = node.value.func.id
#                     if class_name == 'int' or class_name == 'len' or class_name == 'str':
#                         continue
#                     else:
#                         func_class_instances[class_name] = 'class'

#             elif isinstance(node, ast.Call):
#                 func = node.func
#                 if isinstance(func, ast.Attribute):
#                     func_class_instances[func.attr] = 'function'


#         return func_class_instances

#     except Exception:
#         func_class_instances.clear()
#         return func_class_instances

# func_classes.py
import ast, jedi

def list_classes_functions(code):
    try:
        func_class_instances = {}
        tree = ast.parse(code)
        script = jedi.Script(code)
        names = script.get_names(all_scopes=True, definitions=True)

        for name in names:
            if name.type in ['class', 'module']:
                func_class_instances[name.name] = 'class'
            elif name.type == 'function':
                func_class_instances[name.name] = 'function'

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    class_name = node.value.func.id
                    if class_name not in ('int', 'len', 'str'):
                        func_class_instances[class_name] = 'class'
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    func_class_instances[func.attr] = 'function'

        return func_class_instances

    except Exception:
        return {}
