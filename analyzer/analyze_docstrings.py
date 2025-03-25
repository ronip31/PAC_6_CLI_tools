import typer
import ast

def count_docstrings(code: str) -> int:
    """Conta a quantidade de docstrings no código."""
    tree = ast.parse(code)
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str))

def analyze_docstrings(file: str):
    """Comando CLI para contar docstrings."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    docstring_count = count_docstrings(code)
    typer.echo(f"Docstrings: {docstring_count}")
