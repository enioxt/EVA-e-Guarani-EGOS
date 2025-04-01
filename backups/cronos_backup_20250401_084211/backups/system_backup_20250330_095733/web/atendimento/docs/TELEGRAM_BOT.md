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

# Documentação do Bot Telegram EVA & GUARANI

## Visão Geral

O Bot do Telegram EVA & GUARANI é uma interface para interagir com o sistema EVA & GUARANI através da plataforma Telegram. Ele fornece acesso a múltiplas personas especializadas, geração de imagens e outras funcionalidades criativas.

## Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Pacotes Python listados em `backend/requirements.txt`
- Token de acesso ao Bot do Telegram (obtido através do @BotFather)

### Configuração do Ambiente

1. Clone o repositório do EVA & GUARANI
2. Navegue até o diretório `eva-atendimento/backend`
3. Copie o arquivo `.env.example` para `.env`
4. Edite o arquivo `.env` e adicione seu token do Telegram e outras configurações

```bash
# No diretório backend
cp .env.example .env
# Edite o arquivo .env com seu editor de texto preferido
```

### Estrutura de Diretórios

```
eva-atendimento/
├── backend/
│   ├── app/
│   │   ├── integrations/
│   │   │   ├── __init__.py
│   │   │   ├── egos_connector.py
│   │   │   └── stable_diffusion.py
│   │   ├── telegram_bot.py
│   │   └── main.py
│   ├── data/
│   │   └── telegram_bot/
│   │       ├── personas/
│   │       │   ├── default.json
│   │       │   ├── ethik.json
│   │       │   └── atlas.json
│   │       ├── prompts/
│   │       │   └── daily_2025_03_24.json
│   │       └── users/
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   ├── start_bot.bat
│   └── start_telegram_bot.py
├── run_bot_background.ps1
└── README.md
```

## Iniciando o Bot

### Usando o arquivo BAT (Windows)

```bash
cd backend
start_bot.bat
```

### Usando PowerShell (Windows)

```powershell
.\run_bot_background.ps1
```

### Usando Python diretamente

```bash
cd backend
python start_telegram_bot.py
```

## Funcionalidades

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| /start | Inicia ou reinicia o bot, mostrando o menu principal |
| /help | Mostra a mensagem de ajuda com todos os comandos disponíveis |
| /chat | Inicia uma conversa com o bot usando a persona selecionada |
| /image | Inicia o modo de criação de imagens |
| /video | Inicia o modo de criação de vídeos (em desenvolvimento) |
| /daily | Mostra o prompt do dia para criação de imagens |
| /persona | Permite escolher uma persona para conversar |

### Sistema de Personas

O bot possui diferentes personas que oferecem experiências especializadas:

- **Assistente EVA & GUARANI** (default): Assistente geral com capacidades equilibradas
- **ETHIK**: Especialista em ética aplicada e reflexões filosóficas
- **ATLAS**: Especialista em mapeamento sistêmico e visualização de conhecimento

Para adicionar novas personas, crie arquivos JSON no diretório `backend/data/telegram_bot/personas/` seguindo o formato dos exemplos existentes.

### Geração de Imagens

A funcionalidade de geração de imagens permite criar imagens a partir de descrições textuais. Esta função requer:

1. Uma API de geração de imagens configurada (como Stable Diffusion)
2. Configurações adequadas no arquivo `.env`:

   ```
   STABLE_DIFFUSION_API_URL=sua_url_api
   STABLE_DIFFUSION_API_KEY=sua_chave_api
   ```

### Prompts Diários

O sistema inclui prompts diários para inspirar a criatividade na geração de imagens. Os prompts são armazenados como arquivos JSON em `backend/data/telegram_bot/prompts/` no formato `daily_YYYY_MM_DD.json`.

## Customização

### Adicionando Novas Personas

Para adicionar uma nova persona:

1. Crie um arquivo JSON em `backend/data/telegram_bot/personas/`
2. Siga o formato:

   ```json
   {
     "name": "Nome da Persona",
     "description": "Descrição da persona",
     "system_prompt": "Instrução detalhada sobre o comportamento da persona",
     "greeting": "Mensagem de saudação",
     "examples": [
       {"user": "Exemplo de pergunta", "assistant": "Exemplo de resposta"}
     ]
   }
   ```

### Prompts Diários Personalizados

Para adicionar prompts diários personalizados:

1. Crie um arquivo JSON em `backend/data/telegram_bot/prompts/` com o nome `daily_YYYY_MM_DD.json`
2. Siga o formato:

   ```json
   {
     "date": "YYYY-MM-DD",
     "title": "Título do Prompt",
     "description": "Descrição detalhada do tema do dia",
     "examples": ["Exemplo 1", "Exemplo 2"],
     "tips": ["Dica 1", "Dica 2"]
   }
   ```

## Solução de Problemas

### Logs e Depuração

Os logs do bot são salvos em `backend/telegram_bot.log`. Verifique este arquivo para informações detalhadas sobre erros e o funcionamento do bot.

### Problemas Comuns

1. **Bot não inicia**: Verifique se o token do Telegram está correto no arquivo `.env`
2. **Erro de importação de módulos**: Verifique se todas as dependências foram instaladas com `pip install -r requirements.txt`
3. **Geração de imagens não funciona**: Verifique as configurações da API de Stable Diffusion no arquivo `.env`

## Desenvolvimento

### Estrutura do Código

- `telegram_bot.py`: Contém a lógica principal do bot
- `integrations/stable_diffusion.py`: Integração com API de geração de imagens
- `integrations/egos_connector.py`: Conexão com outros módulos do sistema EVA & GUARANI

### Adicionando Novas Funcionalidades

Para adicionar novas funcionalidades ao bot:

1. Implemente a lógica em `telegram_bot.py`
2. Adicione novos comandos no ConversationHandler principal
3. Atualize a documentação e os comandos de ajuda

## Considerações de Segurança

- Nunca compartilhe seu token do Telegram publicamente
- Implemente limites de taxa para evitar abusos
- Proteja os dados dos usuários conforme regulamentações de privacidade

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

*Última atualização: 24 de Março de 2025*
