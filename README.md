# PAC_6
 
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

## Contribuições

Sinta-se à vontade para melhorar este script e compartilhar sugestões! Abra um pull request ou envie um issue no repositório onde ele estiver hospedado.

---

Autor: [Seu Nome]

