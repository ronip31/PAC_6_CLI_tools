PAC_6


# Sistema Automatizado de Análise de Código

Este projeto oferece uma ferramenta automatizada para análise de código-fonte, facilitando a contagem de linhas, identificação de funções e classes, além da contabilização de comentários. Desenvolvido especialmente para auxiliar desenvolvedores a melhorar a qualidade e a manutenção de projetos de software.

## História do Usuário
Como desenvolvedor de sistemas, desejo um sistema de análise automatizada de código que conte as linhas de código, identifique funções e classes, e contabilize comentários, a fim de melhorar a qualidade e manutenção dos projetos de software.

## Critérios de Aceitação
### 1. Interface de Linha de Comando (CLI)
- Comandos intuitivos definidos através de bibliotecas como Argparse, Click ou Typer.
- Comando padrão para exibição das opções de ajuda (--help).
- Validação clara e precisa dos argumentos e parâmetros fornecidos pelo usuário.
- Menu de ajuda com informações claras sobre cada comando disponível.

### 2. Contagem de Linhas de Código (LOC)
- Contagem precisa das linhas de código em um arquivo fornecido pelo usuário.
- Opção para incluir ou excluir linhas vazias na contagem.
- Mensagens claras de erro em casos de arquivo inexistente ou corrompido.

### 3. Identificação e Contagem de Funções e Classes
- Identificação e contagem correta de funções (`def`) e classes (`class`) usando expressões regulares em Python.
- Retorno separado da contagem de funções e classes.
- Mensagens amigáveis para padrões inesperados ou arquivos ilegíveis.

### 4. Contagem de Comentários
- Detecção precisa de comentários em Python (`#`).
- Uso de expressões regulares robustas para precisão.
- Retorno claro do número específico de linhas comentadas.

### 5. Geração Automática de Relatórios
- Escolha de formato do relatório (CSV, JSON ou TXT) via argumento CLI.
- Consolidação clara dos resultados das análises (LOC, funções/classes e comentários).
- Relatório objetivo e fácil de interpretar.
- Informações claras sobre erros durante a geração do relatório (permissões, diretórios inválidos, espaço em disco insuficiente).

### 6. Documentação
- README claro com explicação dos comandos disponíveis, uso e exemplos práticos.
- Explicação detalhada da estrutura interna do projeto e principais métodos.
- Processo detalhado para execução dos testes e interpretação dos resultados.

## Requisitos
Antes de executar o script, você precisa ter o Python instalado em seu sistema. Você pode verificar se o Python está instalado rodando o seguinte comando no terminal:
```bash
python --version
```
Se o Python não estiver instalado, faça o download e instale a partir do site oficial: [Python Downloads](https://www.python.org/downloads/)

## Instalação da Biblioteca Typer
Este script usa a biblioteca `typer` para criar a interface de linha de comando. Para instalá-la, use o seguinte comando:
```bash
pip install typer
```
Se desejar suporte a cores para melhor visualização no terminal, também instale `rich`:
```bash
pip install rich
```

# Code Analyzer CLI

## Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/PAC_6_CLI_tools.git
cd PAC_6_CLI_tools
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

## Uso
Para visualizar a ajuda geral da ferramenta:
```bash
python -m analyzer.main --help
```

### Comandos Disponíveis
| Comando             | Descrição                                         |
|---------------------|-------------------------------------------------|
| `analyze-all`      | Analisa todas as métricas do código              |
| `analyze-lines`    | Conta o número total de linhas no código         |
| `analyze-comments` | Conta o número de comentários no código          |
| `analyze-docstrings` | Conta o número de docstrings no código       |
| `analyze-classes`  | Conta o número de classes no código              |
| `analyze-functions`| Conta o número de funções no código              |

## Testes
Para rodar todos os testes unitários:
```bash
pytest tests/
```
Para rodar `pytest` diretamente via Python:
```bash
python -m pytest tests/
```

### Exemplo de Uso
Para rodar um teste específico, por exemplo `test_lines.py`:
```bash
pytest tests/test_lines.py
```
Para rodar os testes com saída detalhada:
```bash
pytest -v tests/
```
Para rodar apenas os testes que falharam anteriormente:
```bash
pytest --lf
```

## Licença
Este projeto é open-source e está sob a licença MIT.

