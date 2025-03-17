# **Sistema Automatizado de Análise de Código**

Este projeto oferece uma ferramenta automatizada para análise de código-fonte Python, facilitando a contagem de linhas, identificação de funções e classes, além da contabilização de comentários. Desenvolvido para ajudar desenvolvedores a melhorar a qualidade e manutenção de seus projetos de software.  

## **História do Usuário**  
Como desenvolvedor de sistemas, desejo um sistema de análise automatizada de código que conte as linhas de código, identifique funções e classes e contabilize comentários, a fim de melhorar a qualidade e manutenção dos projetos de software.  

## **Critérios de Aceitação**  

### 1. **Interface de Linha de Comando (CLI)**  
- Comandos intuitivos, definidos com a biblioteca `Typer`.  
- Exibição das opções de ajuda com `--help`.  
- Validação clara e precisa dos argumentos e parâmetros fornecidos.  

### 2. **Contagem de Linhas de Código (LOC)**  
- Contagem precisa das linhas de código de um arquivo Python.  
- Opção para incluir ou excluir linhas vazias na contagem.  

### 3. **Identificação e Contagem de Funções e Classes**  
- Identificação correta de funções (`def`) e classes (`class`) usando expressões regulares.  
- Contagem separada de funções e classes.  

### 4. **Contagem de Comentários**  
- Detecção precisa de comentários (`#`) e docstrings (`""" """`).  
- Uso de expressões regulares robustas para precisão.  

### 5. **Geração Automática de Relatórios**  
- Suporte a múltiplos formatos (`CSV`, `JSON`, `TXT`).  
- Consolidação dos resultados das análises.  

### 6. **Documentação**  
- README detalhado com explicação dos comandos e exemplos.  
- Processo de execução de testes e interpretação dos resultados.  

---

## **Requisitos**
Antes de executar o script, verifique se o Python está instalado:  
```bash
python --version
```  
Se não estiver instalado, faça o download [aqui](https://www.python.org/downloads/).  

## **Instalação**  

### 1. Clone o repositório  
```bash
git clone https://github.com/seu-usuario/PAC_6_CLI_tools.git
cd PAC_6_CLI_tools
```

### 2. Instale as dependências  
```bash
pip install -r requirements.txt
```

---

## **Uso**  
Para visualizar a ajuda geral da ferramenta:  
```bash
python -m analyzer.main --help
```

### **Comandos Disponíveis**
| Comando               | Descrição                                          |
|-----------------------|--------------------------------------------------|
| `analyze-all`        | Analisa todas as métricas do código              |
| `analyze-lines`      | Conta o número total de linhas no código         |
| `analyze-comments`   | Conta o número de comentários no código          |
| `analyze-docstrings` | Conta o número de docstrings no código           |
| `analyze-classes`    | Conta o número de classes no código              |
| `analyze-functions`  | Conta o número de funções no código              |

### **Exemplo de Uso**
Para analisar um arquivo `sample.py` e obter todas as métricas:  
```bash
python -m analyzer.main analyze-all examples/sample.py
```

#### **Saída esperada:**  
```bash
Arquivo: examples/sample.py
Total de linhas: 13
Comentários: 2
Docstrings: 3
Classes: 1
Funções: 1
```

Para analisar apenas os comentários:  
```bash
python -m analyzer.main analyze-comments examples/sample.py
```

### **Analisando um Diretório Completo**
Para analisar todos os arquivos `.py` em um diretório:

#### **Windows (PowerShell):**  
```powershell
Get-ChildItem -Path examples -Filter "*.py" | ForEach-Object { python -m analyzer.main analyze-all $_.FullName }
```

#### **Linux/macOS (Bash):**  
```bash
find examples -name "*.py" -exec python -m analyzer.main analyze-all {} \;
```

---

## **Testes**  
Para rodar todos os testes unitários:  
```bash
pytest tests/
```  
Para rodar `pytest` diretamente via Python:  
```bash
python -m pytest tests/
```

### **Rodando Testes Específicos**  
Para testar apenas `test_lines.py`:  
```bash
pytest tests/test_lines.py
```
Para rodar testes com saída detalhada:  
```bash
pytest -v tests/
```
Para rodar apenas os testes que falharam anteriormente:  
```bash
pytest --lf
```

---

## **Licença**  
Este projeto é open-source e está sob a licença MIT.

