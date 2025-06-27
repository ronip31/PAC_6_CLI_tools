#!/usr/bin/env python3
"""
Exemplo de código com problemas para testar análise de bugs com IA.
"""

import os
import sys

# Problema de segurança: input sem validação
user_input = input("Digite algo: ")
print(f"Você digitou: {user_input}")

# Problema de performance: loop ineficiente
def slow_function():
    result = []
    for i in range(1000):
        result.append(i * 2)
    return result

# Problema de qualidade: variável não utilizada
unused_variable = "não uso isso"

# Problema de manutenibilidade: função muito longa sem documentação
def complex_function_without_docstring(a, b, c, d, e, f, g, h, i, j):
    x = a + b
    y = c * d
    z = e / f
    w = g ** h
    v = i % j
    result = x + y + z + w + v
    if result > 100:
        result = result * 2
    elif result < 0:
        result = result * -1
    else:
        result = result + 1
    return result

# Problema de segurança: exec com input do usuário
def dangerous_function():
    code = input("Digite código Python: ")
    exec(code)  # Perigoso!

# Problema de qualidade: código duplicado
def duplicate_function1():
    x = 1
    y = 2
    z = x + y
    return z

def duplicate_function2():
    x = 1
    y = 2
    z = x + y
    return z

# Problema de performance: lista desnecessária
def inefficient_function():
    numbers = []
    for i in range(100):
        numbers.append(i)
    return sum(numbers)

# Problema de manutenibilidade: números mágicos
def magic_numbers():
    if age > 18 and age < 65:  # Números mágicos
        return "adulto"
    elif age < 18:
        return "menor"
    else:
        return "idoso"

# Problema de segurança: senha hardcoded
password = "senha123"  # Nunca faça isso!

# Problema de qualidade: exceção muito genérica
def bad_exception_handling():
    try:
        result = 10 / 0
    except:  # Muito genérico
        print("Erro aconteceu")

# Problema de performance: string concatenation em loop
def slow_string_operation():
    result = ""
    for i in range(1000):
        result += str(i)  # Ineficiente
    return result

if __name__ == "__main__":
    # Executa algumas funções problemáticas
    slow_function()
    dangerous_function()
    inefficient_function()
    bad_exception_handling()
    slow_string_operation() 