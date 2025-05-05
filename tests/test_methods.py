from analyzer.analyze_methods import count_methods, analyze_methods
import pytest
from typer.testing import CliRunner
import tempfile
import os

def test_count_methods():
    # Teste 1: Classe sem métodos
    code1 = """
class MinhaClasse:
    pass
    """
    assert count_methods(code1) == (0, 0)

    # Teste 2: Classe com apenas métodos públicos
    code2 = """
class MinhaClasse:
    def metodo1(self):
        pass
    def metodo2(self):
        pass
    """
    assert count_methods(code2) == (2, 0)

    # Teste 3: Classe com apenas métodos privados
    code3 = """
class MinhaClasse:
    def _metodo1(self):
        pass
    def _metodo2(self):
        pass
    """
    assert count_methods(code3) == (0, 2)

    # Teste 4: Classe com métodos especiais (dunder)
    code4 = """
class MinhaClasse:
    def __init__(self):
        pass
    def __str__(self):
        pass
    """
    assert count_methods(code4) == (0, 0)

    # Teste 5: Classe com mix de métodos
    code5 = """
class MinhaClasse:
    def metodo_publico(self):
        pass
    def _metodo_privado(self):
        pass
    def __init__(self):
        pass
    """
    assert count_methods(code5) == (1, 1)

    # Teste 6: Múltiplas classes
    code6 = """
class Classe1:
    def metodo_publico(self):
        pass
    def _metodo_privado(self):
        pass

class Classe2:
    def outro_metodo(self):
        pass
    def _outro_privado(self):
        pass
    """
    assert count_methods(code6) == (2, 2)

    # Teste 7: Código sem classes
    code7 = """
def funcao_normal():
    pass
    """
    assert count_methods(code7) == (0, 0)

def test_edge_cases():
    # Teste 8: String vazia
    assert count_methods("") == (0, 0)

    # Teste 9: Apenas comentários
    code9 = """
# Isso é um comentário
# Outro comentário
"""
    assert count_methods(code9) == (0, 0)

    # Teste 10: Classe com decoradores
    code10 = """
class MinhaClasse:
    @property
    def metodo_publico(self):
        pass
    @staticmethod
    def _metodo_privado():
        pass
    """
    assert count_methods(code10) == (1, 1)

# Novos testes para analyze_methods
def test_analyze_methods(capsys):
    # Criamos um arquivo temporário para testar
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Caso 1: Classe com métodos públicos e privados
        temp_file.write("""
class MinhaClasse:
    def metodo_publico(self):
        pass
    def _metodo_privado(self):
        pass
    def outro_publico(self):
        pass
""")
        temp_file.flush()
        
        # Testamos a função analyze_methods
        analyze_methods(temp_file.name)
        
        # Capturamos a saída
        captured = capsys.readouterr()
        
        # Verificamos se a saída contém as informações esperadas
        assert "Análise de Métodos:" in captured.out
        assert "Métodos Públicos: 2" in captured.out
        assert "Métodos Privados: 1" in captured.out
        assert "Total de Métodos: 3" in captured.out
        assert "Proporção Público/Privado: 66.7% / 33.3%" in captured.out

    # Limpeza do arquivo temporário
    os.unlink(temp_file.name)

def test_analyze_methods_empty_class(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Caso 2: Classe vazia
        temp_file.write("""
class ClasseVazia:
    pass
""")
        temp_file.flush()
        
        analyze_methods(temp_file.name)
        captured = capsys.readouterr()
        
        assert "Métodos Públicos: 0" in captured.out
        assert "Métodos Privados: 0" in captured.out
        assert "Total de Métodos: 0" in captured.out

    os.unlink(temp_file.name)

def test_analyze_methods_multiple_classes(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Caso 3: Múltiplas classes
        temp_file.write("""
class Classe1:
    def metodo1(self):
        pass
    def _metodo_privado1(self):
        pass

class Classe2:
    def metodo2(self):
        pass
    def _metodo_privado2(self):
        pass
""")
        temp_file.flush()
        
        analyze_methods(temp_file.name)
        captured = capsys.readouterr()
        
        assert "Métodos Públicos: 2" in captured.out
        assert "Métodos Privados: 2" in captured.out
        assert "Total de Métodos: 4" in captured.out
        assert "Proporção Público/Privado: 50.0% / 50.0%" in captured.out

    os.unlink(temp_file.name)

def test_analyze_methods_file_not_found():
    # Caso 4: Arquivo não existente
    with pytest.raises(FileNotFoundError):
        analyze_methods("arquivo_que_nao_existe.py")

def test_analyze_methods_with_special_methods(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Caso 5: Classe com métodos especiais
        temp_file.write("""
class ClasseComEspeciais:
    def __init__(self):
        pass
    def metodo_normal(self):
        pass
    def _metodo_privado(self):
        pass
    def __str__(self):
        pass
""")
        temp_file.flush()
        
        analyze_methods(temp_file.name)
        captured = capsys.readouterr()
        
        assert "Métodos Públicos: 1" in captured.out
        assert "Métodos Privados: 1" in captured.out
        assert "Total de Métodos: 2" in captured.out
        assert "Proporção Público/Privado: 50.0% / 50.0%" in captured.out

    os.unlink(temp_file.name)

def test_analyze_methods_with_decorators(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Caso 6: Classe com métodos decorados
        temp_file.write("""
class ClasseComDecorators:
    @property
    def propriedade(self):
        pass
    
    @staticmethod
    def metodo_estatico(self):
        pass
    
    @classmethod
    def _metodo_privado(cls):
        pass
""")
        temp_file.flush()
        
        analyze_methods(temp_file.name)
        captured = capsys.readouterr()
        
        assert "Métodos Públicos: 2" in captured.out
        assert "Métodos Privados: 1" in captured.out
        assert "Total de Métodos: 3" in captured.out

    os.unlink(temp_file.name) 