import ast

get_c_instances = set()
get_funcs = set()



def list_classes_functions(code):
    try:
        get_c_instances.clear()
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    class_name = node.value.func.id
                    if class_name == 'int' or class_name == 'len' or class_name == 'str':
                        continue
                    else:
                        get_c_instances.add(class_name)

                elif isinstance(node, ast.Call):
                    func = node.func
                    if isinstance(func, ast.Attribute):
                        get_funcs.add(func.attr)
                        # print(f"{func.attr}")


        return get_c_instances

    except Exception:
        get_c_instances.clear()
        return get_c_instances