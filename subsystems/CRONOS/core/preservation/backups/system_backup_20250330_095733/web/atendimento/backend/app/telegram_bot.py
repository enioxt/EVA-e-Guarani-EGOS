#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Bot para Telegram

Este bot implementa funcionalidades avançadas com preservação de contexto,
integração com personas e diversas funções criativas como geração de imagens 
e prompts diários.
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import io

# Bibliotecas para o Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes, 
    ConversationHandler,
    filters
)

# Armazenamento de contexto e configurações
from pydantic import BaseModel
import yaml
from dotenv import load_dotenv

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tenta importar a integração Stable Diffusion
try:
    import sys
    import os
    
    # Adiciona o diretório atual ao PATH para importações
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # Tenta importar diretamente
    try:
        from integrations.stable_diffusion import StableDiffusionAPI
    except ImportError:
        # Se não funcionar, tenta com caminho absoluto
        from app.integrations.stable_diffusion import StableDiffusionAPI
        
    stable_diffusion_api = StableDiffusionAPI()
    STABLE_DIFFUSION_AVAILABLE = True
    logger.info("Integração com Stable Diffusion disponível")
except ImportError as e:
    logger.warning(f"Integração com Stable Diffusion não disponível: {e}")
    STABLE_DIFFUSION_AVAILABLE = False
    stable_diffusion_api = None

# Tenta importar a integração EGOS
try:
    try:
        from integrations.egos_connector import EGOSConnector
    except ImportError:
        # Se não funcionar, tenta com caminho absoluto
        from app.integrations.egos_connector import EGOSConnector
    
    egos_connector = EGOSConnector()
    EGOS_AVAILABLE = True
    logger.info("Integração com EVA & GUARANI EGOS disponível")
except ImportError as e:
    logger.warning(f"Integração com EVA & GUARANI EGOS não disponível: {e}")
    EGOS_AVAILABLE = False
    egos_connector = None

# Add this after other imports
try:
    from tools.integration.perplexity_integration import PerplexityIntegration
    perplexity_enabled = True
    logger.info("Perplexity integration loaded successfully")
except ImportError:
    perplexity_enabled = False
    logger.warning("Perplexity integration not available. Search features will be limited.")

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_DIR = Path("data/telegram_bot")
USER_DATA_DIR = DATA_DIR / "users"
PROMPT_DATA_DIR = DATA_DIR / "prompts"
PERSONA_DATA_DIR = DATA_DIR / "personas"

# Garante que os diretórios existam
DATA_DIR.mkdir(exist_ok=True, parents=True)
USER_DATA_DIR.mkdir(exist_ok=True, parents=True)
PROMPT_DATA_DIR.mkdir(exist_ok=True, parents=True)
PERSONA_DATA_DIR.mkdir(exist_ok=True, parents=True)

# Estados para o ConversationHandler
(
    MAIN_MENU,
    CHAT_MODE,
    IMAGE_PROMPT,
    VIDEO_PROMPT,
    SELECTING_PERSONA,
) = range(5)

