import ast
import tokenize
from io import StringIO

class ProporcaoComentarioCodigo:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.source_code = self._read_file()
        self.lines = self.source_code.splitlines()
        self.tree = ast.parse(self.source_code)

    def _read_file(self) -> str:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")

    def _get_comments(self):
        comments = {}
        for toktype, tokstring, start, _, _ in tokenize.generate_tokens(StringIO(self.source_code).readline):
            if toktype == tokenize.COMMENT:
                lineno = start[0]
                comments[lineno] = tokstring.strip()
        return comments

    def _get_node_lines(self, node):
        if hasattr(node, 'body') and node.body:
            start_line = node.lineno
            end_line = node.body[-1].lineno if hasattr(node.body[-1], 'lineno') else node.lineno
            return start_line, end_line
        return node.lineno, node.lineno

    def analisar(self):
        comentarios = self._get_comments()
        resultados = []

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start, end = self._get_node_lines(node)
                nome = f"{'Classe' if isinstance(node, ast.ClassDef) else 'Função'}: {node.name}"
                total_linhas = end - start + 1
                total_comentarios = sum(1 for i in range(start, end + 1) if i in comentarios)
                percentual = (total_comentarios / total_linhas) * 100 if total_linhas > 0 else 0
                resultados.append({
                    "nome": nome,
                    "linhas_totais": total_linhas,
                    "comentarios": total_comentarios,
                    "percentual": round(percentual, 2)
                })

        return resultados
