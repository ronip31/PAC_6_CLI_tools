import typer

def count_lines(code: str) -> int:
    """Conta o número total de linhas no código."""
    return len(code.splitlines())

def analyze_lines(file: str):
    """Comando CLI para contar linhas de código."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    line_count = count_lines(code)
    typer.echo(f"Total de linhas: {line_count}")
