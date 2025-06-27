import typer
import requests
import json
import os
import hashlib
import pickle
from typing import Optional, List, Dict, Any
import time
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class BugPredictorAI:
    """Classe para análise de código usando IA através de API de LLM."""
    
    def __init__(self, api_key: str = None, api_url: str = None, cache_dir: str = ".cache", model: str = None):
        """
        Inicializa o analisador de bugs com IA.
        
        Args:
            api_key: Chave da API (pode ser definida via variável de ambiente)
            api_url: URL da API (padrão: OpenAI)
            cache_dir: Diretório para armazenar o cache (padrão: ".cache")
            model: Modelo a ser usado (padrão: gpt-3.5-turbo ou OPENAI_MODEL)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.api_url = api_url or "https://api.openai.com/v1/chat/completions"
        
        # Modelo configurável
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        # Configurações por modelo
        self.model_configs = {
            'gpt-3.5-turbo': {
                'max_tokens': 2000,
                'temperature': 0.3,
                'cost_per_1k_tokens': 0.002  # USD
            },
            'gpt-3.5-turbo-16k': {
                'max_tokens': 4000,
                'temperature': 0.3,
                'cost_per_1k_tokens': 0.004
            },
            'gpt-4': {
                'max_tokens': 2000,
                'temperature': 0.3,
                'cost_per_1k_tokens': 0.03
            },
            'gpt-4-turbo': {
                'max_tokens': 2000,
                'temperature': 0.3,
                'cost_per_1k_tokens': 0.01
            }
        }
        
        # Usa configuração padrão se modelo não encontrado
        if self.model not in self.model_configs:
            print(f"Aviso: Modelo '{self.model}' não reconhecido. Usando configuração padrão.")
            self.model_configs[self.model] = {
                'max_tokens': 2000,
                'temperature': 0.3,
                'cost_per_1k_tokens': 0.002
            }
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_key(self, code: str, language: str) -> str:
        """Gera uma chave única para o cache baseada no código e linguagem."""
        content = f"{language}:{code}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _get_cache_file(self, cache_key: str) -> Path:
        """Retorna o caminho do arquivo de cache."""
        return self.cache_dir / f"bugs_ai_{cache_key}.pkl"
    
    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Carrega resultado do cache se existir e não estiver expirado."""
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            return None
            
        # Verifica se o cache não expirou (24 horas)
        if time.time() - cache_file.stat().st_mtime > 86400:  # 24 horas
            cache_file.unlink()
            return None
            
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
    def _save_to_cache(self, cache_key: str, result: Dict[str, Any]):
        """Salva resultado no cache."""
        cache_file = self._get_cache_file(cache_key)
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
        except Exception:
            pass  # Ignora erros de cache
        
    def _create_prompt(self, code: str, language: str = "python") -> str:
        """Cria o prompt para análise de código."""
        return f"""Analise o seguinte código {language} e identifique possíveis problemas, bugs e sugestões de melhoria:

```{language}
{code}
```

Por favor, forneça uma análise detalhada incluindo:
1. Problemas de Segurança: Vulnerabilidades, injeção de código, etc.
2. Problemas de Performance: Algoritmos ineficientes, loops desnecessários, etc.
3. Problemas de Qualidade: Código duplicado, variáveis não utilizadas, etc.
4. Problemas de Manutenibilidade: Código difícil de entender, falta de documentação, etc.
5. Sugestões de Melhoria: Como melhorar o código
6. Severidade: Baixa, Média, Alta ou Crítica para cada problema

Responda em formato JSON com a seguinte estrutura:
{{
    "problems": [
        {{
            "type": "security|performance|quality|maintainability",
            "severity": "low|medium|high|critical",
            "description": "Descrição do problema",
            "line": número_da_linha_ou_null,
            "suggestion": "Sugestão de correção"
        }}
    ],
    "summary": {{
        "total_problems": número,
        "critical": número,
        "high": número,
        "medium": número,
        "low": número
    }}
}}"""

    def analyze_code(self, code: str, language: str = "python", use_cache: bool = True) -> Dict[str, Any]:
        """
        Analisa código usando IA.
        
        Args:
            code: Código a ser analisado
            language: Linguagem de programação
            use_cache: Se deve usar o cache (padrão: True)
            
        Returns:
            Dicionário com a análise
        """
        if not self.api_key:
            return {
                "error": "API key não configurada. Configure OPENAI_API_KEY no arquivo .env, variável de ambiente ou passe via parâmetro."
            }
        
        # Verifica cache primeiro
        if use_cache:
            cache_key = self._get_cache_key(code, language)
            cached_result = self._load_from_cache(cache_key)
            if cached_result:
                print("Resultado carregado do cache (análise anterior).")
                return cached_result
        
        try:
            prompt = self._create_prompt(code, language)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Você é um analisador de código especializado em identificar bugs e problemas de qualidade."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_configs[self.model]['temperature'],
                "max_tokens": self.model_configs[self.model]['max_tokens']
            }
            
            print("Fazendo requisição para a API da OpenAI...")
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Tenta fazer parse do JSON
            try:
                analysis = json.loads(content)
                # Salva no cache se bem-sucedido
                if use_cache:
                    cache_key = self._get_cache_key(code, language)
                    self._save_to_cache(cache_key, analysis)
                return analysis
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, retorna o texto como está
                return {
                    "raw_analysis": content,
                    "error": "Não foi possível processar a resposta como JSON"
                }
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro na requisição: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}

