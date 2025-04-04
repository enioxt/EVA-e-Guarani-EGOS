#!/usr/bin/env python3
import json
import os

# Configuração
config = {
    "cursor_paths": {
        "appdata": "C:\\Users\\Enidi\\AppData\\Roaming\\Cursor",
        "home": "C:\\Users\\Enidi\\.cursor",
        "workspace": "C:\\Eva & Guarani - EGOS",
    },
    "bios_paths": {
        "root": "C:\\Eva & Guarani - EGOS\\BIOS-Q",
        "storage": "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\storage",
        "context": "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\storage\\cursor_context",
    },
    "integration": {
        "auto_save": True,
        "backup_enabled": True,
        "sync_interval": 300,
        "max_backups": 10,
        "log_level": "INFO",
        "debug_mode": False,
    },
}

# Caminho do arquivo
config_path = "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\config\\bios_config.json"

# Garantir que o diretório existe
os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Remover o arquivo se existir
if os.path.exists(config_path):
    os.remove(config_path)
    print(f"🗑️ Arquivo antigo removido: {config_path}")

# Criar novo arquivo
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"✅ Novo arquivo criado: {config_path}")

# Verificar se o arquivo foi criado corretamente
try:
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"\n📄 Conteúdo do arquivo:")
        print(content)
        print(f"\n📊 Tamanho: {len(content)} bytes")

    # Tentar carregar como JSON
    with open(config_path, "r", encoding="utf-8") as f:
        json.load(f)
        print("\n✅ Arquivo JSON válido!")
except Exception as e:
    print(f"\n❌ Erro: {str(e)}")
    print(f"Tipo de erro: {type(e).__name__}")
