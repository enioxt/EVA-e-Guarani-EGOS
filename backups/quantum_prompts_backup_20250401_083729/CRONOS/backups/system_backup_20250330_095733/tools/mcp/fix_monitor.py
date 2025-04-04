#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Corrige o problema de carregamento de limites e reinicia o monitor.
"""

import os
import json
import sys
import time
from context_monitor import stop_monitoring, start_monitoring, get_status, monitor_state, state_lock

# Configurações
CONTEXT_LIMITS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "BIOS-Q", "context_limits.json"
)

print("Parando o monitor atual...")
stop_monitoring()
time.sleep(2)

print("\nCarregando limites diretamente do BIOS-Q...")
try:
    with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # Corrige possíveis problemas no JSON
        if content.startswith("}"):
            content = content[1:]
        if not content.startswith("{"):
            content = "{" + content

        limits = json.loads(content)

        if "cursor" in limits and limits["cursor"].get("measured", False):
            print(
                f"Limite encontrado: {limits['cursor']['limit']} (safe: {limits['cursor']['safe_limit']})"
            )

            # Atualiza o estado diretamente
            with state_lock:
                monitor_state["context_limit"] = limits["cursor"]["safe_limit"]
                monitor_state["context_source"] = "empirical"
                print(
                    f"Monitor atualizado: {monitor_state['context_limit']} (fonte: {monitor_state['context_source']})"
                )
        else:
            print("Nenhum limite para 'cursor' encontrado!")
except Exception as e:
    print(f"Erro ao carregar limites: {e}")

print("\nIniciando novo monitor...")
time.sleep(1)
start_monitoring()

print("\nVerificando status do monitor:")
status = get_status()
print(f"- Capacidade utilizada: {status['capacity_used']*100:.1f}%")
print(f"- Limite atual: {status['context_limit']} caracteres")
print(f"- Fonte do limite: {status['context_source']}")
print(f"- Mensagens atuais: {status['message_count']}")

is_empirical = status["context_source"] == "empirical"
print(f"\nO sistema está usando o limite empírico: {is_empirical}")
print("Correção concluída!")