def analyze_bugs_ai(file: str, language: str = "python", api_key: str = None, no_cache: bool = False, model: str = None):
    """
    Função CLI para análise de bugs usando IA.
    
    Args:
        file: Arquivo a ser analisado
        language: Linguagem de programação
        api_key: Chave da API (opcional)
        no_cache: Se deve ignorar o cache (padrão: False)
        model: Modelo a ser usado (opcional)
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file}")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    
    print(f"Analisando código com IA...")
    print(f"Arquivo: {file}")
    print(f"Linguagem: {language}")
    
    predictor = BugPredictorAI(api_key=api_key, model=model)
    print(f"Modelo: {predictor.model}")
    
    result = predictor.analyze_code(code, language, use_cache=not no_cache)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return
    
    if "raw_analysis" in result:
        print("\nAnálise da IA:")
        print(result["raw_analysis"])
        return
    
    print("\n" + "="*60)
    print("ANÁLISE DE BUGS COM IA")
    print("="*60)
    
    if "summary" in result:
        summary = result["summary"]
        print(f"\nRESUMO:")
        print(f"   Total de problemas: {summary.get('total_problems', 0)}")
        print(f"   Críticos: {summary.get('critical', 0)}")
        print(f"   Altos: {summary.get('high', 0)}")
        print(f"   Médios: {summary.get('medium', 0)}")
        print(f"   Baixos: {summary.get('low', 0)}")
    
    if "problems" in result and result["problems"]:
        print(f"\nPROBLEMAS IDENTIFICADOS:")
        severity_order = ["critical", "high", "medium", "low"]
        for severity in severity_order:
            problems = [p for p in result["problems"] if p.get("severity") == severity]
            if problems:
                print(f"\n{severity.upper()}:")
                for i, problem in enumerate(problems, 1):
                    line_info = f" (linha {problem['line']})" if problem.get("line") else ""
                    print(f"   {i}. {problem.get('description', 'N/A')}{line_info}")
                    if problem.get("suggestion"):
                        print(f"      Sugestão: {problem['suggestion']}")
    else:
        print("\nNenhum problema crítico identificado!")
        print("   O código parece estar bem estruturado.")

def analyze_bugs_ai_simple(file: str, language: str = "python", api_key: str = None, no_cache: bool = False, model: str = None):
    """
    Versão simplificada da análise de bugs.
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file}")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    
    print(f"Analisando {file} com IA...")
    
    predictor = BugPredictorAI(api_key=api_key, model=model)
    print(f"Modelo: {predictor.model}")
    
    result = predictor.analyze_code(code, language, use_cache=not no_cache)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return
    
    if "raw_analysis" in result:
        print("\nAnálise:")
        print(result["raw_analysis"])
        return
    
    if "problems" in result and result["problems"]:
        print(f"\nEncontrados {len(result['problems'])} problemas:")
        for i, problem in enumerate(result["problems"], 1):
            severity = problem.get("severity", "unknown")
            line_info = f" (linha {problem['line']})" if problem.get("line") else ""
            print(f"   {i}. [{severity.upper()}] {problem.get('description', 'N/A')}{line_info}")
    else:
        print("\nNenhum problema identificado!")

