#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Depura o carregamento de limites do BIOS-Q.
"""

import os
import json
import sys

# Configurações
CONTEXT_LIMITS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "BIOS-Q", "context_limits.json"
)
print(f"Arquivo de limites: {CONTEXT_LIMITS_FILE}")
print(f"Existe: {os.path.exists(CONTEXT_LIMITS_FILE)}")

try:
    # Tenta carregar o arquivo
    with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"\nConteúdo bruto:\n{content}")

        # Interpreta como JSON
        try:
            limits = json.loads(content)
            print(f"\nJSON interpretado:")
            print(json.dumps(limits, indent=2))

            # Verifica as chaves
            if "cursor" in limits:
                print(f"\nLimite do cursor encontrado:")
                print(f"- limit: {limits['cursor'].get('limit')}")
                print(f"- measured: {limits['cursor'].get('measured')}")
                print(f"- safe_limit: {limits['cursor'].get('safe_limit')}")
            else:
                print("\nNenhum limite para 'cursor' encontrado!")
        except json.JSONDecodeError as e:
            print(f"\nErro ao decodificar JSON: {e}")
except Exception as e:
    print(f"\nErro ao abrir arquivo: {e}")
