#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Ferramenta de migração WhatsApp para Telegram

Este script auxilia na migração do EVA Atendimento do WhatsApp para o Telegram,
transferindo configurações, dados de usuário e adaptando o formato das mensagens.
"""

import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("migration.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Diretórios
WHATSAPP_DATA_DIR = Path("../data/whatsapp")
TELEGRAM_DATA_DIR = Path("../backend/data/telegram_bot")
BACKUP_DIR = Path("../backup/migration_" + datetime.now().strftime("%Y%m%d_%H%M%S"))


def setup_directories():
    """Configura os diretórios necessários para a migração"""
    # Cria diretório de backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Diretório de backup criado: {BACKUP_DIR}")

    # Cria diretórios do Telegram se não existirem
    TELEGRAM_DATA_DIR.mkdir(parents=True, exist_ok=True)
    (TELEGRAM_DATA_DIR / "users").mkdir(exist_ok=True)
    (TELEGRAM_DATA_DIR / "prompts").mkdir(exist_ok=True)
    logger.info(f"Diretórios do Telegram criados: {TELEGRAM_DATA_DIR}")


def backup_existing_data():
    """Faz backup dos dados existentes antes da migração"""
    if TELEGRAM_DATA_DIR.exists():
        logger.info("Fazendo backup dos dados existentes do Telegram...")
        for item in TELEGRAM_DATA_DIR.glob("**/*"):
            if item.is_file():
                # Cria a mesma estrutura de diretórios no backup
                relative_path = item.relative_to(TELEGRAM_DATA_DIR)
                backup_path = BACKUP_DIR / "telegram" / relative_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, backup_path)
        logger.info("Backup dos dados do Telegram concluído.")

    if WHATSAPP_DATA_DIR.exists():
        logger.info("Fazendo backup dos dados existentes do WhatsApp...")
        for item in WHATSAPP_DATA_DIR.glob("**/*"):
            if item.is_file():
                # Cria a mesma estrutura de diretórios no backup
                relative_path = item.relative_to(WHATSAPP_DATA_DIR)
                backup_path = BACKUP_DIR / "whatsapp" / relative_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, backup_path)
        logger.info("Backup dos dados do WhatsApp concluído.")


def map_whatsapp_to_telegram_user(whatsapp_id: str) -> Dict[str, Any]:
    """
    Cria um modelo de usuário do Telegram a partir de dados do WhatsApp.
    Obs: Como não há mapeamento direto, criamos um modelo vazio com o número como username.
    """
    # Remove o @ ou + do número se existir
    clean_id = whatsapp_id.replace("@c.us", "").replace("+", "")

    return {
        "user_id": int(clean_id) if clean_id.isdigit() else hash(clean_id),  # Hash como fallback
        "username": clean_id,
        "first_name": "Usuário",
        "last_name": "WhatsApp",
        "chat_history": [],
        "selected_persona": None,
        "preferences": {},
        "last_active": datetime.now().isoformat(),
    }


def convert_whatsapp_chat_to_telegram(chat_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Converte o formato de histórico de chat do WhatsApp para o formato do Telegram"""
    telegram_chat = []

    for message in chat_data:
        # Converte o formato da mensagem
        telegram_message = {
            "role": "assistant" if message.get("fromMe", True) else "user",
            "content": message.get("body", ""),
            "timestamp": message.get("timestamp", datetime.now().isoformat()),
        }

        # Adiciona apenas se tiver conteúdo
        if telegram_message["content"]:
            telegram_chat.append(telegram_message)

    return telegram_chat


