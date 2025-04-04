#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from context_manager import ContextManager


class CursorIntegration:
    def __init__(self):
        self.manager = ContextManager()
        self.cursor_context_dir = self.manager.chats_path / "cursor_context"

    def setup_cursor_context(self):
        """Configura o contexto do Cursor IDE"""
        # Criar arquivo de configuração do Cursor
        cursor_config = {
            "version": "7.5",
            "context_manager": {
                "enabled": True,
                "auto_backup": True,
                "max_backups": 5,
                "backup_interval": 3600,  # 1 hora
            },
            "paths": {
                "chats": str(self.manager.chats_path),
                "quantum": str(self.manager.quantum_path),
                "core": str(self.manager.core_path),
                "tools": str(self.manager.tools_path),
            },
        }

        config_file = self.cursor_context_dir / "cursor_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(cursor_config, f, indent=2)

        # Criar arquivo de estado do Cursor
        cursor_state = {
            "last_context": None,
            "last_backup": None,
            "active_files": [],
            "workspace_state": self.manager.get_current_state(),
        }

        state_file = self.cursor_context_dir / "cursor_state.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(cursor_state, f, indent=2)

    def update_cursor_state(self):
        """Atualiza o estado do Cursor IDE"""
        state_file = self.cursor_context_dir / "cursor_state.json"
        if not state_file.exists():
            self.setup_cursor_context()

        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)

        # Atualizar estado
        state["workspace_state"] = self.manager.get_current_state()
        state["last_context"] = self.manager.create_context()
        state["last_backup"] = self.manager.create_backup()

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def restore_cursor_state(self):
        """Restaura o estado do Cursor IDE"""
        state_file = self.cursor_context_dir / "cursor_state.json"
        if not state_file.exists():
            print("Nenhum estado anterior encontrado")
            return False

        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)

        if state["last_backup"]:
            return self.manager.restore_context(state["last_backup"])
        return False

    def cleanup_cursor_context(self):
        """Limpa o contexto do Cursor IDE"""
        self.manager.cleanup_old_backups()


def main():
    """Função principal para testar a integração"""
    integration = CursorIntegration()

    # Configurar contexto
    integration.setup_cursor_context()
    print("Contexto do Cursor configurado")

    # Atualizar estado
    integration.update_cursor_state()
    print("Estado do Cursor atualizado")

    # Limpar contexto antigo
    integration.cleanup_cursor_context()
    print("Contexto antigo limpo")

    # Mostrar histórico
    history = integration.manager.get_context_history()
    print("\nHistórico de contextos:")
    for entry in history:
        print(f"- {entry['timestamp']}: {entry['type']}")


if __name__ == "__main__":
    main()
