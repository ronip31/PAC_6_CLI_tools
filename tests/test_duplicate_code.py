from analyzer.analyze_duplicate_code import find_duplicate_blocks, hash_block

def test_hash_block():
    """Testa a geração de hash para blocos de código."""
    lines = ["def test():", "    pass", "    return True"]
    hash1 = hash_block(lines)
    hash2 = hash_block(lines)
    assert hash1 == hash2  # Mesmo bloco deve gerar mesmo hash
    
    # Blocos diferentes devem gerar hashes diferentes
    lines2 = ["def test():", "    pass", "    return False"]
    hash3 = hash_block(lines2)
    assert hash1 != hash3

def test_find_duplicate_blocks_simple():
    """Testa detecção de blocos duplicados simples."""
    code = """def funcao1():
    x = 10
    y = 20
    return x + y

def funcao2():
    x = 10
    y = 20
    return x + y"""
    
    duplicates = find_duplicate_blocks(code, block_size=3)
    assert len(duplicates) >= 2  # Pelo menos 2 ocorrências do bloco duplicado

def test_find_duplicate_blocks_no_duplicates():
    """Testa quando não há blocos duplicados."""
    code = """def funcao1():
    x = 10
    return x

def funcao2():
    y = 20
    return y"""
    
    duplicates = find_duplicate_blocks(code, block_size=3)
    assert len(duplicates) == 0

def test_find_duplicate_blocks_with_comments():
    """Testa detecção com comentários."""
    code = """def funcao1():
    x = 10
    return x

def funcao2():
    x = 10
    return x"""
    
    duplicates = find_duplicate_blocks(code, block_size=2)
    assert len(duplicates) >= 2

def test_find_duplicate_blocks_ignore_blank():
    """Testa que blocos só de linhas em branco são ignorados."""
    code = """def funcao1():
    pass

def funcao2():
    pass"""
    
    duplicates = find_duplicate_blocks(code, block_size=3)
    # Não deve encontrar duplicatas de blocos só com linhas em branco
    assert len(duplicates) == 0

def test_find_duplicate_blocks_different_sizes():
    """Testa diferentes tamanhos de bloco."""
    code = """def funcao1():
    x = 10
    y = 20
    z = 30
    return x + y + z

def funcao2():
    x = 10
    y = 20
    z = 30
    return x + y + z"""
    
    # Bloco de 4 linhas
    duplicates_4 = find_duplicate_blocks(code, block_size=4)
    assert len(duplicates_4) >= 2
    
    # Bloco de 2 linhas
    duplicates_2 = find_duplicate_blocks(code, block_size=2)
    assert len(duplicates_2) >= 2 