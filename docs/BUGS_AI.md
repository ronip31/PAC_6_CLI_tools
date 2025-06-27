# 🤖 Análise de Bugs com IA

Esta funcionalidade utiliza inteligência artificial para analisar código Python e identificar possíveis bugs, problemas de segurança, performance e qualidade.

## 📋 Funcionalidades

A análise de bugs com IA identifica:

- **🔒 Problemas de Segurança**: Vulnerabilidades, injeção de código, senhas hardcoded
- **⚡ Problemas de Performance**: Algoritmos ineficientes, loops desnecessários
- **🎯 Problemas de Qualidade**: Código duplicado, variáveis não utilizadas
- **🔧 Problemas de Manutenibilidade**: Código difícil de entender, falta de documentação

## 🚀 Como Usar

### Pré-requisitos

1. **Chave de API da OpenAI**: Você precisa de uma chave de API válida da OpenAI
2. **Configuração da chave**:
   - Configure a variável de ambiente: `OPENAI_API_KEY=sua_chave_aqui`
   - Ou passe via parâmetro: `--api-key sua_chave_aqui`
   - Ou use o arquivo `.env` (recomendado)

### Configuração Automática (Recomendado)

Execute o script de configuração:

```bash
python setup_env.py
```

Este script irá:
1. Guiar você para obter a chave da OpenAI
2. Criar o arquivo `.env` automaticamente
3. Testar se a configuração está funcionando

### Configuração Manual

#### Opção 1: Arquivo .env (Recomendado)
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

#### Opção 2: Variável de Ambiente
**Windows:**
```sh
set OPENAI_API_KEY=sua_chave_aqui
```
**Linux/Mac:**
```sh
export OPENAI_API_KEY=sua_chave_aqui
```

### Comandos Disponíveis

#### Análise Completa
```bash
python -m analyzer.main bugs-ai arquivo.py
```

#### Análise Simplificada
```bash
python -m analyzer.main bugs-ai-simple arquivo.py
```

#### Com Opções
```bash
# Especificar linguagem
python -m analyzer.main bugs-ai arquivo.py --language python

# Usar chave de API diretamente
python -m analyzer.main bugs-ai arquivo.py --api-key sua_chave_aqui

# Modo simplificado
python -m analyzer.main bugs-ai arquivo.py --simple
```

## 📊 Exemplo de Saída

```
🤖 Analisando código com IA...
📁 Arquivo: examples/buggy_code.py
🔤 Linguagem: python

============================================================
🔍 ANÁLISE DE BUGS COM IA
============================================================

📊 RESUMO:
   Total de problemas: 8
   🔴 Críticos: 2
   🟠 Altos: 3
   🟡 Médios: 2
   🟢 Baixos: 1

🚨 PROBLEMAS IDENTIFICADOS:

🔴 CRITICAL:
   1. 🔒 Uso de exec() com input do usuário (linha 35)
      💡 Sugestão: Nunca use exec() com entrada do usuário. Use ast.literal_eval() ou validação rigorosa
   2. 🔒 Senha hardcoded no código (linha 55)
      💡 Sugestão: Use variáveis de ambiente ou arquivo de configuração seguro

🟠 HIGH:
   1. ⚡ Loop ineficiente com append() (linha 12)
      💡 Sugestão: Use list comprehension ou range() diretamente
   2. 🔒 Input sem validação (linha 8)
      💡 Sugestão: Valide e sanitize todas as entradas do usuário
   3. 🎯 Código duplicado entre funções (linhas 37-47)
      💡 Sugestão: Extraia código comum para uma função reutilizável
```

## 🔧 Configuração

### Configuração Automática
```bash
python setup_env.py
```

### Configuração Manual

#### Arquivo .env (Recomendado)
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

#### Variável de Ambiente
```bash
# Windows
set OPENAI_API_KEY=sua_chave_aqui

# Linux/Mac
export OPENAI_API_KEY=sua_chave_aqui
```

## 🧪 Testes

Execute os testes específicos da funcionalidade:
```bash
python -m pytest tests/test_bugs_ai.py -v
```

## 📝 Exemplo de Código com Problemas

O arquivo `examples/buggy_code.py` contém exemplos de problemas que a IA pode identificar:

- Input sem validação
- Uso de `exec()` com entrada do usuário
- Senhas hardcoded
- Código duplicado
- Loops ineficientes
- Variáveis não utilizadas
- Exceções muito genéricas

## ⚠️ Limitações

1. **Custo**: Cada análise consome tokens da API da OpenAI
2. **Dependência de Internet**: Requer conexão com a API
3. **Falsos Positivos**: A IA pode identificar problemas que não são realmente problemas
4. **Contexto Limitado**: A análise é baseada apenas no código fornecido

## 🔍 Dicas de Uso

1. **Use em conjunto**: Combine com outras análises estáticas
2. **Revise resultados**: Sempre revise as sugestões da IA
3. **Teste em pequenos trechos**: Para códigos grandes, analise por partes
4. **Configure adequadamente**: Use a chave de API corretamente

## 🛠️ Personalização

Você pode personalizar o prompt de análise editando o método `_create_prompt()` na classe `BugPredictorAI` em `analyzer/analyze_bugs_ai.py`.

## 📞 Suporte

Para problemas ou dúvidas sobre esta funcionalidade:
1. Execute `python setup_env.py` para configurar automaticamente
2. Verifique se a chave de API está configurada corretamente
3. Teste com um arquivo simples primeiro
4. Consulte os logs de erro para mais detalhes 