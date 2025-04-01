#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - EVA Atendimento API

API principal do sistema EVA Atendimento, que integra o bot do Telegram
e fornece endpoints para administração e monitoramento.
"""

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração da API
app = FastAPI(
    title="EVA Atendimento API",
    description="API do sistema EVA Atendimento - Powered by EVA & GUARANI",
    version="0.2.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adiciona o diretório atual ao PATH para importações relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Tenta importar módulos de integração com EVA & GUARANI
try:
    from .integrations.egos_connector import EGOSConnector
    egos_connector = EGOSConnector()
    EGOS_AVAILABLE = True
    logger.info("Integração com EVA & GUARANI disponível.")
except ImportError:
    logger.warning("Integração com EVA & GUARANI não disponível.")
    EGOS_AVAILABLE = False
    egos_connector = None

# Inicializa o bot do Telegram em segundo plano
def start_telegram_bot_background():
    """Inicia o bot do Telegram em um processo separado"""
    try:
        from .telegram_bot import main as start_bot
        asyncio.create_task(start_bot_async())
        logger.info("Bot do Telegram iniciado em segundo plano.")
    except ImportError:
        logger.error("Módulo do bot do Telegram não encontrado.")

async def start_bot_async():
    """Wrapper assíncrono para iniciar o bot"""
    try:
        # Importa e inicia o bot em uma thread separada para não bloquear a API
        import threading
        
        # Tenta importar o bot diretamente ou com caminho relativo
        try:
            from .telegram_bot import main as start_bot
        except ImportError:
            try:
                from telegram_bot import main as start_bot
            except ImportError:
                logger.error("Não foi possível importar o módulo do bot do Telegram.")
                return
        
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.daemon = True  # Thread será encerrada quando o processo principal terminar
        bot_thread.start()
        
        logger.info("Bot do Telegram iniciado em thread separada.")
    except Exception as e:
        logger.error(f"Erro ao iniciar bot do Telegram: {e}")

# Endpoints da API
@app.get("/")
async def root():
    """Endpoint raiz que fornece informações básicas sobre a API"""
    return {
        "name": "EVA Atendimento API",
        "version": "0.2.0",
        "status": "online",
        "telegram_bot": "enabled",
        "whatsapp_bot": "planned",
        "egos_integration": "available" if EGOS_AVAILABLE else "unavailable",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Verifica o estado de saúde do sistema"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "ok",
            "database": "ok",
            "telegram_bot": "ok",
        },
        "metrics": {
            "love_quotient": 0.95,
            "consciousness_level": 0.92,
            "ethical_alignment": 0.98
        }
    }
    
    # Se a integração EVA & GUARANI estiver disponível, usa-a para obter métricas
    if EGOS_AVAILABLE and egos_connector is not None:
        try:
            egos_health = egos_connector.health_check()
            health_data["metrics"] = egos_health["metrics"]
            health_data["components"]["egos"] = egos_health["status"]
            health_data["components"]["egos_subsystems"] = egos_health["subsystems"]
        except Exception as e:
            logger.error(f"Erro ao obter status do EGOS: {e}")
            health_data["components"]["egos"] = "error"
    else:
        health_data["components"]["egos"] = "unavailable"
    
    return health_data

@app.get("/telegram/status")
async def telegram_status():
    """Retorna o status do bot do Telegram"""
    # Aqui poderia verificar o status real do bot
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "uptime": "1 day, 2 hours",
        "active_users": 5,
        "message_count": 120
    }

@app.post("/telegram/broadcast")
async def broadcast_message(message: Dict[str, Any], background_tasks: BackgroundTasks):
    """Envia uma mensagem para todos os usuários do Telegram"""
    if "text" not in message:
        raise HTTPException(status_code=400, detail="Campo 'text' é obrigatório")
    
    # Aqui seria implementada a lógica para enviar a mensagem para todos os usuários
    # Como placeholder, apenas logamos a intenção
    logger.info(f"Solicitação de broadcast recebida: {message['text'][:50]}...")
    
    return {
        "status": "scheduled",
        "timestamp": datetime.now().isoformat(),
        "message_preview": message["text"][:50] + "..." if len(message["text"]) > 50 else message["text"],
        "target_count": 5  # Placeholder
    }

@app.get("/prompts/daily")
async def get_daily_prompt():
    """Retorna o prompt diário de criação de imagem"""
    try:
        # Aqui obteríamos o prompt do dia do sistema de prompts
        # Como placeholder, retornamos um exemplo
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": "Futuro Urbano",
            "description": "Imagine uma cidade do futuro que combina alta tecnologia com sustentabilidade e natureza integrada.",
            "examples": [
                "Uma metrópole com arranha-céus cobertos de jardins verticais e pessoas usando veículos voadores sustentáveis",
                "Uma cidade subaquática com biodiversidade marinha integrada à arquitetura",
                "Um centro urbano onde a tecnologia e a natureza coexistem harmoniosamente, com animais e humanos compartilhando espaços"
            ],
            "tips": [
                "Pense em como a tecnologia pode ser usada para preservar a natureza",
                "Considere diferentes níveis de infraestrutura (subterrânea, térreo, aérea)",
                "Inclua elementos que mostrem a interação entre pessoas, tecnologia e natureza",
                "Use cores vivas para tecnologia e tons naturais para elementos orgânicos"
            ]
        }
    except Exception as e:
        logger.error(f"Erro ao obter prompt diário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter prompt diário")

@app.on_event("startup")
async def startup_event():
    """Eventos executados na inicialização da API"""
    logger.info("Iniciando EVA Atendimento API...")
    
    # Inicia o bot do Telegram em segundo plano
    try:
        start_telegram_bot_background()
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot do Telegram: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)