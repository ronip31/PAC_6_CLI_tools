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

def test_analyze_all_cli_output():
    # Teste com saída CLI
    result = runner.invoke(app, ["all", "examples/sample.py"])
    assert result.exit_code == 0
    assert "Análise do Arquivo" in result.stdout

def test_analyze_all_dir():
    # Teste com diretório
    result = runner.invoke(app, ["all-dir", "examples/", "--format", "json"])
    assert result.exit_code == 0
    
    # Verifica se a saída é um JSON válido
    json_data = json.loads(result.stdout)
    assert "files" in json_data
    assert "directory_analyzed" in json_data

def test_individual_commands():
    # Teste comandos individuais
    commands = [
        ["lines", "examples/sample.py"],
        ["comments", "examples/sample.py"],
        ["docstrings", "examples/sample.py"],
        ["classes", "examples/sample.py"],
        ["functions", "examples/sample.py"],
        ["methods", "examples/sample.py"],
        ["function-size", "examples/sample.py"],
        ["duplicate-code", "examples/sample.py"],
        ["indent", "examples/sample.py"],
        ["dependencies", "examples/sample.py"],
        ["comment-ratio", "examples/sample.py"]
    ]
    
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, f"Comando {command} falhou"

def test_bugs_ai_command():
    # Teste do comando de bugs com IA (sem API key)
    result = runner.invoke(app, ["bugs-ai", "examples/sample.py"])
    assert result.exit_code == 0
    assert "API key não configurada" in result.stdout

def test_bugs_ai_simple_command():
    # Teste do comando simplificado de bugs com IA
    result = runner.invoke(app, ["bugs-ai-simple", "examples/sample.py"])
    assert result.exit_code == 0
    assert "API key não configurada" in result.stdout 