def migrate_user_data():
    """Migra dados de usuário do WhatsApp para o Telegram"""
    if not WHATSAPP_DATA_DIR.exists():
        logger.warning(
            "Diretório de dados do WhatsApp não encontrado. Pulando migração de usuários."
        )
        return

    # Procura arquivos de usuário do WhatsApp
    user_files = list(WHATSAPP_DATA_DIR.glob("users/*.json"))

    if not user_files:
        logger.warning("Nenhum arquivo de usuário do WhatsApp encontrado.")
        return

    logger.info(f"Encontrados {len(user_files)} arquivos de usuário do WhatsApp.")

    # Processa cada arquivo de usuário
    for user_file in user_files:
        try:
            with open(user_file, "r", encoding="utf-8") as f:
                whatsapp_user_data = json.load(f)

            # Identificador do usuário (número de telefone)
            whatsapp_id = whatsapp_user_data.get(
                "id", os.path.basename(user_file).replace(".json", "")
            )

            # Cria o modelo de usuário do Telegram
            telegram_user = map_whatsapp_to_telegram_user(whatsapp_id)

            # Converte o histórico de chat
            chat_history = whatsapp_user_data.get("chatHistory", [])
            if chat_history:
                telegram_user["chat_history"] = convert_whatsapp_chat_to_telegram(chat_history)

            # Salva o arquivo de usuário do Telegram
            telegram_user_file = TELEGRAM_DATA_DIR / "users" / f"{telegram_user['user_id']}.json"
            with open(telegram_user_file, "w", encoding="utf-8") as f:
                json.dump(telegram_user, f, ensure_ascii=False, indent=2)

            logger.info(f"Usuário migrado: {whatsapp_id} -> {telegram_user['user_id']}")

        except Exception as e:
            logger.error(f"Erro ao migrar usuário {user_file}: {e}")

    logger.info("Migração de usuários concluída.")


def migrate_prompt_templates():
    """Migra templates de prompt do WhatsApp para o Telegram"""
    prompt_source_dir = WHATSAPP_DATA_DIR / "templates"

    if not prompt_source_dir.exists():
        logger.warning("Diretório de templates de prompt do WhatsApp não encontrado.")
        return

    # Procura arquivos de template
    template_files = list(prompt_source_dir.glob("*.json"))

    if not template_files:
        logger.warning("Nenhum template de prompt do WhatsApp encontrado.")
        return

    logger.info(f"Encontrados {len(template_files)} templates de prompt do WhatsApp.")

    # Processa cada template
    for template_file in template_files:
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                template_data = json.load(f)

            # Converte para o formato de prompt do Telegram
            prompt_data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": template_data.get("title", "Prompt sem título"),
                "description": template_data.get("description", ""),
                "examples": template_data.get("examples", []),
                "tips": template_data.get("tips", []),
            }

            # Salva o arquivo de prompt do Telegram
            prompt_file = TELEGRAM_DATA_DIR / "prompts" / template_file.name
            with open(prompt_file, "w", encoding="utf-8") as f:
                json.dump(prompt_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Template migrado: {template_file.name}")

        except Exception as e:
            logger.error(f"Erro ao migrar template {template_file}: {e}")

    logger.info("Migração de templates concluída.")


def migrate_config_files():
    """Migra arquivos de configuração do WhatsApp para o Telegram"""
    whatsapp_config = WHATSAPP_DATA_DIR / "config.json"
    telegram_config = TELEGRAM_DATA_DIR / "config.json"

    if not whatsapp_config.exists():
        logger.warning("Arquivo de configuração do WhatsApp não encontrado.")
        return

    try:
        with open(whatsapp_config, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        # Adapta a configuração para o formato do Telegram
        telegram_config_data = {
            "bot_name": config_data.get("botName", "EVA Atendimento"),
            "welcome_message": config_data.get("welcomeMessage", "Olá! Sou o assistente EVA."),
            "personas": {
                "criativa": config_data.get("creativePersona", {}),
                "científica": config_data.get("scientificPersona", {}),
                "filosófica": config_data.get("philosophicalPersona", {}),
                "estratégica": config_data.get("strategicPersona", {}),
                "educacional": config_data.get("educationalPersona", {}),
                "artística": config_data.get("artisticPersona", {}),
            },
            "migrated_from_whatsapp": True,
            "migration_date": datetime.now().isoformat(),
        }

        # Salva a nova configuração
        with open(telegram_config, "w", encoding="utf-8") as f:
            json.dump(telegram_config_data, f, ensure_ascii=False, indent=2)

        logger.info("Arquivo de configuração migrado com sucesso.")

    except Exception as e:
        logger.error(f"Erro ao migrar arquivo de configuração: {e}")


def main():
    """Função principal para executar a migração"""
    logger.info("Iniciando migração do WhatsApp para o Telegram...")

    try:
        # Configura diretórios
        setup_directories()

        # Backup dos dados existentes
        backup_existing_data()

        # Migração dos dados
        migrate_user_data()
        migrate_prompt_templates()
        migrate_config_files()

        logger.info("Migração concluída com sucesso!")
        logger.info(f"Backup dos dados originais disponível em: {BACKUP_DIR}")

    except Exception as e:
        logger.error(f"Erro durante a migração: {e}")
        logger.error("A migração foi interrompida devido a um erro.")


if __name__ == "__main__":
    main()
