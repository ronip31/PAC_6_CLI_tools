import typer
import ast
from typing import Tuple

def count_methods(code: str) -> Tuple[int, int]:
    """
    Conta o número de métodos públicos e privados nas classes do código.
    Retorna uma tupla (métodos_públicos, métodos_privados).
    """
    tree = ast.parse(code)
    public_methods = 0
    private_methods = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Métodos que começam com __ são considerados privados
                    if item.name.startswith('__') and item.name.endswith('__'):
                        # Ignora métodos especiais como __init__, __str__, etc
                        continue
                    elif item.name.startswith('_'):
                        private_methods += 1
                    else:
                        public_methods += 1
    
    return public_methods, private_methods

def analyze_methods(file: str):
    """Comando CLI para analisar métodos públicos e privados."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    
    public_count, private_count = count_methods(code)
    total_methods = public_count + private_count
    
    typer.echo(f"Análise de Métodos:")
    typer.echo(f"Métodos Públicos: {public_count}")
    typer.echo(f"Métodos Privados: {private_count}")
    typer.echo(f"Total de Métodos: {total_methods}")
    if total_methods > 0:
        public_ratio = (public_count / total_methods) * 100
        private_ratio = (private_count / total_methods) * 100
        typer.echo(f"Proporção Público/Privado: {public_ratio:.1f}% / {private_ratio:.1f}%") 