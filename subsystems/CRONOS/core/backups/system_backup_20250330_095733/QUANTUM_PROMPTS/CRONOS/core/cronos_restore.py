#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRONOS - Context Restore Module
Responsável por carregar contextos salvos do Cursor IDE
"""

import json
from pathlib import Path
from . import cronos_capture

def load_context(save_path=None):
    """Carrega contexto de um arquivo de save"""
    try:
        # Se nenhum caminho fornecido, tenta obter o save mais recente
        if save_path is None:
            save_path = cronos_capture.get_latest_save()
            if save_path is None:
                print("Nenhum arquivo de save encontrado")
                return None
        
        # Converte para objeto Path
        save_path = Path(save_path)
        
        # Verifica se arquivo existe
        if not save_path.exists():
            print(f"Arquivo de save não encontrado: {save_path}")
            return None
        
        # Carrega contexto
        with open(save_path, 'r', encoding='utf-8') as f:
            context = json.load(f)
            
        print(f"Contexto carregado de: {save_path}")
        return context
    except Exception as e:
        print(f"Erro ao carregar contexto: {e}")
        return None

def verify_context(context):
    """Verifica se um contexto tem a estrutura necessária"""
    try:
        required_fields = ["timestamp", "messages", "metadata"]
        return all(field in context for field in required_fields)
    except Exception:
        return False

if __name__ == "__main__":
    # Tenta carregar o contexto mais recente
    context = load_context()
    if context and verify_context(context):
        print("\nEstrutura do contexto:")
        print(f"- Timestamp: {context['timestamp']}")
        print(f"- Mensagens: {len(context['messages'])}")
        print(f"- Metadata: {context['metadata']}") 