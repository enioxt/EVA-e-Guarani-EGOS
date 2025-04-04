#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reinicia o monitor de contexto para testar carregamento de limites do BIOS-Q.
"""

from context_monitor import stop_monitoring, start_monitoring, get_status, load_context_limits
import time

print("Parando o monitor atual...")
stop_monitoring()
time.sleep(2)

print("\nCarregando limites do BIOS-Q...")
result = load_context_limits()
print(f"- Limite carregado: {result}")

print("\nIniciando novo monitor...")
start_monitoring()
time.sleep(1)  # Espera para inicialização completa

print("\nVerificando status com limite carregado do BIOS-Q:")
status = get_status()
print(f"- Capacidade utilizada: {status['capacity_used']*100:.1f}%")
print(f"- Limite atual: {status['context_limit']} caracteres")
print(f"- Fonte do limite: {status['context_source']}")
print(f"- Mensagens atuais: {status['message_count']}")

is_empirical = status["context_source"] == "empirical"
print(f"\nO sistema está usando o limite empírico: {is_empirical}")
print("Teste concluído!")
