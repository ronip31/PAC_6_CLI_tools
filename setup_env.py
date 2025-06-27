#!/usr/bin/env python3
"""
Script para configurar o arquivo .env com a chave da API da OpenAI.
"""

import os
import getpass

def create_env_file():
    """Cria ou atualiza o arquivo .env com a chave da API."""
    
    print("Configuração do arquivo .env")
    print("=" * 40)
    
    # Verifica se o arquivo .env já existe
    env_file = ".env"
    existing_key = None
    
    if os.path.exists(env_file):
        print(f"Arquivo {env_file} já existe.")
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    existing_key = line.split('=', 1)[1].strip()
                    if existing_key and existing_key != 'sua_chave_aqui':
                        print(f"Chave atual: {existing_key[:10]}...")
                        break
        
        if existing_key and existing_key != 'sua_chave_aqui':
            response = input("Deseja sobrescrever a chave existente? (s/N): ").lower()
            if response != 's':
                print("Configuração cancelada.")
                return
    
    # Solicita a nova chave
    print("\nPara obter sua chave da OpenAI:")
    print("1. Acesse: https://platform.openai.com/api-keys")
    print("2. Faça login ou crie uma conta")
    print("3. Clique em 'Create new secret key'")
    print("4. Copie a chave (começa com 'sk-')")
    print()
    
    api_key = getpass.getpass("Digite sua chave da API da OpenAI (será ocultada): ").strip()
    
    if not api_key:
        print("Chave não fornecida. Configuração cancelada.")
        return
    
    if not api_key.startswith('sk-'):
        print("Aviso: A chave da OpenAI geralmente começa com 'sk-'. Verifique se está correta.")
        confirm = input("Continuar mesmo assim? (s/N): ").lower()
        if confirm != 's':
            print("Configuração cancelada.")
            return
    
    # Cria o arquivo .env
    env_content = f"""# Configurações da API OpenAI
OPENAI_API_KEY={api_key}

# Outras configurações que podem ser adicionadas no futuro
# MODEL=gpt-3.5-turbo
# MAX_TOKENS=2000
# TEMPERATURE=0.3
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\nArquivo {env_file} criado/atualizado com sucesso!")
        print("Agora você pode usar os comandos de análise de bugs com IA.")
        print("\nExemplo:")
        print("  python -m analyzer.main bugs-ai examples/buggy_code.py")
        
    except Exception as e:
        print(f"Erro ao criar arquivo {env_file}: {e}")

def test_configuration():
    """Testa se a configuração está funcionando."""
    print("\nTestando configuração...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'sua_chave_aqui':
            print("✓ Configuração OK! Chave da API carregada.")
            print(f"  Chave: {api_key[:10]}...")
        else:
            print("✗ Configuração não encontrada.")
            print("  Execute este script novamente para configurar.")
    except ImportError:
        print("✗ Biblioteca python-dotenv não encontrada.")
        print("  Execute: pip install python-dotenv")

if __name__ == "__main__":
    create_env_file()
    test_configuration() 