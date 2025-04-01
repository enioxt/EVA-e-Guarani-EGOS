#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRONOS - Cursor Commands Interface
Interface de comandos para interação com o sistema CRONOS no Cursor IDE
"""

import sys
import json
from pathlib import Path
from . import cronos_capture
from . import cronos_restore
from . import context_monitor

def save_cronos():
    """Salva contexto atual"""
    save_path = cronos_capture.save_context()
    if save_path:
        print(f"Contexto salvo com sucesso em: {save_path}")
        return True
    return False

def load_cronos(path=None):
    """Carrega contexto salvo"""
    context = cronos_restore.load_context(path)
    if context and cronos_restore.verify_context(context):
        print("Contexto carregado com sucesso")
        return True
    return False

def list_saves():
    """Lista todos os contextos salvos"""
    saves = cronos_capture.get_save_list()
    if not saves:
        print("Nenhum contexto salvo encontrado")
        return False
    
    print(f"\nEncontrados {len(saves)} contextos salvos:")
    for save in saves:
        print(f"- {save['timestamp']}: {save['path']}")
    return True

def show_status():
    """Mostra status atual do monitor"""
    status = context_monitor.get_monitor_status()
    print("\nStatus do Monitor CRONOS:")
    print(f"- Rodando: {status['running']}")
    print(f"- Tamanho Atual: {status['current_size']} caracteres")
    print(f"- Capacidade Usada: {status['capacity_used']}")
    print(f"- Limite de Contexto: {status['context_limit']} caracteres ({status['source']})")
    print(f"- Última Verificação: {status['last_check']}")
    print(f"- Último Save: {status['last_save']}")
    return True

def update_limit(size=None):
    """Atualiza limite de contexto baseado no tamanho atual"""
    if size is None:
        # Em uma implementação real, obteríamos isso do Cursor
        size = 100000  # Tamanho exemplo
    
    success = context_monitor.save_context_limits(size)
    if success:
        print(f"Limite de contexto atualizado para {size} caracteres")
        return True
    return False

def main():
    """Manipulador principal de comandos"""
    if len(sys.argv) < 2:
        print("Uso: cursor_commands.py <comando> [args...]")
        return 1
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "save_cronos": save_cronos,
        "load_cronos": lambda: load_cronos(args[0] if args else None),
        "list_saves": list_saves,
        "show_status": show_status,
        "update_limit": lambda: update_limit(int(args[0]) if args else None)
    }
    
    if command not in commands:
        print(f"Comando desconhecido: {command}")
        return 1
    
    success = commands[command]()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 