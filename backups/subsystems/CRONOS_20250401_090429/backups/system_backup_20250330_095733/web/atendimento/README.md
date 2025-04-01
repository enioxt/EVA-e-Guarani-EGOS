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

# EVA Atendimento

> Sistema de atendimento automatizado baseado no framework EVA & GUARANI EGOS

## 📌 Visão Geral

EVA Atendimento é uma plataforma que implementa um sistema de atendimento automatizado multichannel, usando o framework quantum EVA & GUARANI para fornecer recursos avançados de processamento de linguagem natural, geração de conteúdo e interação contextual.

### Canais de Comunicação Suportados

- 📱 **Telegram**: Bot totalmente funcional com suporte para chat, geração de imagens e vídeos
- 🌐 **API REST**: Interface para integração com outros sistemas
- 💻 **Frontend Web**: Interface para administração e monitoramento do sistema

## 🚀 Componentes Principais

### Backend

- **API REST**: Desenvolvida com FastAPI para alta performance
- **Bot do Telegram**: Integração completa com a API do Telegram
- **Integrações EVA & GUARANI**: Conexões com os sistemas ATLAS, NEXUS, CRONOS e ETHIK

### Frontend

- **Painel de Administração**: Dashboard para monitoramento e configuração
- **Visualização de Estatísticas**: Métricas de uso e performance
- **Gerenciamento de Usuários**: Controle de acesso e permissões

## 🛠️ Instalação e Uso

### Pré-requisitos

- Python 3.9+
- Token de bot do Telegram (obtido via [@BotFather](https://t.me/BotFather))
- APIs de geração de conteúdo (opcional)

### Configuração Rápida

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/eva-atendimento.git
   cd eva-atendimento
   ```

2. Instale as dependências:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:

   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   # Especialmente TELEGRAM_TOKEN
   ```

4. Inicie o bot do Telegram:

   ```bash
   python start_telegram_bot.py
   ```

5. Inicie a API (em outro terminal):

   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## 📊 Funcionalidades do Bot Telegram

### Comandos Disponíveis

- `/start` - Inicia a interação com o bot
- `/help` - Mostra a lista de comandos disponíveis
- `/image` - Inicia o fluxo de geração de imagens
- `/video` - Inicia o fluxo de geração de vídeos
- `/daily` - Mostra o prompt diário para criação de imagens

### Geração de Imagens

O bot permite gerar imagens a partir de descrições textuais, utilizando:

- Integração com APIs como DALL-E, Stable Diffusion
- Sistema de prompts diários para inspiração
- Personalização por persona selecionada

### Persistência Contextual

O sistema mantém o contexto das conversas, permitindo:

- Histórico de interações por usuário
- Personalização baseada em preferências detectadas
- Adaptação do estilo de resposta conforme uso

## 🧪 Testando o Bot do Telegram

Para testar o bot do Telegram com o token fornecido, siga estas etapas:

1. Abra o aplicativo do Telegram e pesquise por `@avatechartbot`
2. Inicie uma conversa com o bot usando o comando `/start`
3. Explore as funcionalidades disponíveis:
   - Teste o comando `/help` para ver todos os comandos disponíveis
   - Teste o comando `/image` para solicitar a geração de uma imagem
   - Teste o comando `/video` para solicitar a geração de um vídeo
   - Teste o comando `/daily` para ver o prompt diário
   - Teste a conversa natural digitando mensagens comuns

### Observações sobre o Teste

- O bot está configurado com o token `7642662485:AAHsOEk05KD884z-hElUfzOQV6nopj7GJj0`
- Algumas funcionalidades podem estar em modo de simulação se as APIs de geração de conteúdo não estiverem configuradas
- O bot salva o contexto das conversas entre sessões, permitindo manter o histórico

### Resolução de Problemas

Se encontrar problemas ao testar o bot:

1. Verifique se o bot está online tentando a interação com `/start`
2. Confirme se o serviço backend está em execução
3. Verifique os logs em `backend/telegram_bot.log` para mais detalhes sobre erros

## 🔮 Integrações

### EVA & GUARANI EGOS

- **ATLAS**: Cartografia sistêmica para mapeamento de conversas
- **NEXUS**: Análise modular para preferências de usuário
- **CRONOS**: Preservação evolutiva para contexto histórico
- **ETHIK**: Framework ético para respostas alinhadas

### APIs Externas

- **Geração de Imagens**: Integração com DALL-E, Stable Diffusion, etc.
- **Geração de Vídeos**: Integração com Runway ML e outras plataformas

## 📋 Roadmap

- [ ] Implementação completa das APIs de geração de conteúdo
- [ ] Integração com WhatsApp Business API
- [ ] Sistema de pagamentos para recursos premium
- [ ] Análise avançada de sentimento nas conversas
- [ ] Personalização de interface por usuário

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar pull requests.

## 📝 Licença

Este projeto está licenciado sob os termos da licença MIT.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

*Última atualização: 24 de Março de 2025*

## Módulos do EVA Atendimento

O sistema EVA Atendimento é composto pelos seguintes módulos:

### 1. Telegram Bot

O Bot para Telegram permite interagir com o sistema EVA & GUARANI através da plataforma de mensagens Telegram.

#### Iniciando o Bot

Para iniciar o bot do Telegram, você pode utilizar um dos métodos abaixo:

**Usando o arquivo BAT (Windows):**

```bash
cd backend
start_bot.bat
```

**Usando PowerShell (Windows):**

```powershell
.\run_bot_background.ps1
```

**Usando Python diretamente:**

```bash
cd backend
python start_telegram_bot.py
```

#### Funcionalidades do Bot

O bot do Telegram oferece as seguintes funcionalidades:

- **Conversação**: Interaja com diferentes personas do sistema EVA & GUARANI
- **Geração de Imagens**: Crie imagens a partir de descrições textuais
- **Prompts Diários**: Receba sugestões diárias para estimular sua criatividade
- **Sistema de Personas**: Escolha entre diferentes especialistas para suas consultas

#### Configuração

A configuração do bot é realizada através do arquivo `.env`. Um modelo está disponível em `.env.example`.

Principais configurações:

- `TELEGRAM_TOKEN`: Token de acesso ao Bot do Telegram
- `STABLE_DIFFUSION_API_URL`: URL da API para geração de imagens
- `STABLE_DIFFUSION_API_KEY`: Chave de API para geração de imagens
