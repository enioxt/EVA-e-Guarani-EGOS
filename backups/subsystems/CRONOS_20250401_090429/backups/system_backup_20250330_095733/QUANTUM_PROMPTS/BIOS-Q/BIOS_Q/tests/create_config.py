#!/usr/bin/env python3
import json
import os

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

config_path = "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\config\\bios_config.json"

# Garantir que o diretório existe
os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Escrever o arquivo com codificação UTF-8
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

print(f"✅ Arquivo de configuração criado em: {config_path}")
