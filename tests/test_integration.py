import pytest
import json
import os
from typer.testing import CliRunner
from analyzer.main import app

runner = CliRunner()

def test_analyze_all_json_output():
    # Teste com saída JSON
    result = runner.invoke(app, ["all", "examples/sample.py", "--format", "json"])
    assert result.exit_code == 0
    
    # Verifica se a saída é um JSON válido
    json_data = json.loads(result.stdout)
    assert "metrics" in json_data
    assert "methods" in json_data
    
    # Teste com arquivo de saída
    output_file = "test_output.json"
    result = runner.invoke(app, ["all", "examples/sample.py", "--format", "json", "--output", output_file])
    assert result.exit_code == 0
    
    # Verifica se o arquivo foi criado
    assert os.path.exists(output_file)
    
    # Limpa o arquivo de teste
    os.remove(output_file)

def test_analyze_all_cli_ 