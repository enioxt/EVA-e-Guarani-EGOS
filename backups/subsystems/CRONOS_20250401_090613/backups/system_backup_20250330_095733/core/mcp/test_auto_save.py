#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste de salvamento automático do monitor de contexto.
Este script simula uma carga que se aproxima dos 80% da capacidade.
"""

import time
from context_monitor import add_message, get_status, start_monitoring, force_save

# Mensagem de teste (aproximadamente 100 caracteres)
TEST_MESSAGE = "Esta é uma mensagem de teste para o monitor de contexto. Vamos verificar o salvamento automático."

# Inicia o monitor
print("Iniciando monitoramento...")
start_monitoring()

# Mostra status inicial
print("\nStatus inicial:")
status = get_status()
print(f"- Capacidade utilizada: {status['capacity_used']*100:.1f}%")
print(f"- Mensagens: {status['message_count']}")
print(f"- Tamanho: {status['current_size']} caracteres")

# Adiciona mensagens até se aproximar de 80%
print("\nAdicionando mensagens...")
count = 0
while status['capacity_used'] < 0.79:
    # Adiciona uma mensagem
    add_message(f"[Mensagem {count}] {TEST_MESSAGE}")
    count += 1
    
    # Verifica status atual
    status = get_status()
    
    # Mostra progresso a cada 10 mensagens
    if count % 10 == 0:
        print(f"- Adicionadas {count} mensagens - Capacidade: {status['capacity_used']*100:.1f}%")
    
    # Pequena pausa para não sobrecarregar
    time.sleep(0.1)

# Mostra status final
print("\nLimite de 80% se aproximando:")
print(f"- Capacidade utilizada: {status['capacity_used']*100:.1f}%")
print(f"- Mensagens adicionadas: {count}")
print(f"- Tamanho total: {status['current_size']} caracteres")
print("\nAguardando salvamento automático (10 segundos)...")

# Aguarda o salvamento automático
time.sleep(10)

# Verifica se o salvamento foi realizado
final_status = get_status()
print("\nStatus após salvamento automático:")
print(f"- Capacidade utilizada: {final_status['capacity_used']*100:.1f}%")
print(f"- Mensagens: {final_status['message_count']}")
print(f"- Último salvamento: {time.ctime(final_status['last_save_time'])}")

# Verifica se o salvamento foi acionado
if final_status['last_save_time'] > status['last_save_time']:
    print("\n✅ Salvamento automático realizado com sucesso!")
else:
    print("\n❌ Salvamento automático não foi acionado como esperado.")
    print("Forçando salvamento manualmente...")
    force_save()

print("\nTeste concluído!") 