def clear_cache():
    """Limpa o cache de análises."""
    cache_dir = Path(".cache")
    if cache_dir.exists():
        for cache_file in cache_dir.glob("bugs_ai_*.pkl"):
            cache_file.unlink()
        print("Cache limpo com sucesso!")
    else:
        print("Nenhum cache encontrado.")

def list_models():
    """Lista os modelos disponíveis com suas configurações."""
    print("Modelos disponíveis para análise de bugs:")
    print("=" * 50)
    
    models = {
        'gpt-3.5-turbo': {
            'description': 'Modelo padrão, rápido e econômico',
            'max_tokens': 2000,
            'cost_per_1k_tokens': 0.002,
            'recomendado': 'Para uso geral'
        },
        'gpt-3.5-turbo-16k': {
            'description': 'Versão com contexto maior',
            'max_tokens': 4000,
            'cost_per_1k_tokens': 0.004,
            'recomendado': 'Para arquivos grandes'
        },
        'gpt-4': {
            'description': 'Modelo mais avançado',
            'max_tokens': 2000,
            'cost_per_1k_tokens': 0.03,
            'recomendado': 'Para análises complexas'
        },
        'gpt-4-turbo': {
            'description': 'Versão mais recente do GPT-4',
            'max_tokens': 2000,
            'cost_per_1k_tokens': 0.01,
            'recomendado': 'Melhor custo-benefício'
        }
    }
    
    for model, config in models.items():
        print(f"\n{model}:")
        print(f"  Descrição: {config['description']}")
        print(f"  Max tokens: {config['max_tokens']}")
        print(f"  Custo/1K tokens: ${config['cost_per_1k_tokens']}")
        print(f"  Recomendado: {config['recomendado']}")
    
    print(f"\nPara usar um modelo específico:")
    print(f"  python -m analyzer.main bugs-ai arquivo.py --model gpt-3.5-turbo")
    print(f"  Ou configure OPENAI_MODEL no arquivo .env")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python -m analyzer.analyze_bugs_ai <arquivo> [opções]")
        print("\nOpções:")
        print("  --language <lang>     Linguagem do código (padrão: python)")
        print("  --no-cache           Ignorar cache")
        print("  --model <model>      Modelo a usar (padrão: gpt-3.5-turbo)")
        print("  --api-key <key>      Chave da API")
        print("  --simple             Modo simplificado")
        print("  --clear-cache        Limpar cache")
        print("  --list-models        Listar modelos disponíveis")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Parse argumentos
    language = "python"
    no_cache = False
    model = None
    api_key = None
    simple = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--language" and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--no-cache":
            no_cache = True
            i += 1
        elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--api-key" and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--simple":
            simple = True
            i += 1
        elif sys.argv[i] == "--clear-cache":
            clear_cache()
            sys.exit(0)
        elif sys.argv[i] == "--list-models":
            list_models()
            sys.exit(0)
        else:
            i += 1
    
    if simple:
        analyze_bugs_ai_simple(file_path, language, api_key, no_cache, model)
    else:
        analyze_bugs_ai(file_path, language, api_key, no_cache, model) 