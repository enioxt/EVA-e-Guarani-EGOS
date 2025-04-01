#!/usr/bin/env python3
﻿import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class BIOSCursorIntegration:
    def __init__(self):
        self.config = self.load_config()
        self.cursor_paths = self.config['cursor_paths']
        self.bios_paths = self.config['bios_paths']
        self.integration = self.config['integration']
        
    def load_config(self):
        config_path = Path(__file__).parent / 'config' / 'bios_config.json'
        with open(config_path, 'r') as f:
            return json.load(f)
            
    def save_context(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        context_dir = Path(self.bios_paths['context'])
        backup_dir = context_dir / timestamp
        
        # Criar backup do contexto atual
        if self.integration['backup_enabled']:
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar arquivos do Cursor
            cursor_context = Path(self.cursor_paths['appdata']) / 'User' / 'workspaceStorage'
            if cursor_context.exists():
                shutil.copytree(cursor_context, backup_dir / 'workspaceStorage', dirs_exist_ok=True)
                
            # Copiar arquivos do BIOS
            if context_dir.exists():
                shutil.copytree(context_dir, backup_dir / 'bios_context', dirs_exist_ok=True)
                
        # Limpar backups antigos
        self.cleanup_old_backups()
        
    def load_context(self, timestamp=None):
        if timestamp is None:
            # Carregar o contexto mais recente
            context_dir = Path(self.bios_paths['context'])
            backups = sorted(context_dir.glob('*'), reverse=True)
            if not backups:
                return False
            timestamp = backups[0].name
            
        backup_dir = Path(self.bios_paths['context']) / timestamp
        if not backup_dir.exists():
            return False
            
        # Restaurar arquivos do Cursor
        cursor_context = Path(self.cursor_paths['appdata']) / 'User' / 'workspaceStorage'
        if (backup_dir / 'workspaceStorage').exists():
            shutil.rmtree(cursor_context, ignore_errors=True)
            shutil.copytree(backup_dir / 'workspaceStorage', cursor_context)
            
        # Restaurar arquivos do BIOS
        if (backup_dir / 'bios_context').exists():
            shutil.rmtree(Path(self.bios_paths['context']), ignore_errors=True)
            shutil.copytree(backup_dir / 'bios_context', Path(self.bios_paths['context']))
            
        return True
        
    def cleanup_old_backups(self):
        context_dir = Path(self.bios_paths['context'])
        backups = sorted(context_dir.glob('*'), reverse=True)
        if len(backups) > self.integration['max_backups']:
            for backup in backups[self.integration['max_backups']:]:
                shutil.rmtree(backup)

if __name__ == '__main__':
    bios = BIOSCursorIntegration()
    bios.save_context()
