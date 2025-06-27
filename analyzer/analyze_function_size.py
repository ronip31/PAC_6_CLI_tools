import typer
import ast
from typing import Tuple

def calculate_function_sizes(code: str, debug: bool = False) -> Tuple[int, float]:
    """
    Calcula o número de funções e o tamanho médio das funções no código.
    Retorna uma tupla (número_de_funções, tamanho_médio).
    Linhas em branco NÃO são contadas.
    """
    tree = ast.parse(code)
    function_count = 0
    total_lines = 0
    code_lines = code.split('\n')
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1
            first_line = node.lineno
            last_line = node.end_lineno if hasattr(node, 'end_lineno') else first_line
            first_line = max(1, first_line)
            last_line = min(len(code_lines), last_line)
            # Pega o intervalo correto
            lines_in_func = code_lines[first_line-1:last_line]
            non_blank = [line for line in lines_in_func if line.strip()]
            if debug:
                print(f'Função {node.name}:')
                for idx, line in enumerate(lines_in_func, start=first_line):
                    print(f'{idx:3}: {repr(line)}')
                print(f'Linhas não em branco: {len(non_blank)}\n')
            total_lines += len(non_blank)
    if function_count == 0:
        return 0, 0.0
    return function_count, total_lines / function_count

def analyze_function_size(file: str, debug: bool = False):
    """
    Função CLI para analisar o tamanho médio das funções de um arquivo.
    """
    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()
    function_count, avg_size = calculate_function_sizes(code, debug=debug)
    print("Análise do Tamanho das Funções:")
    print(f"Número de Funções: {function_count}")
    print(f"Tamanho Médio das Funções: {avg_size:.1f} linhas") 