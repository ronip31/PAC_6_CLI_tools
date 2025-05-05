import unittest
import tempfile
import os
from analyzer.analyze_comment_ratio import ProporcaoComentarioCodigo

class TestProporcaoComentarioCodigo(unittest.TestCase):

    def criar_arquivo_temporario(self, codigo: str) -> str:
        temp_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False, suffix='.py')
        temp_file.write(codigo)
        temp_file.close()
        return temp_file.name

    def tearDown(self):
        if hasattr(self, 'temp_file_path') and os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_codigo_com_comentarios(self):
        code = '''\
# Comentário geral

class ClasseExemplo:
    # Comentário da classe
    def metodo(self):
        # Comentário no método
        return 42

def funcao():
    # Comentário na função
    return 1
'''
        self.temp_file_path = self.criar_arquivo_temporario(code)
        analisador = ProporcaoComentarioCodigo(self.temp_file_path)
        resultado = analisador.analisar()
        self.assertEqual(len(resultado), 3)

    def test_codigo_sem_comentarios(self):
        code = '''\
class SemComentarios:
    def metodo(self):
        x = 1
        return x

def funcao():
    y = 2
    return y
'''
        self.temp_file_path = self.criar_arquivo_temporario(code)
        analisador = ProporcaoComentarioCodigo(self.temp_file_path)
        resultado = analisador.analisar()
        for item in resultado:
            self.assertEqual(item['comentarios'], 0)
            self.assertEqual(item['percentual'], 0.0)

    def test_multiplas_funcoes_classes(self):
        code = '''\
class A:
    def f1(self): pass

class B:
    def f2(self): pass

def fora(): pass
'''
        self.temp_file_path = self.criar_arquivo_temporario(code)
        analisador = ProporcaoComentarioCodigo(self.temp_file_path)
        resultado = analisador.analisar()
        self.assertEqual(len(resultado), 5)  # 2 classes + 3 métodos/funções

    def test_funcao_na_classe_sem_comentario(self):
        code = '''\
class Teste:
    def metodo(self):
        valor = 123
        return valor
'''
        self.temp_file_path = self.criar_arquivo_temporario(code)
        analisador = ProporcaoComentarioCodigo(self.temp_file_path)
        resultado = analisador.analisar()
        for item in resultado:
            self.assertIn('nome', item)
            self.assertIn('comentarios', item)
            self.assertEqual(item['comentarios'], 0)

    def test_classe_sem_metodos(self):
        code = '''\
class Vazia:
    # Comentário na classe
    pass
'''
        self.temp_file_path = self.criar_arquivo_temporario(code)
        analisador = ProporcaoComentarioCodigo(self.temp_file_path)
        resultado = analisador.analisar()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['nome'], 'Classe: Vazia')
        self.assertGreaterEqual(resultado[0]['comentarios'], 1)

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            ProporcaoComentarioCodigo("caminho/que/nao/existe.py")

if __name__ == '__main__':
    unittest.main()
