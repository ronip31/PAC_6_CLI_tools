import ast

def estimate_complexity(func_code: str) -> str:
    tree = ast.parse(func_code)
    max_depth = [0]
    def visit(node, depth=0):
        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            max_depth[0] = max(max_depth[0], depth)
        for child in ast.iter_child_nodes(node):
            visit(child, depth)
    visit(tree)
    if max_depth[0] == 0:
        return "O(1)"
    elif max_depth[0] == 1:
        return "O(n)"
    elif max_depth[0] == 2:
        return "O(n^2)"
    else:
        return f"O(n^{max_depth[0]})"

def analyze_complexity_code(code: str):
    tree = ast.parse(code)
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_code = ast.get_source_segment(code, node)
            complexity = estimate_complexity(func_code)
            results.append({
                'function': node.name,
                'complexity': complexity
            })
    return results

def analyze_complexity(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    results = analyze_complexity_code(code)
    print(f"\n📈 Análise Assintótica das Funções em {file_path}:")
    for r in results:
        print(f"Função: {r['function']}, Complexidade Estimada: {r['complexity']}")
    if not results:
        print("Nenhuma função encontrada.") 