#!/usr/bin/env python3

from analyzer.analyze_function_size import calculate_function_sizes

def test_simple():
    # Teste 1: Função simples
    code1 = "def minha_funcao():\n    pass"
    count1, avg1 = calculate_function_sizes(code1)
    print(f"Teste 1 - Função simples: {count1} funções, média: {avg1:.1f} linhas")
    assert count1 == 1
    assert avg1 == 2.0
    
    # Teste 2: Múltiplas funções
    code2 = """def funcao1():
    print("hello")
    return True

def funcao2():
    pass"""
    
    count2, avg2 = calculate_function_sizes(code2)
    print(f"Teste 2 - Múltiplas funções: {count2} funções, média: {avg2:.1f} linhas")
    assert count2 == 2
    assert avg2 == 3.0
    
    # Teste 3: Sem funções
    code3 = "print('Hello')\nx = 10"
    count3, avg3 = calculate_function_sizes(code3)
    print(f"Teste 3 - Sem funções: {count3} funções, média: {avg3:.1f} linhas")
    assert count3 == 0
    assert avg3 == 0
    
    print("Todos os testes passaram!")

if __name__ == "__main__":
    test_simple() 