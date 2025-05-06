# PAC_6

Alunos: 
        Alberto Zilio
        Lucas Steffens
        Roni Pereira

# Sistema Automatizado de Análise de Código

Este projeto oferece uma ferramenta automatizada para análise de código-fonte, facilitando a contagem de linhas, identificação de funções, classes e métodos (públicos/privados), além da contabilização de comentários. Desenvolvido especialmente para auxiliar desenvolvedores a melhorar a qualidade e a manutenção de projetos de software.

## História do Usuário

Como desenvolvedor de sistemas, desejo um sistema de análise automatizada de código que conte as linhas de código, identifique funções, classes e métodos (públicos/privados), e contabilize comentários, a fim de melhorar a qualidade e manutenção dos projetos de software.

## Critérios de Aceitação

### 1. Interface de Linha de Comando (CLI)
- Comandos intuitivos definidos através de bibliotecas como Typer.
- Comando padrão para exibição das opções de ajuda (--help).
- Validação clara e precisa dos argumentos e parâmetros fornecidos pelo usuário.
- Menu de ajuda com informações claras sobre cada comando disponível.
- Suporte a diferentes formatos de saída (CLI e JSON).

### 2. Contagem de Linhas de Código (LOC)
- Contagem precisa das linhas de código em um arquivo fornecido pelo usuário.
- Opção para incluir ou excluir linhas vazias na contagem.
- Mensagens claras de erro em casos de arquivo inexistente ou corrompido.

### 3. Identificação e Contagem de Funções, Classes e Métodos
- Identificação e contagem correta de funções (`def`), classes (`class`) e métodos usando expressões regulares em Python.
- Distinção entre métodos públicos e privados.
- Cálculo da proporção entre métodos públicos e privados.
- Retorno separado da contagem de funções, classes e métodos.
- Mensagens amigáveis para padrões inesperados ou arquivos ilegíveis.

### 4. Contagem de Comentários
- Detecção precisa de comentários em Python (`#`).
- Uso de expressões regulares robustas para precisão.
- Retorno claro do número específico de linhas comentadas.

### 5. Geração Automática de Relatórios
- Escolha de formato do relatório (CLI ou JSON) via argumento.
- Consolidação clara dos resultados das análises.
- Suporte a análise de arquivos individuais ou diretórios completos.
- Relatório objetivo e fácil de interpretar.
- Informações claras sobre erros durante a geração do relatório.

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
- Análise de métodos (públicos/privados)
- Análise de indentação
- Análise de dependências
- Proporção de comentários por unidade de código

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
git clone https://github.com/ronip31/PAC_6_CLI_tools
cd PAC_6_CLI_tools
```

#### 2. Crie e ative o ambiente virtual

##### Windows PowerShell:

```powershell
python -m venv venv

.\venv\Scripts\activate
```
##### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale em modo desenvolvimento

```bash
pip install -e .
```

> ⚠️ **Importante:** certifique-se de ativar o ambiente virtual antes de rodar o comando acima, para que o comando `analyzer` fique disponível corretamente no terminal.

---

### ✅ Verificando o comando

Após instalar, você pode verificar se o comando foi instalado corretamente com:

```bash
analyzer -v
```
ou

```bash
analyzer --version
```


---

## Uso da CLI

Depois da instalação, você poderá usar o comando `analyzer` diretamente no terminal.

### Comandos Disponíveis

| Comando               | Descrição                                               |
|-----------------------|---------------------------------------------------------|
| `all`                | Analisa todas as métricas de um arquivo                |
| `all-dir`            | Analisa todas as métricas de arquivos em um diretório |
| `lines`              | Conta o número total de linhas no código                |
| `comments`           | Conta o número de comentários no código                 |
| `docstrings`         | Conta o número de docstrings no código                  |
| `classes`            | Conta o número de classes no código                     |
| `functions`          | Conta o número de funções no código                     |
| `methods`            | Analisa os métodos públicos e privados no código       |
| `indent`             | Analisa os níveis de indentação                        |
| `dependencies`       | Analisa as dependências externas do código             |
| `comment-ratio`      | Calcula o percentual de comentários por unidade        |
| `--version` / `-v`   | Exibe a versão da ferramenta                           |
| `--help`             | Exibe o menu de ajuda personalizado                     |

### Opções de Formato

Os comandos `all` e `all-dir` aceitam as seguintes opções:

| Opção                | Descrição                                               |
|-----------------------|---------------------------------------------------------|
| `--format` / `-f`    | Formato de saída (cli ou json)                         |
| `--output` / `-o`    | Arquivo de saída para formato json                     |

---

### Exemplos de Uso

#### Analisar todas as métricas de um arquivo:

```bash
# Saída padrão (CLI)
analyzer all examples/sample.py

# Saída em JSON
analyzer all examples/sample.py --format json

# Salvar resultado em arquivo JSON
analyzer all examples/sample.py --format json --output resultado.json
```

#### Analisar todas as métricas de um diretório:

```bash
# Saída padrão (CLI)
analyzer all-dir examples/

# Saída em JSON
analyzer all-dir examples/ --format json

# Salvar resultado em arquivo JSON
analyzer all-dir examples/ --format json --output resultado.json
```

#### Analisar somente métodos:

```bash
analyzer methods examples/sample.py
```

#### Exibir versão da ferramenta:

```bash
analyzer --version
```

#### Ver ajuda geral:

```bash
analyzer --help
```

#### Ver ajuda específica de um comando:

```bash
analyzer all --help
analyzer all-dir --help
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