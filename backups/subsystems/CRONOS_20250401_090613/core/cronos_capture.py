#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRONOS - Context Capture Module
Responsável por salvar o contexto atual do Cursor IDE
"""

import os
import json
import datetime
from pathlib import Path

# Caminhos
SAVE_DIR = Path(__file__).parent.parent / "saves"
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def generate_save_name():
    """Gera um nome único para o arquivo de save"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"context_{timestamp}.json"


def save_context(context_data=None):
    """Salva o contexto atual em um arquivo"""
    try:
        # Se nenhum dado de contexto fornecido, cria estrutura mínima
        if context_data is None:
            context_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "messages": [],
                "metadata": {"source": "cursor", "version": "1.0"},
            }

        # Gera caminho do arquivo de save
        save_path = SAVE_DIR / generate_save_name()

        # Salva contexto
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(context_data, f, indent=2)

        print(f"Contexto salvo em: {save_path}")
        return str(save_path)
    except Exception as e:
        print(f"Erro ao salvar contexto: {e}")
        return None


def get_latest_save():
    """Obtém o caminho do arquivo de save mais recente"""
    try:
        saves = list(SAVE_DIR.glob("context_*.json"))
        if not saves:
            return None
        return str(max(saves, key=os.path.getctime))
    except Exception as e:
        print(f"Erro ao obter save mais recente: {e}")
        return None


def get_save_list():
    """Obtém lista de todos os arquivos de save"""
    try:
        saves = list(SAVE_DIR.glob("context_*.json"))
        return [
            {
                "path": str(save),
                "timestamp": datetime.datetime.fromtimestamp(save.stat().st_ctime).isoformat(),
            }
            for save in saves
        ]
    except Exception as e:
        print(f"Erro ao listar saves: {e}")
        return []


if __name__ == "__main__":
    # Teste de save
    test_context = {
        "timestamp": datetime.datetime.now().isoformat(),
        "messages": ["Mensagem de teste"],
        "metadata": {"test": True},
    }

    save_path = save_context(test_context)
    if save_path:
        print(f"Save de teste bem sucedido: {save_path}")

    # Lista saves
    saves = get_save_list()
    print(f"\nEncontrados {len(saves)} arquivos de save:")
