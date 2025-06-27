import typer
import os
from analyzer.analyze_lines import analyze_lines, count_lines
from analyzer.analyze_comments import analyze_comments, count_comments
from analyzer.analyze_docstrings import analyze_docstrings, count_docstrings
from analyzer.analyze_classes import analyze_classes, count_classes
from analyzer.analyze_functions import analyze_functions, count_functions
from analyzer.analyze_function_size import analyze_function_size, calculate_function_sizes
from analyzer.analyze_indentation import analyze_indentation, count_indentation
from analyzer.analyze_duplicate_code import analyze_duplicate_code, find_duplicate_blocks
from analyzer.analyze_bugs_ai import analyze_bugs_ai, analyze_bugs_ai_simple
from analyzer.dependency_analyzer import get_external_imports, analyze_repository

from analyzer.analyze_comment_ratio import ProporcaoComentarioCodigo
from analyzer.analyze_methods import analyze_methods, count_methods

from pathlib import Path
import subprocess


from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from analyzer.output_formatter import format_output
import json
from datetime import datetime

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
- `all`                → Analisa todas as métricas de um arquivo
- `all-dir`            → Analisa todas as métricas de arquivos Python em um diretório
- `lines`              → Conta o número total de linhas no código
- `comments`           → Conta o número de comentários no código
- `docstrings`         → Conta o número de docstrings no código
- `classes`            → Conta o número de classes no código
- `functions`          → Conta o número de funções no código
- `function-size`      → Analisa o tamanho médio das funções no código
- `duplicate-code`     → Identifica blocos de código duplicados
- `methods`            → Analisa os métodos públicos e privados no código
- `indent`             → Analisa os níveis de indentação
- `dependencies`       → Analisa as dependências externas do código
- `comment-ratio`      → Calcula o percentual de comentários por unidade de código
- `bugs-ai`            → Analisa código usando IA para identificar bugs e problemas
- `bugs-ai-simple`     → Versão simplificada da análise de bugs com IA

## 🔍 Opções de formato
Os comandos `all` e `all-dir` aceitam as seguintes opções:
- `--format` ou `-f`   → Formato de saída (cli ou json)
- `--output` ou `-o`   → Arquivo de saída para formato json

## 🤖 Comandos de IA
Os comandos `bugs-ai` e `bugs-ai-simple` requerem uma chave de API da OpenAI:
- Configure a variável de ambiente `OPENAI_API_KEY`
- Ou use `--api-key` para passar a chave diretamente
- Use `--simple` para modo simplificado
- Use `--language` para especificar a linguagem (padrão: python)

## 🧪 Comandos auxiliares (via terminal)
- `runtests`           → Roda todos os testes automatizados
- `runtests-verbose`   → Roda testes com saída detalhada
- `runtests-failures`  → Roda somente os testes que falharam anteriormente

