# PAC_6

# Sistema Automatizado de Análise de Código

Este projeto oferece uma ferramenta automatizada para análise de código-fonte, facilitando a contagem de linhas, identificação de funções e classes, além da contabilização de comentários. Desenvolvido especialmente para auxiliar desenvolvedores a melhorar a qualidade e a manutenção de projetos de software.

## História do Usuário

Como desenvolvedor de sistemas, desejo um sistema de análise automatizada de código que conte as linhas de código, identifique funções e classes, e contabilize comentários, a fim de melhorar a qualidade e manutenção dos projetos de software.

## Critérios de Aceitação

### 1. Interface de Linha de Comando (CLI)
- Comandos intuitivos definidos através de bibliotecas como Typer.
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

---

# Code Analyzer CLI

## Sobre o Projeto

O **Code Analyzer CLI** é uma ferramenta de linha de comando desenvolvida em Python para análise de código-fonte Python. A ferramenta permite realizar diversas análises, incluindo:

- Contagem de linhas de código
- Contagem de comentários
- Contagem de docstrings
- Contagem de classes
- Contagem de funções

---

## Requisitos

Antes de executar o projeto, você precisa ter o Python instalado. Verifique com:

```bash
python --version
```

Instale a versão mais recente a partir de: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/PAC_6_CLI_tools.git
cd PAC_6_CLI_tools
```

### 2. Instale em modo desenvolvimento

Esse modo permite que qualquer alteração no código seja refletida automaticamente.

```bash
pip install -e .
```

---

## Uso da CLI

Depois da instalação, você poderá usar o comando `analyzer` diretamente no terminal.

### Comandos Disponíveis

| Comando               | Descrição                                               |
|-----------------------|---------------------------------------------------------|
| `all`                | Analisa todas as métricas do código                     |
| `lines`              | Conta o número total de linhas no código                |
| `comments`           | Conta o número de comentários no código                 |
| `docstrings`         | Conta o número de docstrings no código                  |
| `classes`            | Conta o número de classes no código                     |
| `functions`          | Conta o número de funções no código                     |
| `--version` / `-v`   | Exibe a versão da ferramenta                            |
| `--help`             | Exibe o menu de ajuda personalizado                     |

---

## Comandos Auxiliares de Testes

Esses comandos são executados diretamente no terminal após a instalação do projeto:

| Comando               | Descrição                                               |
|-----------------------|---------------------------------------------------------|
| `runtests`           | Executa todos os testes automatizados                   |
| `runtests-verbose`   | Executa todos os testes com saída detalhada             |
| `runtests-failures`  | Executa apenas os testes que falharam anteriormente     |

---

### Exemplos de Uso

#### Analisar todas as métricas de um arquivo:

```bash
analyzer all examples/sample.py
```

#### Analisar somente comentários:

```bash
analyzer comments examples/sample.py
```

#### Exibir versão da ferramenta:

```bash
analyzer --version
```

#### Ver ajuda geral (com comandos formatados):

```bash
analyzer --help
```

---

## Análise em Lote (vários arquivos)

### Windows (PowerShell)

```powershell
Get-ChildItem -Path examples -Filter "*.py" | ForEach-Object { analyzer all $_.FullName }
```

### Linux/macOS (Bash)

```bash
for file in examples/*.py; do analyzer all "$file"; done
```

---

## Testes

Você também pode rodar os testes diretamente com `pytest` se preferir:

### Executar todos os testes:

```bash
python -m pytest tests/
```

### Executar teste específico:

```bash
python -m pytest tests/test_lines.py
```

### Execução com saída detalhada:

```bash
python -m pytest -v tests/
```

### Executar somente testes que falharam anteriormente:

```bash
python -m pytest --lf
```

---

## Licença

Este projeto é open-source e está sob a licença MIT.

---