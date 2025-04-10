from rich.console import Console
from rich.table import Table

def count_indentation(file_path):
    indent_levels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            if line.strip():  # Ignorar linhas em branco
                spaces = len(line) - len(line.lstrip(' '))
                tabs = len(line) - len(line.lstrip('\t'))
                level = spaces if spaces else tabs * 4  # 1 tab = 4 espaços
                indent_levels.append((line_number, level))

    if not indent_levels:
        return {
            'average_indent': 0,
            'max_indent': 0,
            'min_indent': 0,
            'indent_distribution': {}
        }

    total_indent = sum(level for _, level in indent_levels)
    max_indent = max(level for _, level in indent_levels)
    min_indent = min(level for _, level in indent_levels)
    distribution = {}
    for _, level in indent_levels:
        distribution[level] = distribution.get(level, 0) + 1

    return {
        'average_indent': round(total_indent / len(indent_levels), 2),
        'max_indent': max_indent,
        'min_indent': min_indent,
        'indent_distribution': dict(sorted(distribution.items()))
    }

def analyze_indentation(file_path):
    result = count_indentation(file_path)

    console = Console()
    table = Table(title="Análise de Indentação")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="magenta")

    table.add_row("Indentação Média", str(result['average_indent']))
    table.add_row("Indentação Máxima", str(result['max_indent']))
    table.add_row("Indentação Mínima", str(result['min_indent']))

    distribution = "\n".join([f"{k} espaços: {v} linhas" for k, v in result['indent_distribution'].items()])
    table.add_row("Distribuição de Indentação", distribution)

    console.print(table)
