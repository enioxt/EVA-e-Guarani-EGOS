#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from context_manager import ContextManager
from cursor_integration import CursorIntegration

def init_context():
    """Inicializa o sistema de contexto"""
    manager = ContextManager()
    integration = CursorIntegration()
    
    # Atualizar estado
    integration.update_cursor_state()
    
    # Criar backup se necessário
    if manager.should_create_backup():
        manager.create_backup()
        
    # Limpar backups antigos
    manager.cleanup_old_backups()

if __name__ == "__main__":
    init_context()
