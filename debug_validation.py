#!/usr/bin/env python3

def is_comment_or_blank(line: str) -> bool:
    """Verifica se uma linha é comentário ou em branco."""
    stripped = line.strip()
    return stripped == '' or stripped.startswith('#')

def filter_block(lines):
    """Remove linhas em branco e comentários de um bloco."""
    return [line for line in lines if not is_comment_or_blank(line)]

def hash_block(lines):
    """Gera um hash SHA-1 para um bloco de linhas."""
    filtered_lines = filter_block(lines)
    if not filtered_lines:
        return ''
    block_str = '\n'.join(filtered_lines)
    return hashlib.sha1(block_str.encode('utf-8')).hexdigest()

import hashlib

# Lendo o arquivo
with open('examples/sample.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== VALIDAÇÃO MANUAL ===")
print(f"Total de linhas no arquivo: {len(lines)}")

# Verificando algumas duplicações específicas
print("\n=== Verificando blocos de 2 linhas ===")

# Bloco 9-10
block_9_10 = lines[8:10]  # 0-indexed
print(f"Linhas 9-10: {repr(block_9_10)}")
filtered_9_10 = filter_block(block_9_10)
print(f"Após filtro: {repr(filtered_9_10)}")
hash_9_10 = hash_block(block_9_10)
print(f"Hash: {hash_9_10[:8]}...")

# Bloco 10-11
block_10_11 = lines[9:11]
print(f"Linhas 10-11: {repr(block_10_11)}")
filtered_10_11 = filter_block(block_10_11)
print(f"Após filtro: {repr(filtered_10_11)}")
hash_10_11 = hash_block(block_10_11)
print(f"Hash: {hash_10_11[:8]}...")

print(f"\nHashes iguais? {hash_9_10 == hash_10_11}")

print("\n=== Verificando blocos de 3 linhas ===")
# Bloco 9-11
block_9_11 = lines[8:11]
print(f"Linhas 9-11: {repr(block_9_11)}")
filtered_9_11 = filter_block(block_9_11)
print(f"Após filtro: {repr(filtered_9_11)}")
hash_9_11 = hash_block(block_9_11)
print(f"Hash: {hash_9_11[:8]}...")

# Bloco 10-12
block_10_12 = lines[9:12]
print(f"Linhas 10-12: {repr(block_10_12)}")
filtered_10_12 = filter_block(block_10_12)
print(f"Após filtro: {repr(filtered_10_12)}")
hash_10_12 = hash_block(block_10_12)
print(f"Hash: {hash_10_12[:8]}...")

print(f"\nHashes iguais? {hash_9_11 == hash_10_12}")

print("\n=== Verificando duplicações de classes ===")
# Verificando as classes duplicadas
print("Linhas 14-15 (classe):")
block_14_15 = lines[13:15]
print(f"Conteúdo: {repr(block_14_15)}")
filtered_14_15 = filter_block(block_14_15)
print(f"Após filtro: {repr(filtered_14_15)}")
hash_14_15 = hash_block(block_14_15)
print(f"Hash: {hash_14_15[:8]}...")

print("Linhas 24-25 (classe):")
block_24_25 = lines[23:25]
print(f"Conteúdo: {repr(block_24_25)}")
filtered_24_25 = filter_block(block_24_25)
print(f"Após filtro: {repr(filtered_24_25)}")
hash_24_25 = hash_block(block_24_25)
print(f"Hash: {hash_24_25[:8]}...")

print(f"Hashes iguais? {hash_14_15 == hash_24_25}")

print("\n=== Verificando duplicações de funções ===")
# Verificando as funções duplicadas
print("Linhas 16-18 (função):")
block_16_18 = lines[15:18]
print(f"Conteúdo: {repr(block_16_18)}")
filtered_16_18 = filter_block(block_16_18)
print(f"Após filtro: {repr(filtered_16_18)}")
hash_16_18 = hash_block(block_16_18)
print(f"Hash: {hash_16_18[:8]}...")

print("Linhas 19-21 (função):")
block_19_21 = lines[18:21]
print(f"Conteúdo: {repr(block_19_21)}")
filtered_19_21 = filter_block(block_19_21)
print(f"Após filtro: {repr(filtered_19_21)}")
hash_19_21 = hash_block(block_19_21)
print(f"Hash: {hash_19_21[:8]}...")

print(f"Hashes iguais? {hash_16_18 == hash_19_21}") 