import ast
import os
from collections import defaultdict

# Módulos padrões do Python (parcialmente listados)
STANDARD_LIBS = {
    'os', 'sys', 'math', 'json', 're', 'datetime', 'time', 'typing', 'functools',
    'collections', 'subprocess', 'pathlib', 'itertools', 'random', 'threading',
    'http', 'shutil', 'tempfile', 'csv', 'glob', 'logging', 'unittest'
}

def get_external_imports(filepath, counter):
    """Adiciona os nomes dos pacotes externos importados no arquivo ao contador."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except (FileNotFoundError, SyntaxError):
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name not in STANDARD_LIBS:
                    counter[name] += 1
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name not in STANDARD_LIBS:
                    counter[name] += 1

def analyze_repository(path="."):
    """Percorre todos os arquivos .py e conta os imports externos únicos."""
    import_counter = defaultdict(int)

    for subdir, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(subdir, file)
                get_external_imports(filepath, import_counter)

    return dict(import_counter)
