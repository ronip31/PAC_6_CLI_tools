import typer
import hashlib
from collections import defaultdict
from typing import List, Tuple

def is_comment_or_blank(line: str) -> bool:
    """Verifica se uma linha é comentário ou em branco."""
    stripped = line.strip()
    return stripped == '' or stripped.startswith('#')

def filter_block(lines: List[str]) -> List[str]:
    """Remove linhas em branco e comentários de um bloco."""
    return [line for line in lines if not is_comment_or_blank(line)]

def hash_block(lines: List[str]) -> str:
    """Gera um hash SHA-1 para um bloco de linhas, ignorando comentários e linhas em branco."""
    filtered_lines = filter_block(lines)
    if not filtered_lines:
        return ''  # Bloco vazio após filtragem
    block_str = '\n'.join(filtered_lines)
    return hashlib.sha1(block_str.encode('utf-8')).hexdigest()

def find_duplicate_blocks(code: str, block_size: int = 5) -> List[Tuple[int, int, str]]:
    """
    Encontra blocos de código duplicados, ignorando comentários e linhas em branco.
    Retorna uma lista de tuplas: (linha_inicial, linha_final, hash)
    """
    lines = code.split('\n')
    hashes = defaultdict(list)  # hash -> lista de linhas iniciais
    
    for i in range(len(lines) - block_size + 1):
        block = lines[i:i+block_size]
        h = hash_block(block)
        if not h:
            continue  # ignora blocos vazios após filtragem
        hashes[h].append(i+1)  # linha inicial (1-indexed)
    
    # Filtra apenas hashes com mais de uma ocorrência
    duplicates = []
    for h, starts in hashes.items():
        if len(starts) > 1:
            for start in starts:
                duplicates.append((start, start+block_size-1, h))
    return duplicates

def find_all_duplicates(code: str, min_size: int = 2, max_size: int = 10) -> dict:
    """
    Encontra duplicações em múltiplos tamanhos de bloco.
    Retorna um dicionário com os resultados por tamanho.
    """
    results = {}
    for size in range(min_size, max_size + 1):
        duplicates = find_duplicate_blocks(code, size)
        if duplicates:
            results[size] = duplicates
    return results

def analyze_duplicate_code(file: str, block_size: int = None, auto: bool = False):
    """
    Função CLI para identificar blocos duplicados em um arquivo.
    """
    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    if auto or block_size is None:
        # Modo automático: testa múltiplos tamanhos
        print("🔍 Analisando duplicações em múltiplos tamanhos de bloco...")
        print("ℹ️  Ignorando comentários e linhas em branco")
        all_duplicates = find_all_duplicates(code, min_size=2, max_size=10)
        
        if not all_duplicates:
            print("Nenhum bloco duplicado encontrado em nenhum tamanho (2-10 linhas).")
            return
        
        print(f"\n📊 Resultados encontrados:")
        for size, duplicates in all_duplicates.items():
            print(f"\n🔸 Blocos de {size} linhas ({len(duplicates)} duplicações):")
            for start, end, h in duplicates:
                print(f"   Linhas {start}-{end} (hash: {h[:8]}...)")
    else:
        # Modo específico: tamanho definido
        print(f"ℹ️  Ignorando comentários e linhas em branco")
        duplicates = find_duplicate_blocks(code, block_size)
        if not duplicates:
            print(f"Nenhum bloco duplicado de {block_size} linhas encontrado.")
            return
        print(f"Blocos duplicados de {block_size} linhas:")
        for start, end, h in duplicates:
            print(f"Linhas {start}-{end} (hash: {h[:8]}...)") 