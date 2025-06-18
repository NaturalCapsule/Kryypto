import ast

func_class_instances = {}

def list_classes_functions(code):
    try:
        func_class_instances.clear()
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    class_name = node.value.func.id
                    if class_name == 'int' or class_name == 'len' or class_name == 'str':
                        continue
                    else:
                        func_class_instances[class_name] = 'class'


            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    func_class_instances[func.attr] = 'function'


        return func_class_instances

    except Exception:
        func_class_instances.clear()
        return func_class_instances
