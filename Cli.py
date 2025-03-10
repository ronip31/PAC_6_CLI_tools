import typer
import re

app = typer.Typer()

def count_lines(file_path: str):
    """
    Contagem de Linhas de Código (LOC).
    Lê o arquivo e conta linhas de código, comentários e docstrings.
    Também identifica a quantidade de funções e classes no código.
    """
    total_lines = 0
    code_lines = 0
    comment_lines = 0
    docstring_lines = 0
    empty_lines = 0
    function_count = 0
    class_count = 0
    in_docstring = False
    docstring_delimiter = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                total_lines += 1
                stripped_line = line.strip()
                
                # Linhas vazias
                if not stripped_line:
                    empty_lines += 1
                    continue
                
                # Identificação de Docstrings
                if stripped_line.startswith(('"""', "'''")):
                    if in_docstring:
                        if stripped_line == docstring_delimiter or stripped_line.endswith(docstring_delimiter):
                            # Fechando docstring
                            in_docstring = False
                        docstring_lines += 1  # Conta a linha de fechamento
                    else:
                        # Se a docstring começa e termina na mesma linha
                        if stripped_line.count('"""') == 2 or stripped_line.count("'''") == 2:
                            docstring_lines += 1  # Conta apenas uma linha
                        else:
                            in_docstring = True   # Abrindo docstring
                            docstring_delimiter = stripped_line[:3]  # Define qual delimitador está sendo usado
                            docstring_lines += 1  # Conta a linha de abertura
                    continue
                
                if in_docstring:
                    docstring_lines += 1  # Conta apenas as linhas dentro da docstring
                    continue

                # Comentários isolados
                if stripped_line.startswith("#"):
                    comment_lines += 1
                    continue

                # Código com comentário inline
                if "#" in stripped_line:
                    comment_lines += 1
                    stripped_line = stripped_line.split("#")[0].strip()  # Remove o comentário
                    if not stripped_line:
                        continue  # Se só tinha um comentário, não conta como código

                # Código
                code_lines += 1

                # Funções e Classes
                if re.match(r'^def\s+\w+\s*\(', stripped_line):
                    function_count += 1
                elif re.match(r'^class\s+\w+', stripped_line):
                    class_count += 1
        
        # Exibição dos resultados
        typer.echo(f"Arquivo: {file_path}")
        typer.echo(f"Total de linhas: {total_lines}")
        typer.echo(f"Linhas de código: {code_lines}")
        typer.echo(f"Linhas de comentário: {comment_lines}")
        typer.echo(f"Linhas de docstrings: {docstring_lines}")
        typer.echo(f"Linhas vazias: {empty_lines}")
        typer.echo(f"Número de funções: {function_count}")
        typer.echo(f"Número de classes: {class_count}")
        
    except FileNotFoundError:
        typer.echo(f"Erro: Arquivo '{file_path}' não encontrado.", err=True)
    except Exception as e:
        typer.echo(f"Erro ao processar o arquivo: {e}", err=True)

@app.command(help="Contagem de Linhas de Código (LOC). Analisa um arquivo Python e exibe informações sobre código, comentários e estrutura.")
def loc(file: str):
    count_lines(file)

if __name__ == "__main__":
    app()
