import ast

def analyze_dead_code(code: str):
    tree = ast.parse(code)
    defined_funcs = set()
    defined_classes = set()
    used_funcs = set()
    used_classes = set()

    class DeadCodeVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            defined_funcs.add(node.name)
            self.generic_visit(node)
        def visit_ClassDef(self, node):
            defined_classes.add(node.name)
            self.generic_visit(node)
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                used_funcs.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                used_funcs.add(node.func.attr)
            self.generic_visit(node)
        def visit_Attribute(self, node):
            # Para instanciamento de classes
            if isinstance(node.value, ast.Name):
                used_classes.add(node.value.id)
            self.generic_visit(node)
        def visit_Name(self, node):
            # Para instanciamento de classes
            if node.id in defined_classes:
                used_classes.add(node.id)
            self.generic_visit(node)

    DeadCodeVisitor().visit(tree)
    dead_funcs = sorted(list(defined_funcs - used_funcs))
    dead_classes = sorted(list(defined_classes - used_classes))
    return {
        "dead_functions": dead_funcs,
        "dead_classes": dead_classes
    }

def analyze_dead_code_cli(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    result = analyze_dead_code(code)
    print(f"\n🪦 Código Morto em {file_path}:")
    if result["dead_functions"]:
        print("Funções não utilizadas:")
        for func in result["dead_functions"]:
            print(f"  - {func}")
    else:
        print("Nenhuma função morta encontrada.")
    if result["dead_classes"]:
        print("Classes não utilizadas:")
        for cls in result["dead_classes"]:
            print(f"  - {cls}")
    else:
        print("Nenhuma classe morta encontrada.") 