import tempfile
import os
from analyzer.analyze_indentation import count_indentation

def test_count_indentation_levels():
    # Código de exemplo com diferentes níveis de indentação
    example_code = """\
def func():
     x = 1
     if x > 0:
          print(x)
     return x
"""

    # Criar um arquivo temporário com esse código
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".py") as temp_file:
        temp_file.write(example_code)
        temp_path = temp_file.name

    try:
        result = count_indentation(temp_path)

        # Verificações básicas
        assert isinstance(result, dict)
        assert "average_indent" in result
        assert "max_indent" in result
        assert "min_indent" in result
        assert "indent_distribution" in result

        assert result["min_indent"] == 0
        assert result["max_indent"] == 10
        assert result["average_indent"] >= 0
        assert sum(result["indent_distribution"].values()) > 0

    finally:
        os.remove(temp_path)
