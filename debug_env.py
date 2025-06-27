#!/usr/bin/env python3
"""
Script para diagnosticar problemas com configuração do .env
"""

import os
from dotenv import load_dotenv

def debug_env():
    print("=== DIAGNÓSTICO DE CONFIGURAÇÃO ===")
    
    # 1. Verificar se o arquivo .env existe
    env_file = ".env"
    print(f"1. Arquivo .env existe: {os.path.exists(env_file)}")
    
    if os.path.exists(env_file):
        print(f"   Caminho: {os.path.abspath(env_file)}")
        
        # 2. Ler conteúdo do arquivo .env
        print("\n2. Conteúdo do arquivo .env:")
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                print(f"   {content}")
        except Exception as e:
            print(f"   Erro ao ler arquivo: {e}")
    
    # 3. Carregar variáveis de ambiente
    print("\n3. Carregando variáveis de ambiente...")
    load_dotenv()
    
    # 4. Verificar variáveis
    print("\n4. Variáveis carregadas:")
    
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL')
    
    print(f"   OPENAI_API_KEY: {'Configurada' if api_key else 'NÃO CONFIGURADA'}")
    if api_key:
        print(f"   Tamanho da chave: {len(api_key)} caracteres")
        print(f"   Começa com 'sk-': {api_key.startswith('sk-')}")
        print(f"   Primeiros 10 chars: {api_key[:10]}...")
    
    print(f"   OPENAI_MODEL: {model or 'Não configurado (usará padrão)'}")
    
    # 5. Testar requisição simples
    print("\n5. Testando configuração da API...")
    
    if not api_key:
        print("   ❌ API key não encontrada!")
        return
    
    import requests
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Teste simples para verificar se a chave é válida
        response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
        
        print(f"   Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Chave da API válida!")
            models = response.json()
            available_models = [m['id'] for m in models['data'] if 'gpt' in m['id']]
            print(f"   Modelos GPT disponíveis: {available_models[:5]}...")
        elif response.status_code == 401:
            print("   ❌ Chave da API inválida!")
        elif response.status_code == 429:
            print("   ⚠️ Rate limit atingido!")
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
    
    print("\n=== FIM DO DIAGNÓSTICO ===")

if __name__ == "__main__":
    debug_env() 