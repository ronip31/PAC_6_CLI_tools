from analyzer.analyze_function_size import calculate_function_sizes

def test_calculate_function_sizes_single_function():
    """Testa o cálculo com uma única função simples."""
    code = "def minha_funcao():\n    pass"
    function_count, average_size = calculate_function_sizes(code)
    assert function_count == 1
    assert average_size == 2.0  # linha da definição + linha do pass

def test_calculate_function_sizes_multiple_functions():
    """Testa o cálculo com múltiplas funções."""
    code = """def funcao1():
    print("hello")
    return True

def funcao2():
    pass"""
    
    function_count, average_size = calculate_function_sizes(code)
    assert function_count == 2
    # funcao1: 3 linhas (def + print + return)
    # funcao2: 2 linhas (def + pass)
    # média: (3 + 2) / 2 = 2.5
    assert average_size == 2.5

def test_calculate_function_sizes_no_functions():
    """Testa o cálculo quando não há funções."""
    code = "print('Hello')\nx = 10"
    function_count, average_size = calculate_function_sizes(code)
    assert function_count == 0
    assert average_size == 0

def test_calculate_function_sizes_complex_function():
    """Testa o cálculo com uma função mais complexa."""
    code = """def funcao_complexa():
    if True:
        print("teste")
        for i in range(10):
            print(i)
    return "resultado"
"""
    function_count, average_size = calculate_function_sizes(code)
    assert function_count == 1
    # A função tem 6 linhas (def + if + print + for + print + return)
    assert average_size == 6.0

def test_calculate_function_sizes_with_comments():
    """Testa o cálculo com funções que contêm comentários."""
    code = """def funcao_com_comentario():
    # Este é um comentário
    x = 10
    return x"""
    
    function_count, average_size = calculate_function_sizes(code)
    assert function_count == 1
    # 4 linhas: def + comentário + x = 10 + return
    assert average_size == 4.0 