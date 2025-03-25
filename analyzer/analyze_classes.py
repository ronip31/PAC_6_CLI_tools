import typer
import ast

def count_classes(code: str) -> int:
    """Conta o número de classes no código."""
    tree = ast.parse(code)
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))

def analyze_classes(file: str):
    """Comando CLI para contar classes."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    class_count = count_classes(code)
    typer.echo(f"Classes: {class_count}")
