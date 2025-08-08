import ast

_cache = {}
_cache_size_limit = 20  # Reduced cache size for better memory usage

check_class = []

def list_classes_functions(code):
    try:
        if code in _cache:
            return _cache[code]
        
        if len(code) > 100000:
        # if len(code) > 2000:

            return {}


        func_class_instances = {}
        
        if not code.strip():
            return func_class_instances
            
        tree = ast.parse(code)
        
        scope_stack = []
        node_count = 0
        max_nodes = 10000
        
        def process_node(node, in_class=False, current_scope="", depth=0):
            nonlocal node_count
            
            if node_count > max_nodes:
                return
                
            if depth > 50:
                return
                
            node_count += 1
                
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if in_class:
                    method_name = node.name
                    func_class_instances[method_name] = 'method'
                
                for child in node.body:
                    process_node(child, in_class, current_scope, depth + 1)
                    
            elif isinstance(node, ast.Assign):
                # Get variable assignments
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if isinstance(node.value, ast.Call):
                            if isinstance(node.value.func, ast.Name):
                                func_name = node.value.func.id
                                func_class_instances[func_name] = 'class'

                                if current_scope:
                                    full_func_name = f"{current_scope}.{func_name}"
                                    func_class_instances[full_func_name] = 'class'

                            elif isinstance(node.value.func, ast.Attribute):
                                attr_name = node.value.func.attr
                                func_class_instances[attr_name] = 'function'
                                if current_scope:
                                    full_attr_name = f"{current_scope}.{attr_name}"
                                    func_class_instances[full_attr_name] = 'function'

            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    import_name = alias.name
                    check_class.append(import_name)
                    func_class_instances[import_name] = 'import'
                    if current_scope:
                        func_class_instances[import_name] = 'import'
                        
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name not in check_class:
                        func_class_instances[func_name] = 'function'
                        if current_scope:
                            full_func_name = f"{current_scope}.{func_name}"
                            func_class_instances[full_func_name] = 'function'
                elif isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    func_class_instances[attr_name] = 'method'
                    if current_scope:
                        full_attr_name = f"{current_scope}.{attr_name}"
                        func_class_instances[full_attr_name] = 'method'
                        
            elif isinstance(node, ast.Attribute):
                attr_name = node.attr
                if attr_name not in func_class_instances or func_class_instances[attr_name] != 'method':
                    func_class_instances[attr_name] = 'attribute'
                    if current_scope:
                        full_attr_name = f"{current_scope}.{attr_name}"
                        func_class_instances[full_attr_name] = 'attribute'
            
            for child in ast.iter_child_nodes(node):
                process_node(child, in_class, current_scope, depth + 1)
        
        for node in tree.body:
            process_node(node)
        
        if len(_cache) >= _cache_size_limit:
            _cache.pop(next(iter(_cache)))
        _cache[code] = func_class_instances
        return func_class_instances
    except Exception:
        return {}