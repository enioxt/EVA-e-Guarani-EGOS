#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste final do monitor de contexto MCP.
"""

import time
from context_monitor import add_message, get_status, start_monitoring, force_save

# Certifica-se de que o monitor está rodando
print("Iniciando monitor...")
start_monitoring()

# Exibe status inicial
status = get_status()
print(f"\nStatus inicial:")
print(f"- Capacidade: {status['capacity_used']*100:.1f}%")
print(f"- Mensagens: {status['message_count']}")
print(f"- Último salvamento: {time.ctime(status['last_save_time'])}")

# Adiciona mensagens grandes para ultrapassar 80% rapidamente
print("\nAdicionando mensagens para ultrapassar 80%...")
LARGE_MESSAGE = "X" * 8000  # 8000 caracteres
for i in range(11):  # 11 x 8000 = 88000 (acima de 80% do limite de 100000)
    add_message(f"[Chunk {i}] {LARGE_MESSAGE}")
    print(f"- Adicionado chunk {i} - Capacidade: {get_status()['capacity_used']*100:.1f}%")

# Aguarda o salvamento automático
print("\nAguardando salvamento automático (5 segundos)...")
time.sleep(5)

# Verifica se o salvamento foi acionado
final_status = get_status()
print("\nStatus final:")
print(f"- Capacidade: {final_status['capacity_used']*100:.1f}%")
print(f"- Mensagens: {final_status['message_count']}")
print(f"- Último salvamento: {time.ctime(final_status['last_save_time'])}")

if final_status["last_save_time"] > status["last_save_time"]:
    print("\n✅ SUCESSO: Salvamento automático a 80% funcionou!")
else:
    print("\n❌ FALHA: Salvamento automático não ocorreu como esperado")
    print("Forçando salvamento manualmente...")
    force_save()

print("\nTeste concluído!")