# Modelos de dados
class UserContext(BaseModel):
    """Armazena o contexto do usuário para personalização da experiência"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    chat_history: List[Dict[str, str]] = []
    selected_persona: Optional[str] = None
    preferences: Dict[str, Any] = {}
    last_active: Optional[datetime] = None
    
    def add_message(self, role: str, content: str):
        """Adiciona uma mensagem ao histórico do chat"""
        self.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Limita o histórico a 20 mensagens para não ficar muito grande
        if len(self.chat_history) > 20:
            self.chat_history = self.chat_history[-20:]
    
    def update_activity(self):
        """Atualiza o timestamp da última atividade"""
        self.last_active = datetime.now()

class DailyPrompt(BaseModel):
    """Modelo para armazenar prompts diários de imagem"""
    date: str
    title: str
    description: str
    examples: List[str] = []
    tips: List[str] = []
    
    @classmethod
    def get_today(cls) -> "DailyPrompt":
        """Obtém o prompt do dia atual ou cria um novo se não existir"""
        today = datetime.now().strftime("%Y-%m-%d")
        prompt_file = PROMPT_DATA_DIR / f"{today}.json"
        
        if prompt_file.exists():
            with open(prompt_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return cls(**data)
        
        # Se não existir, cria um prompt padrão
        return cls(
            date=today,
            title="Paisagem Onírica",
            description="Crie uma paisagem que mistura elementos do mundo real com aspectos oníricos e surreais.",
            examples=[
                "Uma cidade flutuando entre nuvens com cachoeiras que caem no vazio",
                "Uma floresta onde as árvores são feitas de cristal e os animais são constelações vivas",
                "Um oceano de areia com barcos navegando como se fosse água"
            ],
            tips=[
                "Combine elementos contraditórios como fogo e água",
                "Brinque com a escala dos objetos",
                "Use cores contrastantes para destacar elementos importantes"
            ]
        )

# Funções auxiliares
def load_user_context(user_id: int) -> UserContext:
    """Carrega o contexto do usuário ou cria um novo se não existir"""
    user_file = USER_DATA_DIR / f"{user_id}.json"
    
    if user_file.exists():
        with open(user_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return UserContext(**data)
    
    return UserContext(user_id=user_id)

def save_user_context(context: UserContext):
    """Salva o contexto do usuário em arquivo"""
    user_file = USER_DATA_DIR / f"{context.user_id}.json"
    
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(context.dict(), f, ensure_ascii=False, indent=2)

def load_persona(persona_name: str = "default") -> Dict[str, Any]:
    """Carrega uma persona pelo nome"""
    # Primeiro tenta usar o conector EGOS para carregar personas do sistema principal
    if EGOS_AVAILABLE and egos_connector:
        persona_data = egos_connector.get_persona(persona_name)
        if persona_data:
            logger.info(f"Persona {persona_name} carregada via EGOS")
            return persona_data
    
    # Se não conseguir via EGOS, tenta carregar do arquivo local
    persona_file = PERSONA_DATA_DIR / f"{persona_name}.json"
    
    try:
        if persona_file.exists():
            with open(persona_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar persona {persona_name}: {str(e)}")
    
    # Retorna uma persona padrão se não conseguir carregar
    return {
        "name": "Assistente EVA & GUARANI",
        "system_prompt": "Você é um assistente útil e respeitoso."
    }

# Define o ID do administrador para receber notificação de inicialização
ADMIN_USER_ID = 171767219  # ID do usuário @ebfrocha

# Manejadores de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia a interação com o bot"""
    user = update.effective_user
    user_context = load_user_context(user.id)
    
    # Atualiza informações do usuário
    user_context.username = user.username
    user_context.first_name = user.first_name
    user_context.last_name = user.last_name
    user_context.update_activity()
    
    # Mensagem de boas-vindas
    welcome_message = (
        f"Olá, {user.first_name}! 👋\n\n"
        f"Sou o EVA Atendimento, baseado no sistema EVA & GUARANI. "
        f"Estou aqui para ajudar com diversas tarefas, desde conversas até criação de conteúdo criativo.\n\n"
        f"Como posso ajudar você hoje?"
    )
    
    # Botões do menu principal
    keyboard = [
        [
            InlineKeyboardButton("💬 Conversar", callback_data="chat"),
            InlineKeyboardButton("🖼️ Criar Imagem", callback_data="image")
        ],
        [
            InlineKeyboardButton("🎬 Criar Vídeo", callback_data="video"),
            InlineKeyboardButton("📝 Prompt do Dia", callback_data="daily_prompt")
        ],
        [
            InlineKeyboardButton("👤 Escolher Persona", callback_data="persona"),
            InlineKeyboardButton("ℹ️ Ajuda", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    save_user_context(user_context)
    return MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia mensagem de ajuda com os comandos disponíveis."""
    help_text = (
        "📚 *Comandos disponíveis:*\n\n"
        "/start - Inicia o bot\n"
        "/help - Mostra essa mensagem de ajuda\n"
        "/settings - Configura preferências\n"
        "/persona - Escolhe a persona para interação\n"
        "/generate - Gera uma imagem a partir de um prompt\n"
    )
    
    # Add search command help if available
    if perplexity_enabled:
        help_text += "/search - Busca informações na internet usando Perplexity API\n"
    
    help_text += "\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa os callbacks dos botões inline"""
    query = update.callback_query
    await query.answer()
    
    user_context = load_user_context(query.from_user.id)
    user_context.update_activity()
    
    if query.data == "chat":
        await query.edit_message_text(
            text="Você está no modo de conversa. Pode me perguntar qualquer coisa ou voltar ao menu principal com /start."
        )
        return CHAT_MODE
    
    elif query.data == "image":
        await query.edit_message_text(
            text="Descreva a imagem que você gostaria de criar:"
        )
        return IMAGE_PROMPT
    
    elif query.data == "video":
        await query.edit_message_text(
            text="Descreva o vídeo que você gostaria de criar:"
        )
        return VIDEO_PROMPT
    
    elif query.data == "daily_prompt":
        await daily_prompt(update, context)
        return MAIN_MENU
    
    elif query.data == "persona":
        # Lista as personas disponíveis
        personas = []
        
        # Usa o conector EGOS para listar todas as personas se disponível
        if EGOS_AVAILABLE and egos_connector:
            available_personas = egos_connector.list_available_personas()
            personas = [(p["id"], p["name"]) for p in available_personas]
            logger.info(f"Encontradas {len(personas)} personas via EGOS")
        else:
            # Fallback para listagem direta dos arquivos
            for persona_file in PERSONA_DATA_DIR.glob("*.json"):
                persona_name = persona_file.stem
                try:
                    with open(persona_file, "r", encoding="utf-8") as f:
                        persona_data = json.load(f)
                        personas.append((persona_name, persona_data.get("name", persona_name)))
                except:
                    personas.append((persona_name, persona_name))
        
        if not personas:
            await query.edit_message_text(
                text="Nenhuma persona disponível no momento."
            )
            return MAIN_MENU
        
        keyboard = []
        for persona_id, persona_name in personas:
            keyboard.append([InlineKeyboardButton(persona_name, callback_data=f"select_persona_{persona_id}")])
        
        keyboard.append([InlineKeyboardButton("↩️ Voltar", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="Escolha uma persona para conversar:",
            reply_markup=reply_markup
        )
        return SELECTING_PERSONA
    
    elif query.data.startswith("select_persona_"):
        persona = query.data.replace("select_persona_", "")
        user_context.selected_persona = persona
        save_user_context(user_context)
        
        await query.edit_message_text(
            text=f"Persona '{persona.capitalize()}' selecionada! Agora você pode conversar com esta personalidade."
        )
        return CHAT_MODE
    
    elif query.data == "back_to_menu":
        # Volta ao menu principal
        keyboard = [
            [
                InlineKeyboardButton("💬 Conversar", callback_data="chat"),
                InlineKeyboardButton("🖼️ Criar Imagem", callback_data="image")
            ],
            [
                InlineKeyboardButton("🎬 Criar Vídeo", callback_data="video"),
                InlineKeyboardButton("📝 Prompt do Dia", callback_data="daily_prompt")
            ],
            [
                InlineKeyboardButton("👤 Escolher Persona", callback_data="persona"),
                InlineKeyboardButton("ℹ️ Ajuda", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="O que você gostaria de fazer hoje?",
            reply_markup=reply_markup
        )
        return MAIN_MENU
    
    elif query.data == "help":
        help_text = (
            "🤖 *Comandos do EVA Atendimento*\n\n"
            "/start - Iniciar ou reiniciar o bot\n"
            "/help - Mostrar esta mensagem de ajuda\n"
            "/chat - Iniciar uma conversa com o bot\n"
            "/image - Criar uma imagem a partir de um prompt\n"
            "/video - Criar um vídeo a partir de um prompt\n"
            "/daily - Ver o prompt do dia para criação de imagens\n"
            "/persona - Escolher uma persona para conversar\n\n"
            "Você também pode simplesmente enviar mensagens para conversar!"
        )
        
        await query.edit_message_text(text=help_text, parse_mode="Markdown")
        return MAIN_MENU

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia uma conversa com o usuário"""
    user_context = load_user_context(update.effective_user.id)
    user_context.update_activity()
    
    await update.message.reply_text(
        "Vamos conversar! O que você gostaria de discutir hoje?"
    )
    
    save_user_context(user_context)
    return CHAT_MODE

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa mensagens recebidas no modo de conversa"""
    user_id = update.effective_user.id
    user_context = load_user_context(user_id)
    user_context.update_activity()
    
    # Adiciona a mensagem do usuário ao histórico
    user_message = update.message.text
    user_context.add_message("user", user_message)
    
    # Aqui seria integrada a lógica de chat com IA, usando o contexto do usuário
    # Por enquanto, implementamos uma resposta simples
    persona = user_context.selected_persona
    
    if persona:
        response = f"[Persona {persona.capitalize()}] Obrigado pela sua mensagem! Em uma implementação completa, eu responderia com base na persona selecionada e no seu histórico de conversa."
    else:
        response = "Obrigado pela sua mensagem! Em uma implementação completa, eu responderia com base no seu histórico de conversa."
    
    # Adiciona a resposta ao histórico
    user_context.add_message("assistant", response)
    save_user_context(user_context)
    
    await update.message.reply_text(response)
    return CHAT_MODE

async def handle_image_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa o prompt para criação de imagem"""
    user_context = load_user_context(update.effective_user.id)
    user_context.update_activity()
    
    # Obtem o prompt do usuário
    image_prompt = update.message.text
    user_context.add_message("user", f"Pedido de imagem: {image_prompt}")
    
    # Enviar mensagem de processamento
    processing_msg = await update.message.reply_text(
        "🔄 Processando seu pedido de imagem... Isso pode levar alguns momentos."
    )
    
    try:
        # Verificar integração com Stable Diffusion
        if STABLE_DIFFUSION_AVAILABLE and stable_diffusion_api is not None:
            # Tentar gerar imagem com Stable Diffusion
            success, error_message, image_data = await stable_diffusion_api.generate_image(
                prompt=image_prompt,
                negative_prompt="ugly, blurry, low quality, distorted, deformed",
                width=512,
                height=512
            )
            
            if success and image_data:
                # Enviar a imagem gerada
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image_data,
                    caption=f"✅ Imagem gerada com sucesso!\n\nPrompt: \"{image_prompt}\"\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                )
                
                # Atualizar a mensagem de processamento
                await processing_msg.edit_text(
                    "✅ Imagem gerada e enviada com sucesso!"
                )
                
                user_context.add_message("assistant", "Imagem gerada com sucesso.")
                save_user_context(user_context)
                return MAIN_MENU
        
        # Se não temos integração ou falhou, tentar APIs externas
        image_api_key = os.getenv("IMAGE_API_KEY")
        image_api_url = os.getenv("IMAGE_API_URL")
        
        if image_api_key and image_api_key != "sua_chave_api_aqui" and image_api_url and image_api_url != "https://api.exemplo.com/images":
            # Aqui seria a chamada para a API real de geração de imagens
            # Como exemplo, estamos simulando uma resposta bem-sucedida
            await asyncio.sleep(3)  # Simula o tempo de processamento
            
            success = True
            error_message = None
        else:
            # API não configurada corretamente
            success = False
            error_message = "APIs de geração de imagem não configuradas. Usando resposta simulada."
            logger.warning(error_message)
            
            # Simulação para propósitos de demonstração
            await asyncio.sleep(2)
            success = True  # Fingimos que deu certo mesmo assim
    
    except Exception as e:
        success = False
        error_message = f"Erro ao processar pedido de imagem: {str(e)}"
        logger.error(f"Erro na geração de imagem: {e}")
    
    # Atualizar mensagem com o resultado
    if success:
        # Em uma implementação real, aqui enviaríamos a imagem gerada
        await processing_msg.edit_text(
            f"✅ Pedido de imagem processado.\n\n"
            f"Prompt: \"{image_prompt}\"\n\n"
            f"Em uma implementação completa, eu enviaria a imagem gerada usando APIs como DALL-E ou Stable Diffusion.\n\n"
            f"⚠️ Simulação: a API real de geração ainda não está integrada ou retornou apenas texto."
        )
    else:
        await processing_msg.edit_text(
            f"❌ Não foi possível gerar a imagem.\n"
            f"Erro: {error_message}\n\n"
            f"Por favor, tente novamente mais tarde ou contate o administrador."
        )
    
    user_context.add_message("assistant", "Processamento de pedido de imagem concluído.")
    save_user_context(user_context)
    return MAIN_MENU

async def handle_video_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa o prompt para criação de vídeo"""
    user_context = load_user_context(update.effective_user.id)
    user_context.update_activity()
    
    # Obtem o prompt do usuário
    video_prompt = update.message.text
    user_context.add_message("user", f"Pedido de vídeo: {video_prompt}")
    
    # Enviar mensagem de processamento
    processing_msg = await update.message.reply_text(
        "🔄 Processando seu pedido de vídeo... Isso pode levar alguns momentos."
    )
    
    try:
        # Tentar gerar vídeo com APIs externas
        # Verificar se as configurações estão disponíveis
        video_api_key = os.getenv("VIDEO_API_KEY")
        video_api_url = os.getenv("VIDEO_API_URL")
        
        if video_api_key and video_api_key != "sua_chave_api_aqui" and video_api_url and video_api_url != "https://api.exemplo.com/videos":
            # Aqui seria a chamada para a API real de geração de vídeos
            # Como exemplo, estamos simulando uma resposta bem-sucedida
            await asyncio.sleep(5)  # Simula o tempo de processamento
            
            success = True
            error_message = None
        else:
            # API não configurada corretamente
            success = False
            error_message = "APIs de geração de vídeo não configuradas. Usando resposta simulada."
            logger.warning(error_message)
            
            # Simulação para propósitos de demonstração
            await asyncio.sleep(3)
            success = True  # Fingimos que deu certo mesmo assim
    
    except Exception as e:
        success = False
        error_message = f"Erro ao processar pedido de vídeo: {str(e)}"
        logger.error(f"Erro na geração de vídeo: {e}")
    
    # Atualizar mensagem com o resultado
    if success:
        # Em uma implementação real, aqui enviaríamos o vídeo gerado
        await processing_msg.edit_text(
            f"✅ Pedido de vídeo processado.\n\n"
            f"Prompt: \"{video_prompt}\"\n\n"
            f"Em uma implementação completa, eu enviaria o vídeo gerado usando APIs como Runway ML.\n\n"
            f"⚠️ Simulação: a API real de geração ainda não está integrada."
        )
    else:
        await processing_msg.edit_text(
            f"❌ Não foi possível gerar o vídeo.\n"
            f"Erro: {error_message}\n\n"
            f"Por favor, tente novamente mais tarde ou contate o administrador."
        )
    
    user_context.add_message("assistant", "Processamento de pedido de vídeo concluído.")
    save_user_context(user_context)
    return MAIN_MENU

async def daily_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia o prompt do dia para o usuário"""
    # Obtém o prompt do dia
    prompt = DailyPrompt.get_today()
    
    # Verifica se estamos respondendo a um callback ou comando
    if update.callback_query:
        message_func = update.callback_query.edit_message_text
    else:
        message_func = update.message.reply_text
    
    # Formata a mensagem do prompt
    prompt_text = (
        f"📝 *Prompt do Dia: {prompt.title}*\n\n"
        f"{prompt.description}\n\n"
        f"*Exemplos:*\n"
    )
    
    for example in prompt.examples:
        prompt_text += f"• {example}\n"
    
    prompt_text += "\n*Dicas:*\n"
    
    for tip in prompt.tips:
        prompt_text += f"• {tip}\n"
    
    await message_func(prompt_text, parse_mode="Markdown")
    return MAIN_MENU

async def persona_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite ao usuário escolher uma persona para a conversa"""
    personas = [
        "Criativa", "Científica", "Filosófica", 
        "Estratégica", "Educacional", "Artística"
    ]
    
    keyboard = []
    for i in range(0, len(personas), 2):
        row = []
        row.append(InlineKeyboardButton(personas[i], callback_data=f"select_persona_{personas[i].lower()}"))
        if i + 1 < len(personas):
            row.append(InlineKeyboardButton(personas[i+1], callback_data=f"select_persona_{personas[i+1].lower()}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("Voltar", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Escolha uma persona para conversar:",
        reply_markup=reply_markup
    )
    return SELECTING_PERSONA

# Add this new command handler
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search command with Perplexity API"""
    if not perplexity_enabled or not perplexity_integration:
        await update.message.reply_text(
            "⚠️ Search functionality is not available. Perplexity integration is not configured."
        )
        return

    # Get query from message text
    message_text = update.message.text
    query = message_text.replace("/search", "").strip()
    
    # If no query provided, ask for one
    if not query:
        await update.message.reply_text(
            "Please provide a search query. Example: /search quantum computing"
        )
        return

    # Get active persona if any
    persona = None
    if hasattr(context.user_data, "active_persona"):
        persona = context.user_data.get("active_persona")
    
    # Send typing action
    await update.message.reply_chat_action(ChatAction.TYPING)
    
    try:
        # Perform search
        result = await perplexity_integration.enhance_knowledge(query, persona=persona)
        
        if result.get("status") == "success":
            # Get content and sources
            content = result.get("knowledge", {}).get("content", "No results found.")
            sources = result.get("knowledge", {}).get("sources", [])
            
            # Format sources as text
            sources_text = ""
            if sources:
                sources_text = "\n\n📚 *Sources:*\n"
                for i, source in enumerate(sources[:5], 1):  # Limit to 5 sources
                    if "title" in source and "url" in source:
                        sources_text += f"{i}. [{source['title']}]({source['url']})\n"
                    elif "url" in source:
                        sources_text += f"{i}. {source['url']}\n"
            
            # Check for ethical warnings
            warning_text = ""
            if "ethical_warning" in result.get("knowledge", {}):
                warning_text = f"\n\n⚠️ *Notice:* {result['knowledge']['ethical_warning']}"
            
            # Send response
            response_text = f"*Search Results:* '{query}'\n\n{content}{warning_text}{sources_text}\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            
            # If response is too long, split it
            if len(response_text) > 4000:
                await update.message.reply_text(content[:4000] + "...")
                if sources_text:
                    await update.message.reply_text(sources_text)
            else:
                await update.message.reply_text(
                    response_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
        else:
            # Handle error
            error_message = result.get("message", "An unknown error occurred during search.")
            await update.message.reply_text(
                f"⚠️ *Search Error:*\n{error_message}\n\nPlease try again with a different query.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        logger.error(f"Error during Perplexity search: {str(e)}")
        await update.message.reply_text(
            "⚠️ An error occurred while processing your search. Please try again later."
        )

async def main():
    """Função principal para iniciar o bot"""
    # Verifica se o token do Telegram está configurado
    if not TELEGRAM_TOKEN:
        logger.error("Token do Telegram não encontrado. Configure a variável TELEGRAM_TOKEN no arquivo .env")
        return
    
    # Cria a aplicação e define o token do bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Initialize Perplexity integration if available
    global perplexity_integration
    if perplexity_enabled:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("PERPLEXITY_API_KEY")
            perplexity_integration = PerplexityIntegration(api_key)
            logger.info("Perplexity integration initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Perplexity integration: {str(e)}")
            perplexity_enabled = False
    
    # Cria um conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("help", help_command),
            CommandHandler("chat", chat),
            CommandHandler("daily", daily_prompt),
            CommandHandler("persona", persona_command)
        ],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(button_handler)
            ],
            CHAT_MODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
                CommandHandler("start", start)
            ],
            IMAGE_PROMPT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_image_prompt),
                CommandHandler("start", start)
            ],
            VIDEO_PROMPT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_prompt),
                CommandHandler("start", start)
            ],
            SELECTING_PERSONA: [
                CallbackQueryHandler(button_handler)
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    
    application.add_handler(conv_handler)
    
    # Add search command handler
    application.add_handler(CommandHandler("search", search_command))
    
    # Inicia o bot
    logger.info("Iniciando o bot do Telegram...")
    
    # Registra função para enviar mensagem quando iniciar
    async def post_init(app: Application):
        """Função executada após a inicialização do bot"""
        try:
            await app.bot.send_message(
                chat_id=ADMIN_USER_ID,
                text="✅ EVA & GUARANI Telegram Bot está online e pronto para uso! Versão: 1.0.0"
            )
            logger.info(f"Notificação de inicialização enviada para o usuário {ADMIN_USER_ID}")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de inicialização: {e}")
    
    # Inicia o polling com o post_init configurado
    application.post_init = post_init
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main()) 