## 💡 Exemplos
```bash
# Análise completa de um arquivo
analyzer all examples/sample.py

# Análise completa com saída JSON
analyzer all examples/sample.py --format json

# Análise completa de um diretório
analyzer all-dir examples/

# Análise de diretório com saída JSON
analyzer all-dir examples/ --format json

# Salvar resultado em arquivo JSON
analyzer all examples/sample.py --format json --output resultado.json
analyzer all-dir examples/ --format json --output resultado.json

# Análise de bugs com IA
analyzer bugs-ai examples/sample.py
analyzer bugs-ai examples/sample.py --simple
analyzer bugs-ai examples/sample.py --api-key sua_chave_aqui
```
    """
        console.print(Markdown(help_text))
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.secho("⚠️ Nenhum comando fornecido. Use '--help' para ver os comandos disponíveis.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)


@app.command("all-dir", help="Analisa todas as métricas dos arquivos Python em um diretório.")
def analyze_all_dir(
    directory: str = typer.Argument(..., help="Caminho para o diretório com arquivos Python."),
    format: str = typer.Option("cli", "--format", "-f", help="Formato de saída (cli ou json)"),
    output: str = typer.Option(None, "--output", "-o", help="Arquivo de saída (opcional, apenas para formato json)")
):
    """
    Analisa todas as métricas dos arquivos Python em um diretório.

    Opções de formato:
    - cli: Exibe resultado formatado no terminal (padrão)
    - json: Gera saída em formato JSON

    Exemplos:
        analyzer all-dir examples/
        analyzer all-dir examples/ --format json
        analyzer all-dir examples/ --format json --output resultado.json
    """
    try:
        # Verifica se o diretório existe
        if not os.path.isdir(directory):
            typer.secho(f"❌ Diretório não encontrado: {directory}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

        # Lista todos os arquivos .py no diretório
        python_files = [
            os.path.join(directory, f) 
            for f in os.listdir(directory) 
            if f.endswith('.py')
        ]

        if not python_files:
            typer.secho(f"⚠️ Nenhum arquivo Python encontrado em: {directory}", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)

        # Coleta métricas de todos os arquivos
        all_metrics = {
            "directory_analyzed": directory,
            "analysis_timestamp": datetime.now().isoformat(),
            "files": {}
        }

        total_metrics = {
            "total_files": len(python_files),
            "total_lines": 0,
            "total_comments": 0,
            "total_docstrings": 0,
            "total_classes": 0,
            "total_functions": 0,
            "total_methods": {
                "public": 0,
                "private": 0,
                "total": 0
            }
        }

        # Analisa cada arquivo
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()

                file_metrics = {
                    "metrics": {
                        "lines": count_lines(code),
                        "comments": count_comments(code),
                        "docstrings": count_docstrings(code),
                        "classes": count_classes(code),
                        "functions": count_functions(code)
                    },
                    "methods": {
                        "public": 0,
                        "private": 0,
                        "total": 0,
                        "ratio": {}
                    }
                }

                # Análise de métodos
                public_methods, private_methods = count_methods(code)
                total_methods = public_methods + private_methods
                
                file_metrics["methods"].update({
                    "public": public_methods,
                    "private": private_methods,
                    "total": total_methods
                })

                if total_methods > 0:
                    file_metrics["methods"]["ratio"] = {
                        "public": round((public_methods / total_methods) * 100, 1),
                        "private": round((private_methods / total_methods) * 100, 1)
                    }

                # Atualiza totais
                total_metrics["total_lines"] += file_metrics["metrics"]["lines"]
                total_metrics["total_comments"] += file_metrics["metrics"]["comments"]
                total_metrics["total_docstrings"] += file_metrics["metrics"]["docstrings"]
                total_metrics["total_classes"] += file_metrics["metrics"]["classes"]
                total_metrics["total_functions"] += file_metrics["metrics"]["functions"]
                total_metrics["total_methods"]["public"] += public_methods
                total_metrics["total_methods"]["private"] += private_methods
                total_metrics["total_methods"]["total"] += total_methods

                # Adiciona métricas do arquivo ao resultado
                all_metrics["files"][os.path.basename(file_path)] = file_metrics

            except Exception as e:
                typer.secho(f"⚠️ Erro ao analisar {file_path}: {str(e)}", fg=typer.colors.YELLOW)
                continue

        # Adiciona totais ao resultado
        all_metrics["summary"] = total_metrics

        # Calcula proporção total de métodos
        if total_metrics["total_methods"]["total"] > 0:
            all_metrics["summary"]["methods_ratio"] = {
                "public": round((total_metrics["total_methods"]["public"] / total_metrics["total_methods"]["total"]) * 100, 1),
                "private": round((total_metrics["total_methods"]["private"] / total_metrics["total_methods"]["total"]) * 100, 1)
            }

        # Formatação e saída
        if format.lower() == "json":
            result = format_output(all_metrics, "json", output)
            typer.echo(result)
            return

        # Exibição CLI padrão
        console.print("\n📊 Análise do Diretório:", directory)
        
        # Tabela de resumo
        summary_table = Table(title="📈 Resumo Geral", title_style="bold cyan")
        summary_table.add_column("Métrica", style="bold yellow")
        summary_table.add_column("Valor", justify="right", style="bold green")

        summary_table.add_row("Total de Arquivos", str(total_metrics["total_files"]))
        summary_table.add_row("Total de Linhas", str(total_metrics["total_lines"]))
        summary_table.add_row("Total de Comentários", str(total_metrics["total_comments"]))
        summary_table.add_row("Total de Docstrings", str(total_metrics["total_docstrings"]))
        summary_table.add_row("Total de Classes", str(total_metrics["total_classes"]))
        summary_table.add_row("Total de Funções", str(total_metrics["total_functions"]))
        summary_table.add_row("Total de Métodos Públicos", str(total_metrics["total_methods"]["public"]))
        summary_table.add_row("Total de Métodos Privados", str(total_metrics["total_methods"]["private"]))
        summary_table.add_row("Total de Métodos", str(total_metrics["total_methods"]["total"]))

        if "methods_ratio" in all_metrics["summary"]:
            summary_table.add_row(
                "Proporção Total Público/Privado",
                f"{all_metrics['summary']['methods_ratio']['public']}% / {all_metrics['summary']['methods_ratio']['private']}%"
            )

        console.print(summary_table)

        # Tabela detalhada por arquivo
        details_table = Table(title="\n📁 Detalhes por Arquivo", title_style="bold cyan")
        details_table.add_column("Arquivo", style="bold yellow")
        details_table.add_column("Linhas", justify="right")
        details_table.add_column("Comentários", justify="right")
        details_table.add_column("Classes", justify="right")
        details_table.add_column("Funções", justify="right")
        details_table.add_column("Métodos (Pub/Priv)", justify="right")

        for filename, metrics in all_metrics["files"].items():
            details_table.add_row(
                filename,
                str(metrics["metrics"]["lines"]),
                str(metrics["metrics"]["comments"]),
                str(metrics["metrics"]["classes"]),
                str(metrics["metrics"]["functions"]),
                f"{metrics['methods']['public']}/{metrics['methods']['private']}"
            )

        console.print(details_table)

    except Exception as e:
        typer.secho(f"❌ Erro durante a análise: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command("all")
def analyze_all(
    file: str = typer.Argument(..., help="Caminho para o arquivo Python a ser analisado."),
    format: str = typer.Option("cli", "--format", "-f", help="Formato de saída (cli ou json)"),
    output: str = typer.Option(None, "--output", "-o", help="Arquivo de saída (opcional, apenas para formato json)")
):
    """
    Analisa todas as métricas de um arquivo Python.

    Opções de formato:
    - cli: Exibe resultado formatado no terminal (padrão)
    - json: Gera saída em formato JSON

    Exemplos:
        analyzer all arquivo.py
        analyzer all arquivo.py --format json
        analyzer all arquivo.py --format json --output resultado.json
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        typer.secho(f"❌ Arquivo não encontrado: {file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"❌ Erro ao ler o arquivo: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        # Coleta todas as métricas
        metrics = {
            "file_analyzed": file,
            "analysis_timestamp": datetime.now().isoformat(),
            "metrics": {
                "lines": count_lines(code),
                "comments": count_comments(code),
                "docstrings": count_docstrings(code),
                "classes": count_classes(code),
                "functions": count_functions(code)
            },
            "methods": {
                "public": 0,
                "private": 0,
                "total": 0,
                "ratio": {}
            }
        }

        # Análise de métodos
        public_methods, private_methods = count_methods(code)
        total_methods = public_methods + private_methods
        
        metrics["methods"].update({
            "public": public_methods,
            "private": private_methods,
            "total": total_methods
        })

        if total_methods > 0:
            metrics["methods"]["ratio"] = {
                "public": round((public_methods / total_methods) * 100, 1),
                "private": round((private_methods / total_methods) * 100, 1)
            }

        # Formatação e saída
        if format.lower() == "json":
            result = format_output(metrics, "json", output)
            typer.echo(result)
            return

        # Exibição CLI padrão
        table = Table(title=f"📊 Análise do Arquivo: {file}", title_style="bold cyan")
        table.add_column("Métrica", style="bold yellow")
        table.add_column("Valor", justify="right", style="bold green")

        # Adiciona as linhas na tabela
        table.add_row("Total de Linhas", str(metrics["metrics"]["lines"]))
        table.add_row("Comentários", str(metrics["metrics"]["comments"]))
        table.add_row("Docstrings", str(metrics["metrics"]["docstrings"]))
        table.add_row("Classes", str(metrics["metrics"]["classes"]))
        table.add_row("Funções", str(metrics["metrics"]["functions"]))
        table.add_row("Métodos Públicos", str(metrics["methods"]["public"]))
        table.add_row("Métodos Privados", str(metrics["methods"]["private"]))
        table.add_row("Total de Métodos", str(metrics["methods"]["total"]))
        
        if total_methods > 0:
            table.add_row(
                "Proporção Público/Privado",
                f"{metrics['methods']['ratio']['public']}% / {metrics['methods']['ratio']['private']}%"
            )

        console.print(table)

    except Exception as e:
        typer.secho(f"❌ Erro durante a análise: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


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

@app.command("dependencies", help="Analisa as dependências externas do código.")
def dependencies(path: str = typer.Argument(..., help="Caminho para o arquivo ou diretório Python.")):
    from collections import defaultdict
    import_counter = defaultdict(int)

    if os.path.isfile(path):
        get_external_imports(path, import_counter)
    else:
        import_counter = analyze_repository(path)

    console.print(f"\n[bold magenta]📦 Dependências externas encontradas em '{path}':[/]\n")
    if not import_counter:
        console.print("[green]Nenhuma dependência externa encontrada.[/]")
        return

    table = Table(title="Dependências", title_style="bold blue")
    table.add_column("Biblioteca", style="bold yellow")
    table.add_column("Ocorrências", justify="right", style="bold green")

    for lib, count in sorted(import_counter.items(), key=lambda x: (-x[1], x[0])):
        table.add_row(lib, str(count))

    console.print(table)

@app.command("comment-ratio", help="Calcula o percentual de comentários por unidade de código (funções e classes).")
def comment_ratio(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    try:
        analisador = ProporcaoComentarioCodigo(file)
        resultados = analisador.analisar()
    except FileNotFoundError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not resultados:
        console.print("[yellow]⚠️ Nenhuma função ou classe encontrada.[/]")
        return

    table = Table(title="📈 Proporção Comentário/Código", title_style="bold blue")
    table.add_column("Unidade", style="bold yellow")
    table.add_column("Linhas", justify="right")
    table.add_column("Comentários", justify="right")
    table.add_column("Comentado (%)", justify="right")

    for r in resultados:
        table.add_row(r["nome"], str(r["linhas_totais"]), str(r["comentarios"]), f'{r["percentual"]}%')

    console.print(table)

@app.command("methods", help="Analisa os métodos públicos e privados no código.")
def methods(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_methods(file)

@app.command("function-size", help="Analisa o tamanho médio das funções no código.")
def function_size(file: str = typer.Argument(..., help="Caminho para o arquivo Python.")):
    analyze_function_size(file)

@app.command("duplicate-code", help="Identifica blocos de código duplicados no arquivo.")
def duplicate_code(
    file: str = typer.Argument(..., help="Caminho para o arquivo Python."),
    block_size: int = typer.Option(None, "--block-size", "-b", help="Tamanho do bloco para análise (padrão: automático)"),
    auto: bool = typer.Option(True, "--auto", "-a", help="Modo automático: testa múltiplos tamanhos (2-10 linhas)")
):
    # Se block_size foi especificado, desabilita o modo automático
    if block_size is not None:
        auto = False
    analyze_duplicate_code(file, block_size, auto)

@app.command("bugs-ai", help="Analisa código usando IA para identificar bugs e problemas.")
def bugs_ai(
    file: str = typer.Argument(..., help="Caminho para o arquivo Python."),
    language: str = typer.Option("python", "--language", "-l", help="Linguagem de programação"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="Chave da API (ou configure OPENAI_API_KEY)"),
    simple: bool = typer.Option(False, "--simple", "-s", help="Modo simplificado"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Ignorar cache e fazer nova requisição"),
    model: str = typer.Option(None, "--model", "-m", help="Modelo a ser usado (gpt-3.5-turbo, gpt-4, etc.)")
):
    """
    Analisa código usando IA para identificar bugs, problemas de segurança, performance e qualidade.
    
    Requer uma chave de API da OpenAI. Configure a variável de ambiente OPENAI_API_KEY
    ou passe via parâmetro --api-key.
    
    O sistema usa cache para evitar requisições desnecessárias. Use --no-cache para forçar
    uma nova análise.
    
    Modelos disponíveis: gpt-3.5-turbo (padrão), gpt-3.5-turbo-16k, gpt-4, gpt-4-turbo
    
    Exemplos:
        analyzer bugs-ai examples/sample.py
        analyzer bugs-ai examples/sample.py --simple
        analyzer bugs-ai examples/sample.py --api-key sua_chave_aqui
        analyzer bugs-ai examples/sample.py --no-cache
        analyzer bugs-ai examples/sample.py --model gpt-4
    """
    if simple:
        analyze_bugs_ai_simple(file, language, api_key, no_cache, model)
    else:
        analyze_bugs_ai(file, language, api_key, no_cache, model)

@app.command("bugs-ai-simple", help="Versão simplificada da análise de bugs com IA.")
def bugs_ai_simple(
    file: str = typer.Argument(..., help="Caminho para o arquivo Python."),
    language: str = typer.Option("python", "--language", "-l", help="Linguagem de programação"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="Chave da API (ou configure OPENAI_API_KEY)"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Ignorar cache e fazer nova requisição"),
    model: str = typer.Option(None, "--model", "-m", help="Modelo a ser usado (gpt-3.5-turbo, gpt-4, etc.)")
):
    """
    Versão simplificada da análise de bugs com IA.
    
    Exemplos:
        analyzer bugs-ai-simple examples/sample.py
        analyzer bugs-ai-simple examples/sample.py --api-key sua_chave_aqui
        analyzer bugs-ai-simple examples/sample.py --no-cache
        analyzer bugs-ai-simple examples/sample.py --model gpt-3.5-turbo
    """
    analyze_bugs_ai_simple(file, language, api_key, no_cache, model)

@app.command("clear-cache", help="Limpa o cache de análises de bugs com IA.")
def clear_cache():
    """
    Limpa o cache de análises de bugs com IA.
    
    O cache é usado para evitar requisições desnecessárias à API da OpenAI.
    Use este comando se quiser forçar novas análises.
    """
    from analyzer.analyze_bugs_ai import clear_cache
    clear_cache()

@app.command("list-models", help="Lista os modelos disponíveis para análise de bugs com IA.")
def list_models():
    """
    Lista os modelos disponíveis para análise de bugs com IA.
    
    Mostra informações sobre custos, capacidades e recomendações para cada modelo.
    """
    from analyzer.analyze_bugs_ai import list_models
    list_models()

# Entrada CLI
def cli_main():
    app()

if __name__ == "__main__":
    app()
