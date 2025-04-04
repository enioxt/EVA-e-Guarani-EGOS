#!/usr/bin/env python3
"""
EVA & GUARANI - BIOS-Q Cursor Integration
Sistema simplificado de preservação de contexto para o Cursor
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# Configuração de diretórios
CURSOR_APPDATA = Path(os.getenv("APPDATA")) / "Cursor"
CURSOR_HISTORY = CURSOR_APPDATA / "User" / "History"
PROJECT_ROOT = Path("C:/Eva & Guarani - EGOS")
CHATS_DIR = PROJECT_ROOT / "CHATS"
CURSOR_CONTEXT_DIR = CHATS_DIR / "cursor_context"


class BIOSQCursor:
    """Sistema simplificado de integração BIOS-Q com Cursor"""

    def __init__(self):
        self.signature = "QUANTUM_TEST_SIGNATURE_2024_03_24_BIOS_Q_CONTEXT_ANALYSIS_EGOS_V7_5"
        CURSOR_CONTEXT_DIR.mkdir(exist_ok=True)

    def save_context(self):
        """Salva o contexto atual do Cursor"""
        try:
            # Encontra o diretório mais recente do Cursor
            history_dirs = [d for d in CURSOR_HISTORY.iterdir() if d.is_dir()]
            if not history_dirs:
                print("⚠️ Nenhum histórico encontrado")
                return False

            latest_dir = max(history_dirs, key=lambda x: x.stat().st_mtime)

            # Cria arquivo de contexto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            context_file = CHATS_DIR / f"bios_q_context_{timestamp}.json"

            # Captura informações essenciais
            context_data = {
                "timestamp": datetime.now().isoformat(),
                "project": "EVA & GUARANI - EGOS",
                "environment": "Cursor + Claude 3.7 Sonnet",
                "signature": self.signature,
                "cursor_history_dir": str(latest_dir),
                "cursor_files": [
                    str(f)
                    for f in latest_dir.glob("*")
                    if f.is_file() and f.stat().st_mtime > datetime.now().timestamp() - 3600
                ],
            }

            # Salva o contexto
            with open(context_file, "w", encoding="utf-8") as f:
                json.dump(context_data, f, indent=2)

            # Copia os arquivos do Cursor para nosso diretório de backup
            backup_dir = CURSOR_CONTEXT_DIR / timestamp
            backup_dir.mkdir(exist_ok=True)

            for file_path in context_data["cursor_files"]:
                src = Path(file_path)
                if src.exists():
                    dst = backup_dir / src.name
                    shutil.copy2(src, dst)

            print(f"✅ Contexto BIOS-Q salvo em: {context_file}")
            return True

        except Exception as e:
            print(f"⚠️ Erro ao salvar contexto: {e}")
            return False

    def load_context(self):
        """Carrega o último contexto salvo"""
        try:
            # Encontra o arquivo de contexto mais recente
            context_files = list(CHATS_DIR.glob("bios_q_context_*.json"))
            if not context_files:
                print("⚠️ Nenhum contexto encontrado")
                return False

            latest_context = max(context_files, key=lambda x: x.stat().st_mtime)

            # Carrega o contexto
            with open(latest_context, "r", encoding="utf-8") as f:
                context = json.load(f)

            # Cria um novo diretório no histórico do Cursor
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_history_dir = CURSOR_HISTORY / timestamp
            new_history_dir.mkdir(exist_ok=True)

            # Restaura os arquivos do backup
            backup_dir = CURSOR_CONTEXT_DIR / context["timestamp"].split("T")[0]
            if backup_dir.exists():
                for file_path in backup_dir.glob("*"):
                    if file_path.is_file():
                        dst = new_history_dir / file_path.name
                        shutil.copy2(file_path, dst)

            # Cria um arquivo de marcação para o Cursor
            marker_file = new_history_dir / "cursor_context_loaded"
            marker_file.touch()

            print(f"✅ Contexto BIOS-Q carregado de: {latest_context}")
            print(f"✅ Arquivos restaurados em: {new_history_dir}")
            return context

        except Exception as e:
            print(f"⚠️ Erro ao carregar contexto: {e}")
            return False


if __name__ == "__main__":
    import sys

    bios_q = BIOSQCursor()

    if len(sys.argv) < 2:
        print("Uso: python bios_q_cursor.py [save|load]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "save":
        bios_q.save_context()
    elif command == "load":
        bios_q.load_context()
    else:
        print(f"Comando inválido: {command}")
        sys.exit(1)
