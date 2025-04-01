#!/usr/bin/env python
"""
Script para iniciar o bot do Telegram do EVA Atendimento.
"""

import os
import sys
import logging
import traceback
import asyncio
from pathlib import Path

# Obter o diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Configuração de logging
log_path = os.path.join(current_dir, "telegram_bot.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Adiciona os diretórios ao PATH para importações
sys.path.append(current_dir)
# Adiciona o diretório do projeto ao PATH para permitir imports relativos
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
app_dir = os.path.join(current_dir, "app")
sys.path.append(app_dir)

logger.info(f"Diretório atual: {current_dir}")
logger.info(f"Diretório do projeto: {project_dir}")
logger.info(f"Diretório da app: {app_dir}")
logger.info(f"Python Path: {sys.path}")

# Verifica o ambiente
env_path = os.path.join(current_dir, ".env")
env_example_path = os.path.join(current_dir, ".env.example")

if not os.path.exists(env_path):
    logger.warning(f"Arquivo .env não encontrado em {env_path}. Tentando copiar de .env.example...")
    if os.path.exists(env_example_path):
        import shutil
        shutil.copy(env_example_path, env_path)
        logger.info(f"Arquivo .env criado a partir de .env.example em {env_path}")
    else:
        logger.error(f"Arquivo .env.example não encontrado em {env_example_path}. Crie um arquivo .env manualmente.")
        sys.exit(1)

# Verifica se o diretório de dados existe
data_dir = os.path.join(current_dir, "data", "telegram_bot")
data_dir = Path(data_dir)
if not data_dir.exists():
    logger.info(f"Criando diretório de dados em {data_dir}...")
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "users").mkdir(exist_ok=True)
    (data_dir / "prompts").mkdir(exist_ok=True)
    logger.info("Diretórios de dados criados.")

# Importa e executa o bot
try:
    logger.info("Tentando importar o módulo telegram_bot...")
    
    # Tenta várias abordagens de importação
    try:
        from app.telegram_bot import main
        logger.info("Importado via 'from app.telegram_bot import main'")
    except ImportError:
        try:
            from telegram_bot import main
            logger.info("Importado via 'from telegram_bot import main'")
        except ImportError:
            # Tenta importar usando importlib
            import importlib.util
            
            # Verifica se o arquivo existe primeiro
            telegram_bot_path = os.path.join(app_dir, "telegram_bot.py")
            if os.path.exists(telegram_bot_path):
                logger.info(f"Arquivo telegram_bot.py encontrado em {telegram_bot_path}")
                spec = importlib.util.spec_from_file_location("telegram_bot", telegram_bot_path)
                if spec is not None:
                    telegram_bot = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(telegram_bot)
                    main = telegram_bot.main
                    logger.info("Importado via importlib")
                else:
                    raise ImportError("Não foi possível carregar o spec do módulo")
            else:
                logger.error(f"Arquivo telegram_bot.py não encontrado em {telegram_bot_path}")
                raise ImportError(f"Arquivo não encontrado: {telegram_bot_path}")
    
    logger.info("Iniciando o bot do Telegram...")
    # Executa a função assíncrona corretamente
    asyncio.run(main())
except ImportError as e:
    logger.error(f"Erro ao importar módulo do bot: {e}")
    logger.error("Verifique se o arquivo app/telegram_bot.py existe.")
    
    # Lista os arquivos no diretório app para diagnóstico
    app_dir_path = os.path.join(current_dir, "app")
    if os.path.exists(app_dir_path):
        logger.info(f"Conteúdo do diretório {app_dir_path}:")
        for item in os.listdir(app_dir_path):
            logger.info(f"  - {item}")
    else:
        logger.error(f"Diretório {app_dir_path} não existe.")
    
    logger.error("Verifique se as dependências estão instaladas. Execute: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    logger.error(f"Erro ao iniciar o bot: {e}")
    logger.error(f"Exception detalhada: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1) 