#!/usr/bin/env python3
﻿import re
import os
import sys

# Caminho do relatório
report_path = "C:/Eva & Guarani - EGOS/tools/language/translation_report.md"
project_root = "C:/Eva & Guarani - EGOS"

print(f"Processando relatório: {report_path}")
print("=" * 50)

# Ler o relatório
try:
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
except Exception as e:
    print(f"Erro ao ler o relatório: {e}")
    sys.exit(1)

# Extrair caminhos de arquivo
pattern = r"\|\s*([^|]+\.(?:py|md|txt|json|js|html|css|bat|ps1))\s*\|"
matches = re.findall(pattern, content)

if not matches:
    print("Nenhum arquivo encontrado no relatório")
    sys.exit(1)

print(f"Encontrados {len(matches)} arquivos para processar")
print("=" * 50)

# Processar cada arquivo
success = 0
failed = 0

# Obter o caminho completo para o script de tradução
translator_path = os.path.join(os.path.dirname(__file__), "ai_translate_file.py")

for match in matches:
    path = match.strip()
    if path and not path.startswith("Size") and not path.startswith("Type"):
        abs_path = os.path.join(project_root, path).replace("\\", "/")
        if os.path.exists(abs_path):
            print(f"Traduzindo: {abs_path}")
            # Comando para traduzir com caminho completo
            result = os.system(f'python "{translator_path}" --file "{abs_path}"')
            if result == 0:
                success += 1
            else:
                failed += 1
        else:
            print(f"Arquivo não encontrado: {abs_path}")
            failed += 1

print("=" * 50)
print(f"Processo concluído: {success} sucesso, {failed} falhas")