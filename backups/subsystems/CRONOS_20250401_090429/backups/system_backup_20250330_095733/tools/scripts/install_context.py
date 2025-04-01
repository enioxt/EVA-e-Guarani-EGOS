#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
from context_manager import ContextManager
from cursor_integration import CursorIntegration
import json

def install_context_system():
    """Instala o sistema de contexto"""
    print("Iniciando instalação do sistema de contexto...")
    
    # Criar gerenciador de contexto
    manager = ContextManager()
    print("✓ Gerenciador de contexto criado")
    
    # Criar integração com Cursor
    integration = CursorIntegration()
    print("✓ Integração com Cursor criada")
    
    # Configurar contexto do Cursor
    integration.setup_cursor_context()
    print("✓ Contexto do Cursor configurado")
    
    # Criar backup inicial
    backup_dir = manager.create_backup()
    print(f"✓ Backup inicial criado: {backup_dir}")
    
    # Criar arquivo de configuração
    config = {
        "version": "7.5",
        "installed": True,
        "paths": {
            "base": str(manager.base_path),
            "chats": str(manager.chats_path),
            "quantum": str(manager.quantum_path),
            "core": str(manager.core_path),
            "tools": str(manager.tools_path)
        },
        "settings": {
            "auto_backup": True,
            "max_backups": 5,
            "backup_interval": 3600,
            "context_types": ["bios_q", "cursor", "quantum"]
        }
    }
    
    config_file = manager.chats_path / "metadata" / "context_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print("✓ Arquivo de configuração criado")
    
    # Criar script de inicialização
    init_script = manager.tools_path / "scripts" / "init_context.py"
    with open(init_script, 'w', encoding='utf-8') as f:
        f.write('''import os
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
''')
    print("✓ Script de inicialização criado")
    
    # Criar arquivo README
    readme = manager.chats_path / "metadata" / "CONTEXT_SYSTEM.md"
    with open(readme, 'w', encoding='utf-8') as f:
        f.write('''# Sistema de Contexto EVA & GUARANI

## Visão Geral
Este sistema gerencia o contexto e estado do ambiente EVA & GUARANI, integrando com o Cursor IDE.

## Funcionalidades
- Gerenciamento de contexto
- Backup automático
- Integração com Cursor IDE
- Histórico de contextos
- Restauração de estado

## Estrutura
- `/CHATS`: Arquivos de chat e contexto
- `/QUANTUM_PROMPTS`: Prompts e configurações
- `/core`: Módulos principais
- `/tools`: Scripts e utilitários

## Uso
1. O sistema é inicializado automaticamente
2. Backups são criados a cada hora
3. Contextos antigos são limpos automaticamente
4. Estado pode ser restaurado se necessário

## Configuração
Edite `context_config.json` para ajustar:
- Intervalo de backup
- Número máximo de backups
- Tipos de contexto

## Manutenção
- Use `init_context.py` para reinicializar
- Verifique logs em `context_manager.log`
- Limpe backups antigos manualmente se necessário
''')
    print("✓ Documentação criada")
    
    print("\nInstalação concluída com sucesso!")
    print("\nPara usar o sistema:")
    print("1. O sistema é inicializado automaticamente")
    print("2. Backups são criados a cada hora")
    print("3. Contextos antigos são limpos automaticamente")
    print("4. Use o script de inicialização para reiniciar o sistema")

if __name__ == "__main__":
    install_context_system() 