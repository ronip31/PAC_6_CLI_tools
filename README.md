# PAC_6

# Sistema Automatizado de Análise de Código

Este projeto oferece uma ferramenta automatizada para análise de código-fonte, facilitando a contagem de linhas, identificação de funções e classes, além da contabilização de comentários. Desenvolvido especialmente para auxiliar desenvolvedores a melhorar a qualidade e a manutenção de projetos de software.

## História do Usuário

**Como desenvolvedor de sistemas**, desejo um sistema de análise automatizada de código que conte as linhas de código, identifique funções e classes, e contabilize comentários, a fim de melhorar a qualidade e manutenção dos projetos de software.

##  Critérios de Aceitação

### 1. Interface de Linha de Comando (CLI)
- Comandos intuitivos definidos através de bibliotecas como Argparse, Click ou Typer.
- Comando padrão para exibição das opções de ajuda (`--help`).
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


 
 # Contador de Linhas de Código (LOC)

Este script em Python analisa um arquivo Python específico e exibe informações sobre o número de linhas de código, comentários, docstrings, funções e classes.

## Requisitos

Antes de executar o script, você precisa ter o Python instalado em seu sistema. Você pode verificar se o Python está instalado rodando o seguinte comando no terminal:

```sh
python --version
```

Se o Python não estiver instalado, faça o download e instale a partir do site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Instalação da Biblioteca `typer`

Este script usa a biblioteca `typer` para criar a interface de linha de comando. Para instalá-la, use o seguinte comando:

```sh
pip install typer
```

Se desejar suporte a cores para melhor visualização no terminal, também instale `rich`:

```sh
pip install rich
```

## Como Executar o Script

1. Salve o código em um arquivo Python, por exemplo: `contador_loc.py`.
2. No terminal, navegue até o diretório onde o arquivo está salvo.
3. Execute o seguinte comando:

```sh
python contador_loc.py loc <caminho_do_arquivo_python>
```

### Exemplo de Uso

Se você deseja analisar um arquivo chamado `exemplo.py` localizado no mesmo diretório do script, execute:

```sh
python contador_loc.py loc exemplo.py
```

O script exibirá a contagem de linhas de código, comentários, docstrings, funções e classes.

## Possíveis Erros e Soluções

- **Erro: `Arquivo '<caminho>' não encontrado.`**
  - Certifique-se de que o caminho do arquivo passado está correto.
- **Erro: `ModuleNotFoundError: No module named 'typer'`**
  - Certifique-se de que a biblioteca `typer` está instalada executando `pip install typer`.
- **Erro: `Permission denied` ao executar o script**
  - Verifique as permissões do arquivo e tente rodar o comando com `python3` ou `sudo python3` se necessário.


---



