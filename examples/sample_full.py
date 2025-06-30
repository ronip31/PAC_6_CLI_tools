"""
Exemplo completo para análise de métricas de código.
Inclui funções, classes, docstrings, comentários, duplicação, diferentes níveis de indentação e múltiplas dependências externas.
"""

import math
import typer
import requests
import numpy as np
import pandas as pd
from rich.console import Console
from datetime import datetime

# Função simples
# Comentário de linha

def soma(a, b):
    """Soma dois números."""
    return a + b

# Função com loop

def produto(lista):
    """Multiplica todos os elementos de uma lista."""
    resultado = 1
    for x in lista:
        resultado *= x
    return resultado

# Função duplicada propositalmente

def produto_duplicado(lista):
    resultado = 1
    for x in lista:
        resultado *= x
    return resultado

# Classe com métodos públicos e privados
class Calculadora:
    """Classe de exemplo para análise."""
    def __init__(self):
        self._memoria = 0

    def somar(self, x, y):
        """Soma dois valores."""
        return x + y

    def _armazenar(self, valor):
        self._memoria = valor

    def memoria(self):
        return self._memoria

# Classe duplicada propositalmente
class CalculadoraDuplicada:
    def __init__(self):
        self._memoria = 0
    def somar(self, x, y):
        return x + y
    def _armazenar(self, valor):
        self._memoria = valor
    def memoria(self):
        return self._memoria

# Função recursiva

def fatorial(n):
    """Calcula o fatorial de n."""
    if n <= 1:
        return 1
    return n * fatorial(n-1)

# Função com docstring e múltiplos comentários

def exemplo_comentado(x):
    """Exemplo com muitos comentários."""
    # Este é um comentário
    # Outro comentário
    if x > 0:
        # Comentário dentro do if
        return True
    # Comentário final
    return False 