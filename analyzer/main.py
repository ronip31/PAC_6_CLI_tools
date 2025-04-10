import typer
from analyzer.analyze_lines import analyze_lines, count_lines
from analyzer.analyze_comments import analyze_comments, count_comments
from analyzer.analyze_docstrings import analyze_docstrings, count_docstrings
from analyzer.analyze_classes import analyze_classes, count_classes
from analyzer.analyze_functions import analyze_functions, count_functions
from analyzer.analyze_indentation import analyze_indentation, count_indentation



from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

app = typer.Typer(
    help="Ferramenta CLI para análise de código Python.",
    add_completion=False,
    invoke_without_command=True
)

console = Console()

# Callback para --version ou exibição personalizada de ajuda
@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Mostra a versão e sai."),
    help_: bool = typer.Option(False, "--help", is_eager=True, help="Mostra esta mensagem e sai.")
):
    if version:
        typer.secho("📦 Analyzer CLI - Versão 1.0.0", fg=typer.colors.GREEN, bold=True)
        raise typer.Exit()

    if help_:
        console = Console()
        help_text = """
# 🧠 Analyzer CLI

Ferramenta CLI para análise de código Python.

## 📦 Comandos principais
- `all`               → Analisa todas as métricas de uma vez
- `lines`             → Conta o total de linhas de código
- `comments`          → Conta o total de comentários
- `docstrings`        → Conta as docstrings
- `classes`           → Conta as classes
- `functions`         → Conta as funções
- `indent`            → Analisa os níveis de indentação

## 🧪 Comandos auxiliares (via terminal)
- `runtests`              → Roda todos os testes
- `runtests-verbose`      → Roda testes com saída detalhada
- `runtests-failures`     → Roda somente os testes que falharam anteriormente

## 💡 Exemplo
```bash
analyzer all examples/sample.py
    """
        console.print(Markdown(help_text))
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.secho("⚠️ Nenhum comando fornecido. Use '--help' para ver os comandos disponíveis.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)




# Comando para análise completa
@app.command("all", help="Analisa todas as métricas do código (linhas, comentários, docstrings, classes e funções).")
def analyze_all(file: str = typer.Argument(..., help="Caminho para o arquivo Python a ser analisado.")):
    """Analisa todas as métricas do código em um único comando."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        typer.secho(f"Arquivo não encontrado: {file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # Contagens
    line_count = count_lines(code)
    comment_count = count_comments(code)
    docstring_count = count_docstrings(code)
    class_count = count_classes(code)
    function_count = count_functions(code)
    indent_result = count_indentation(file)

    # Exibição formatada
    table = Table(title=f"📊 Análise do Arquivo: {file}", title_style="bold cyan")
    table.add_column("Métrica", style="bold yellow")
    table.add_column("Quantidade", justify="right", style="bold green")

    table.add_row("Total de linhas", str(line_count))
    table.add_row("Comentários", str(comment_count))
    table.add_row("Docstrings", str(docstring_count))
    table.add_row("Classes", str(class_count))
    table.add_row("Funções", str(function_count))
    table.add_row("Indentação Média", str(indent_result["average_indent"]))
    table.add_row("Indentação Máxima", str(indent_result["max_indent"]))
    table.add_row("Indentação Mínima", str(indent_result["min_indent"]))

    console.print(table)

# Comandos individuais
@app.command("lines", help="Conta o número total de linhas no código.")
def lines(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_lines(file)

@app.command("comments", help="Conta o número de comentários no código.")
def comments(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_comments(file)

@app.command("docstrings", help="Conta a quantidade de docstrings no código.")
def docstrings(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_docstrings(file)

@app.command("classes", help="Conta o número de classes no código.")
def classes(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_classes(file)
@app.command("functions", help="Conta o número de funções no código.")
def functions(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_functions(file)


@app.command("indent", help="Analisa os níveis de indentação do código.")
def indent(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_indentation(file)

    
# Entrada CLI
def cli_main():
    app()

if __name__ == "__main__":
    app()
