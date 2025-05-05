# Código genérico para testar a classe ProporcaoComentarioCodigo

def testar_proporcao_comentario_codigo():
    # Caminho para o arquivo Python a ser analisado
    caminho_arquivo = 'exemplo.py'  # Altere para o caminho do seu arquivo Python

    # Criando uma instância da classe
    analisador = ProporcaoComentarioCodigo(caminho_arquivo)

    # Realizando a análise
    resultados = analisador.analisar()

    # Exibindo os resultados
    print(f"Resultados da análise do arquivo {caminho_arquivo}:\n")
    for resultado in resultados:
        print(f"Nome: {resultado['nome']}")
        print(f"  Linhas totais: {resultado['linhas_totais']}")
        print(f"  Comentários: {resultado['comentarios']}")
        print(f"  Percentual de comentários: {resultado['percentual']}%\n")


if __name__ == "__main__":
    testar_proporcao_comentario_codigo()
