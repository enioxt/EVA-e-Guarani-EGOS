#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define manualmente o limite de contexto para testes.
"""

import os
import json
import sys
from context_monitor import register_limit_reached, get_status

# Verifica argumentos
if len(sys.argv) < 2:
    print("Uso: python set_limit.py <tamanho_do_limite>")
    sys.exit(1)

try:
    # Obtém o limite do argumento
    limit = int(sys.argv[1])
    
    # Registra o limite
    print(f"Registrando limite de {limit} caracteres...")
    result = register_limit_reached(limit)
    
    print("\nLimite atualizado:")
    print(f"- Limite anterior: {result['old_limit']} caracteres")
    print(f"- Novo limite: {result['new_limit']} caracteres")
    print(f"- Capacidade atual: {result['new_capacity']*100:.1f}%")
    
    # Verifica o status atual
    print("\nStatus atual do monitor:")
    status = get_status()
    print(f"- Limite: {status['context_limit']} caracteres")
    print(f"- Fonte: {status['context_source']}")
    print(f"- Capacidade: {status['capacity_used']*100:.1f}%")
    
    print("\nInformações salvas no BIOS-Q para uso futuro.")
    
except ValueError:
    print(f"Erro: '{sys.argv[1]}' não é um número válido.")
    sys.exit(1)
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1) 