#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Adiciona mais mensagens para ultrapassar o limite de 80%.
"""

from context_monitor import add_message, get_status

# Verifica o status atual
status = get_status()
print(f"Status atual: {status['capacity_used']*100:.1f}%")

# Adiciona mais algumas mensagens
for i in range(20):
    add_message(
        f"Mensagem adicional {i} para ultrapassar 80% da capacidade e testar o salvamento automático."
    )

# Verifica o novo status
new_status = get_status()
print(f"Novo status: {new_status['capacity_used']*100:.1f}%")
print(f"Aumento: {(new_status['capacity_used'] - status['capacity_used'])*100:.1f}%")
print(f"Total de mensagens: {new_status['message_count']}")

print("\nAguarde alguns segundos para o salvamento automático ser acionado...")
print("Use 'python cursor_commands.py mcp_status' para verificar o status.")
