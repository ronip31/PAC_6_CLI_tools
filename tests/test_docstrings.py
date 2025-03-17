from analyzer.analyze_docstrings import count_docstrings

def test_count_docstrings():
    code = '"""Este é um docstring."""\ndef funcao():\n    """Outro docstring."""\n    pass'
    assert count_docstrings(code) == 2

    no_docstring_code = "def funcao():\n    pass"
    assert count_docstrings(no_docstring_code) == 0

    multiple_docstrings = '"""Módulo."""\n"""Outro."""\ndef funcao():\n    """Função."""\n    pass'
    assert count_docstrings(multiple_docstrings) == 3
