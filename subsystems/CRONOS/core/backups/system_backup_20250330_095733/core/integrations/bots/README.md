---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: integrations
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: MASTER
  test_coverage: 0.9
  translation_status: completed
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

# EVA & GUARANI - Telegram Bot (avatechartbot)

## Visão Geral

Este é o bot Telegram para o sistema EVA & GUARANI, fornecendo uma interface amigável para interagir com o sistema através do Telegram. O bot suporta geração de imagens, processamento de pagamentos e acesso à base de conhecimento.

## Funcionalidades

- **Geração de Imagens**: Gerar imagens usando APIs do Stable Diffusion, Unsplash ou Pexels
- **Sistema de Pagamento**: Aceitar pagamentos via PIX e criptomoedas
- **Sistema de Créditos**: Gerenciar créditos de usuário e níveis freemium
- **Acesso ao Conhecimento**: Acessar o sistema de conhecimento quântico
- **Respostas de IA**: Interagir com a IA EVA & GUARANI via mensagens de texto

## Estrutura Otimizada

A estrutura do bot foi otimizada e unificada. Os principais arquivos são:

- `simple_telegram_bot.py` - Implementação principal do bot
- `simple_bot.py` - Versão simplificada compatível com Python 3.13+
- `check_bot.py` - Ferramenta unificada para verificar a saúde e status do bot
- `open_telegram_web.py` - Utilitário para abrir o Telegram Web
- `telegram_config.json` - Configuração principal do bot
- `start_bot.bat` - Script para iniciar o bot no Windows

## Instruções de Instalação e Uso

### 1. Requisitos

- Python 3.9 ou superior (recomendado até Python 3.11 para total compatibilidade)
- Pacotes Python necessários:

  ```
  python-telegram-bot==13.15
  requests
  openai (opcional para respostas de IA)
  ```

### 2. Configuração

1. Configurar o arquivo `telegram_config.json` com seu token do bot
   - Obtenha um token do @BotFather no Telegram
   - Configure os IDs de usuários permitidos e administradores

2. Verificar a configuração e saúde do bot:

   ```
   python check_bot.py
   ```

3. (Opcional) Configure as chaves de API para geração de imagens:
   - [Stable Diffusion API](https://stablediffusionapi.com/): Crie uma conta e obtenha a chave API
   - [Unsplash API](https://unsplash.com/developers): Registre-se como desenvolvedor e obtenha a chave API
   - [Pexels API](https://www.pexels.com/api/): Registre-se como desenvolvedor e obtenha a chave API

### 3. Execução do Bot

Para Windows, use o script batch:

```
start_bot.bat
```

Ou execute diretamente:

```
python simple_telegram_bot.py
```

Para Python 3.13+, use a versão simplificada:

```
python simple_bot.py
```

Alternativamente, abra o Telegram Web para interagir com o bot:

```
python open_telegram_web.py
```

## Comandos do Bot

- `/start` - Iniciar o bot e ver introdução
- `/help` - Mostrar mensagem de ajuda com comandos disponíveis
- `/status` - Verificar status do bot e tempo de atividade
- `/credits` - Verificar seus créditos e uso
- `/payment` - Adicionar créditos via pagamento
- `/image` - Gerar uma imagem (será solicitado um prompt)

## Solução de Problemas

Se você encontrar problemas:

1. Execute o verificador de saúde para diagnóstico:

   ```
   python check_bot.py
   ```

2. Verifique os logs em `logs/telegram_bot.log`

3. Se estiver usando Python 3.13+, use a versão simplificada:

   ```
   python simple_bot.py
   ```

4. Para interação direta via navegador:

   ```
   python open_telegram_web.py
   ```

## Créditos

Criado por ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
