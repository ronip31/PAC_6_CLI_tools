import pytest
import os
from unittest.mock import Mock, patch
from analyzer.analyze_bugs_ai import BugPredictorAI, analyze_bugs_ai, analyze_bugs_ai_simple

class TestBugPredictorAI:
    """Testes para a classe BugPredictorAI."""
    
    def test_init_with_api_key(self):
        """Testa inicialização com chave de API."""
        api_key = "test_key"
        predictor = BugPredictorAI(api_key=api_key)
        assert predictor.api_key == api_key
        assert predictor.api_url == "https://api.openai.com/v1/chat/completions"
        assert predictor.model == "gpt-3.5-turbo"
    
    def test_init_with_env_var(self):
        """Testa inicialização com variável de ambiente."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'env_key'}):
            predictor = BugPredictorAI()
            assert predictor.api_key == 'env_key'
    
    def test_init_with_custom_url(self):
        """Testa inicialização com URL customizada."""
        api_key = "test_key"
        custom_url = "https://custom.api.com/v1/chat/completions"
        predictor = BugPredictorAI(api_key=api_key, api_url=custom_url)
        assert predictor.api_url == custom_url
    
    def test_create_prompt(self):
        """Testa criação do prompt."""
        predictor = BugPredictorAI(api_key="test")
        code = "def test(): pass"
        prompt = predictor._create_prompt(code, "python")
        
        assert "python" in prompt
        assert code in prompt
        assert "Problemas de Segurança" in prompt
        assert "Problemas de Performance" in prompt
        assert "JSON" in prompt
    
    def test_analyze_code_no_api_key(self):
        """Testa análise sem chave de API."""
        predictor = BugPredictorAI(api_key=None)
        result = predictor.analyze_code("def test(): pass")
        
        assert "error" in result
        assert "API key não configurada" in result["error"]
    
    @patch('requests.post')
    def test_analyze_code_success(self, mock_post):
        """Testa análise bem-sucedida."""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': '{"problems": [], "summary": {"total_problems": 0}}'
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        predictor = BugPredictorAI(api_key="test_key")
        result = predictor.analyze_code("def test(): pass")
        
        assert "problems" in result
        assert "summary" in result
        assert result["summary"]["total_problems"] == 0
    
    @patch('requests.post')
    def test_analyze_code_invalid_json(self, mock_post):
        """Testa análise com JSON inválido na resposta."""
        # Mock da resposta da API com JSON inválido
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Resposta em texto simples, não JSON'
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        predictor = BugPredictorAI(api_key="test_key")
        result = predictor.analyze_code("def test(): pass")
        
        assert "raw_analysis" in result
        assert "error" in result
        assert "Não foi possível processar" in result["error"]
    
    @patch('requests.post')
    def test_analyze_code_request_error(self, mock_post):
        """Testa erro na requisição."""
        mock_post.side_effect = Exception("Connection error")
        
        predictor = BugPredictorAI(api_key="test_key")
        result = predictor.analyze_code("def test(): pass")
        
        assert "error" in result
        assert "Erro inesperado" in result["error"]

class TestAnalyzeBugsAI:
    """Testes para as funções CLI de análise de bugs."""
    
    def test_analyze_bugs_ai_file_not_found(self):
        """Testa análise com arquivo inexistente."""
        with patch('builtins.print') as mock_print:
            analyze_bugs_ai("arquivo_inexistente.py")
            mock_print.assert_called_with("❌ Arquivo não encontrado: arquivo_inexistente.py")
    
    @patch('analyzer.analyze_bugs_ai.BugPredictorAI')
    def test_analyze_bugs_ai_success(self, mock_predictor_class):
        """Testa análise bem-sucedida."""
        # Mock do predictor
        mock_predictor = Mock()
        mock_predictor.analyze_code.return_value = {
            "problems": [
                {
                    "type": "security",
                    "severity": "high",
                    "description": "Problema de segurança",
                    "line": 10,
                    "suggestion": "Use input() com validação"
                }
            ],
            "summary": {
                "total_problems": 1,
                "critical": 0,
                "high": 1,
                "medium": 0,
                "low": 0
            }
        }
        mock_predictor_class.return_value = mock_predictor
        
        # Criar arquivo temporário
        with open("temp_test.py", "w") as f:
            f.write("user_input = input()\nprint(user_input)")
        
        try:
            with patch('builtins.print') as mock_print:
                analyze_bugs_ai("temp_test.py")
                
                # Verifica se o predictor foi chamado
                mock_predictor.analyze_code.assert_called_once()
                
                # Verifica se a saída foi impressa
                assert mock_print.call_count > 0
        finally:
            # Limpa arquivo temporário
            if os.path.exists("temp_test.py"):
                os.remove("temp_test.py")
    
    @patch('analyzer.analyze_bugs_ai.BugPredictorAI')
    def test_analyze_bugs_ai_error(self, mock_predictor_class):
        """Testa análise com erro."""
        # Mock do predictor com erro
        mock_predictor = Mock()
        mock_predictor.analyze_code.return_value = {
            "error": "Erro de API"
        }
        mock_predictor_class.return_value = mock_predictor
        
        # Criar arquivo temporário
        with open("temp_test.py", "w") as f:
            f.write("print('test')")
        
        try:
            with patch('builtins.print') as mock_print:
                analyze_bugs_ai("temp_test.py")
                mock_print.assert_called_with("❌ Erro: Erro de API")
        finally:
            if os.path.exists("temp_test.py"):
                os.remove("temp_test.py")
    
    @patch('analyzer.analyze_bugs_ai.BugPredictorAI')
    def test_analyze_bugs_ai_simple(self, mock_predictor_class):
        """Testa versão simplificada da análise."""
        # Mock do predictor
        mock_predictor = Mock()
        mock_predictor.analyze_code.return_value = {
            "problems": [
                {
                    "severity": "medium",
                    "description": "Problema médio",
                    "line": 5
                }
            ]
        }
        mock_predictor_class.return_value = mock_predictor
        
        # Criar arquivo temporário
        with open("temp_test.py", "w") as f:
            f.write("x = 1\nprint(x)")
        
        try:
            with patch('builtins.print') as mock_print:
                analyze_bugs_ai_simple("temp_test.py")
                
                # Verifica se o predictor foi chamado
                mock_predictor.analyze_code.assert_called_once()
                
                # Verifica se a saída foi impressa
                assert mock_print.call_count > 0
        finally:
            if os.path.exists("temp_test.py"):
                os.remove("temp_test.py")

if __name__ == "__main__":
    pytest.main([__file__]) 