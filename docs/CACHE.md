# Sistema de Cache para Análise de Bugs com IA

## Visão Geral

O sistema de cache foi implementado para reduzir o número de requisições à API da OpenAI, economizando custos e evitando limites de rate limiting.

## Como Funciona

### Cache Automático
- **Armazenamento**: Resultados são salvos em arquivos `.pkl` no diretório `.cache/`
- **Chave**: Baseada no hash SHA-256 do código + linguagem
- **Expiração**: 24 horas (automaticamente removido após expirar)
- **Ativação**: Automática em todas as análises

### Benefícios
1. **Economia de Custos**: Evita requisições desnecessárias
2. **Performance**: Respostas instantâneas para códigos já analisados
3. **Rate Limiting**: Reduz o risco de atingir limites da API
4. **Desenvolvimento**: Facilita testes repetitivos

## Comandos Disponíveis

### Análise com Cache (Padrão)
```bash
python -m analyzer.main bugs-ai examples/sample.py
```

### Forçar Nova Análise (Ignorar Cache)
```bash
python -m analyzer.main bugs-ai examples/sample.py --no-cache
```

### Limpar Cache
```bash
python -m analyzer.main clear-cache
```

## Estrutura do Cache

```
.cache/
├── bugs_ai_[hash1].pkl
├── bugs_ai_[hash2].pkl
└── ...
```

### Formato dos Arquivos
- **Extensão**: `.pkl` (Python pickle)
- **Conteúdo**: Resultado completo da análise da IA
- **Tamanho**: Variável (depende do tamanho da resposta)

## Configuração

### Diretório de Cache
O cache é armazenado no diretório `.cache/` na raiz do projeto.

### Expiração
- **Padrão**: 24 horas
- **Modificação**: Edite o valor em `analyzer/analyze_bugs_ai.py` linha 47

### Limpeza Automática
Arquivos expirados são automaticamente removidos na próxima verificação.

## Casos de Uso

### Desenvolvimento
```bash
# Primeira análise (faz requisição)
python -m analyzer.main bugs-ai examples/sample.py

# Segunda análise (usa cache)
python -m analyzer.main bugs-ai examples/sample.py
```

### Testes
```bash
# Limpar cache antes dos testes
python -m analyzer.main clear-cache

# Executar testes
python -m analyzer.main bugs-ai examples/sample.py
```

### Produção
```bash
# Forçar nova análise em produção
python -m analyzer.main bugs-ai examples/sample.py --no-cache
```

## Troubleshooting

### Cache Corrompido
```bash
# Limpar cache
python -m analyzer.main clear-cache
```

### Problemas de Permissão
```bash
# Verificar permissões do diretório .cache
ls -la .cache/
```

### Cache Não Funcionando
1. Verifique se o diretório `.cache/` existe
2. Verifique permissões de escrita
3. Execute `clear-cache` e tente novamente

## Limitações

1. **Espaço em Disco**: Cache pode crescer com muitas análises
2. **Compatibilidade**: Arquivos `.pkl` são específicos do Python
3. **Segurança**: Cache contém dados da API (não sensíveis)

## Manutenção

### Limpeza Regular
```bash
# Limpar cache manualmente
python -m analyzer.main clear-cache
```

### Monitoramento
```bash
# Verificar tamanho do cache
du -sh .cache/
```

### Backup
O diretório `.cache/` está no `.gitignore` e não deve ser versionado. 