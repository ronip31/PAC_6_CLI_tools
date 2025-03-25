import typer
from analyzer.analyze_lines import analyze_lines, count_lines
from analyzer.analyze_comments import analyze_comments, count_comments
from analyzer.analyze_docstrings import analyze_docstrings, count_docstrings
from analyzer.analyze_classes import analyze_classes, count_classes
from analyzer.analyze_functions import analyze_functions, count_functions

app = typer.Typer(help="""
Ferramenta CLI para análise de código Python.

Esta aplicação permite analisar diferentes aspectos de um código Python, incluindo:
- Contagem de linhas
- Contagem de comentários
- Contagem de docstrings
- Contagem de classes
- Contagem de funções

Use os comandos individuais para análises específicas ou o comando `analyze-all` para uma análise completa.
""")

@app.command(help="Analisa todas as métricas do código, incluindo linhas, comentários, docstrings, classes e funções.")
def analyze_all(file: str):
    """Analisa todas as métricas do código em um único comando."""
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()

    line_count = count_lines(code)
    comment_count = count_comments(code)
    docstring_count = count_docstrings(code)
    class_count = count_classes(code)
    function_count = count_functions(code)

    typer.echo(f"Arquivo: {file}")
    typer.echo(f"Total de linhas: {line_count}")
    typer.echo(f"Comentários: {comment_count}")
    typer.echo(f"Docstrings: {docstring_count}")
    typer.echo(f"Classes: {class_count}")
    typer.echo(f"Funções: {function_count}")

# Registrando os comandos individuais corretamente
app.command(help="Conta o número total de linhas no código.")(analyze_lines)
app.command(help="Conta o número de comentários no código.")(analyze_comments)
app.command(help="Conta a quantidade de docstrings no código.")(analyze_docstrings)
app.command(help="Conta o número de classes no código.")(analyze_classes)
app.command(help="Conta o número de funções no código.")(analyze_functions)

if __name__ == "__main__":
    app()
