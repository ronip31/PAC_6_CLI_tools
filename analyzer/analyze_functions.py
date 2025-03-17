import typer
import ast

def count_functions(code: str) -> int:
    """Conta o número de funções no código."""
    tree = ast.parse(code)
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))

def analyze_functions_command(file: str):
    """Comando CLI para contar funções."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    function_count = count_functions(code)
    typer.echo(f"Funções: {function_count}")
