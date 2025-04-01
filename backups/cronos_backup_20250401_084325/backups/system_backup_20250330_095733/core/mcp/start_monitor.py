#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inicia o monitor de contexto.
"""

from context_monitor import start_monitoring, get_status
import time

print("Iniciando monitor de contexto...")
start_monitoring()
time.sleep(1)

status = get_status()
print(f"\nMonitor iniciado com sucesso!")
print(f"- Limite atual: {status['context_limit']} caracteres")
print(f"- Fonte do limite: {status['context_source']}")
print(f"- Monitoramento ativo: {status['running']}")
print("\nO monitor agora está rodando em segundo plano.") 