---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: eva-atendimento
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

# Guia de Integração de APIs para EVA & GUARANI

Este documento contém instruções detalhadas sobre como obter e configurar as APIs necessárias para as integrações do sistema EVA & GUARANI, especialmente para o módulo EVA Atendimento.

## Índice

1. [Stable Diffusion](#stable-diffusion)
2. [OpenAI](#openai)
3. [Telegram Bot](#telegram-bot)
4. [Configuração no .env](#configuração-no-env)

## Stable Diffusion

A integração com Stable Diffusion pode ser feita de duas maneiras:

### Opção 1: API Local (AUTOMATIC1111)

1. **Instale o WebUI AUTOMATIC1111**:
   - Clone o repositório: `git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git`
   - Instale as dependências seguindo as instruções do README
   - Execute com a flag `--api`: `./webui.sh --api` (Linux/Mac) ou `webui-user.bat --api` (Windows)

2. **Configuração no EVA Atendimento**:
   - A API local é detectada automaticamente na URL `http://127.0.0.1:7860`
   - Não é necessária configuração adicional no `.env` para a API local

### Opção 2: Serviços de API Externos

#### Stability AI

1. Crie uma conta em [platform.stability.ai](https://platform.stability.ai/)
2. Vá para a seção "API Keys" no seu perfil
3. Crie uma nova chave de API
4. Obtenha informações de uso em [Stability AI API docs](https://platform.stability.ai/docs/api/generation)

#### Replicate

1. Crie uma conta em [replicate.com](https://replicate.com/)
2. Vá para a seção "API Tokens" nas configurações
3. Gere um novo token
4. Explore modelos disponíveis em [replicate.com/explore](https://replicate.com/explore)

## OpenAI

A integração com a OpenAI é usada para processamento de linguagem natural e suporte à geração de conteúdo.

1. **Crie uma conta OpenAI**:
   - Acesse [platform.openai.com](https://platform.openai.com/)
   - Clique em "Sign up" para criar uma conta

2. **Obtenha uma chave de API**:
   - Faça login em sua conta
   - Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Clique em "Create new secret key"
   - Dê um nome descritivo à sua chave
   - Copie a chave gerada (ela só será mostrada uma vez)

3. **Configure limites (opcional)**:
   - Acesse [platform.openai.com/account/limits](https://platform.openai.com/account/limits)
   - Defina limites de gastos para controlar custos

4. **Modelos recomendados**:
   - Para chat: `gpt-4` ou `gpt-3.5-turbo`
   - Para embeddings: `text-embedding-3-small` ou `text-embedding-3-large`

## Telegram Bot

Para criar um bot no Telegram e obter o token necessário:

1. **Abra o Telegram** e pesquise por `@BotFather`
2. **Inicie uma conversa** com o BotFather
3. **Envie o comando** `/newbot` para criar um novo bot
4. **Escolha um nome** para seu bot (ex: "EVA & GUARANI Assistant")
5. **Escolha um username** para seu bot (ex: "eva_guarani_bot") - deve terminar com "bot"
6. **Copie o token** fornecido pelo BotFather
7. Configure permissões adicionais com `/mybots` > [seu bot] > Bot Settings

## Configuração no .env

Após obter as chaves de API necessárias, configure-as no arquivo `.env` do projeto:

```bash
# Configurações do Telegram
TELEGRAM_TOKEN=seu_token_do_telegram_aqui

# Configurações da OpenAI
OPENAI_API_KEY=sua_chave_da_openai_aqui

# Configurações do Stable Diffusion (API externa)
IMAGE_API_KEY=sua_chave_api_aqui
IMAGE_API_URL=https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image
# OU
IMAGE_API_URL=https://api.replicate.com/v1/predictions
```

### Localização do arquivo .env

O arquivo `.env` deve estar localizado no diretório `eva-atendimento/backend/`.

### Verificando a configuração

Para verificar se suas APIs estão configuradas corretamente:

1. **Telegram Bot**: Inicie uma conversa com seu bot no Telegram
2. **Stable Diffusion**: Use o comando `/image` no bot do Telegram
3. **OpenAI**: Verifique os logs em `eva-atendimento/backend/telegram_bot.log`

## Alternativas Gratuitas

Se você não quiser usar APIs pagas, considere estas alternativas:

1. **Modelos locais**: Configure modelos de código aberto localmente
   - [Llama 3](https://github.com/meta-llama/llama3) para processamento de linguagem
   - [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) para geração de imagens

2. **APIs gratuitas com limites**:
   - [Hugging Face Inference API](https://huggingface.co/inference-api)
   - [Ollama](https://ollama.ai/) para execução de modelos locais

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
