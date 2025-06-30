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
| `duplicate-code`     | Identifica blocos de código duplicados no arquivo      |
| `function-size`      | Analisa o tamanho médio das funções no código         |
| `analyze-complexity` | Analisa a complexidade assintótica das funções        |
| `analyze-dead-code`  | Identifica funções e classes não utilizadas (código morto) |
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

#### Analisar código duplicado:

```bash
# Modo automático (tamanhos de bloco de 2 a 10 linhas)
analyzer duplicate-code examples/sample.py

# Especificando tamanho do bloco (ex: 5 linhas)
analyzer duplicate-code examples/sample.py --block-size 5
```

#### Analisar tamanho médio das funções:

```bash
analyzer function-size examples/sample.py
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

## Análise de Bugs com IA (OpenAI)

A ferramenta oferece um comando para análise automática de bugs, problemas de qualidade e sugestões de melhoria usando modelos de IA da OpenAI (como GPT-3.5-turbo).

### Configuração da API

Para usar a análise de bugs com IA, é necessário configurar uma chave de API da OpenAI. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo  # (opcional, pode ser: gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-4, gpt-4-turbo)
```

- A chave pode ser obtida em https://platform.openai.com/api-keys
- O modelo é opcional (padrão: gpt-3.5-turbo)
- Você também pode definir essas variáveis diretamente no ambiente ou passar via parâmetro CLI

### Uso do Cache

Para evitar limites de uso da API, a ferramenta armazena localmente os resultados das análises em um cache. Se o mesmo código for analisado novamente, o resultado será carregado instantaneamente do cache, sem consumir requisições da OpenAI.

- O cache é salvo no diretório `.cache`.
- Para ignorar o cache, use a opção `--no-cache`.
- Para limpar o cache, use `--clear-cache`.

### Comando de Análise de Bugs

Você pode rodar a análise de bugs diretamente:

```bash
python -m analyzer.analyze_bugs_ai <arquivo.py> [opções]
```

#### Opções principais:
- `--language <lang>`: Linguagem do código (padrão: python)
- `--no-cache`: Ignorar cache
- `--model <model>`: Modelo a usar (padrão: gpt-3.5-turbo)
- `--api-key <key>`: Chave da API (sobrepõe .env)
- `--simple`: Saída simplificada
- `--clear-cache`: Limpa o cache
- `--list-models`: Lista modelos disponíveis

#### Exemplos:

```bash
# Análise padrão
python -m analyzer.analyze_bugs_ai examples/sample.py

# Usando modelo gpt-4
python -m analyzer.analyze_bugs_ai examples/sample.py --model gpt-4

# Ignorando cache
python -m analyzer.analyze_bugs_ai examples/sample.py --no-cache

# Limpar cache
python -m analyzer.analyze_bugs_ai --clear-cache
```

### Notas sobre Limites da API
- Se receber erro 429 (Too Many Requests), aguarde alguns minutos e tente novamente.
- O cache ajuda a evitar requisições repetidas.
- Contas gratuitas possuem limites baixos de requisições.

---

# Quality Server (Servidor de Indicadores de Qualidade)

O **Quality Server** é um servidor web leve e eficiente para receber, armazenar e consultar indicadores de qualidade de projetos de software. Ele permite centralizar e visualizar as métricas geradas pelo Analyzer CLI.

## Como rodar o Quality Server

### 1. Instale as dependências

```bash
cd quality_server
pip install -r requirements.txt
```

### 2. Rode o servidor

```bash
uvicorn app.main:app --reload
```

> O servidor estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Como utilizar

### API RESTful
- **POST /projects** — Envie projetos e métricas no formato esperado (veja exemplos no `/docs`)
- **GET /projects** — Consulte todos os projetos e métricas (retorna JSON ou interface web)
- **GET /projects/{project_id}/history** — Histórico de métricas de um projeto
- **POST /upload-raw** — Envie o JSON bruto gerado pelo Analyzer CLI

### Interface Web
- Acesse [http://127.0.0.1:8000/projects](http://127.0.0.1:8000/projects) para visualizar todos os projetos e métricas em uma tabela amigável.
- Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para explorar e testar a API interativamente (Swagger UI).

### Exemplo de envio de métricas via API

```bash
curl -X POST "http://127.0.0.1:8000/projects" -H "Content-Type: application/json" -d '{
  "name": "MeuProjeto",
  "metrics": [
    {
      "timestamp": "2024-05-20T12:00:00",
      "data": {
        "lines": 100,
        "comments": 10,
        "functions": 5
      }
    }
  ]
}'
```

Ou envie o JSON bruto gerado pelo Analyzer CLI:

```bash
curl -X POST "http://127.0.0.1:8000/upload-raw" -H "Content-Type: application/json" -d @resultadooo.json
```

---