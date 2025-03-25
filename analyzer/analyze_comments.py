import typer
import re

def count_comments(code: str) -> int:
    """Conta o número de comentários no código."""
    comment_lines = 0
    for line in code.split("\n"):
        stripped_line = line.strip()
        if "#" in stripped_line:
            comment_lines += 1
            stripped_line = stripped_line.split("#")[0].strip()  # Remove o comentário
            if not stripped_line:
                continue  # Se só tinha um comentário, não conta como código
    return comment_lines

def analyze_comments(file: str):
    """Comando CLI para contar comentários."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    comment_count = count_comments(code)
    typer.echo(f"Comentários: {comment_count}")