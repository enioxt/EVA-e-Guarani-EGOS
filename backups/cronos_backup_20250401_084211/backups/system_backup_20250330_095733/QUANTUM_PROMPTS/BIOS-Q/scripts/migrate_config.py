#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path

def migrate_bios_q_config():
    """
    Migra as configurações do BIOS-Q_backup para BIOS-Q
    mantendo a estrutura original e atualizando os caminhos.
    """
    # Caminhos base
    base_path = Path("/c/Eva Guarani EGOS")
    bios_q_path = base_path / "BIOS-Q"
    config_path = bios_q_path / "config"
    
    # Criar diretório de configuração se não existir
    config_path.mkdir(parents=True, exist_ok=True)
    
    # Configuração do BIOS-Q
    bios_q_config = {
        "version": "1.0.0",
        "name": "BIOS-Q MCP",
        "description": "Quantum System Initialization Protocol",
        "paths": {
            "root": str(base_path),
            "quantum_prompts": str(base_path / "QUANTUM_PROMPTS"),
            "bios_q": str(bios_q_path)
        },
        "mcps": {
            "sequential-thinking": {
                "active": True,
                "priority": 1,
                "description": "Complex problem solving and analysis"
            },
            "perplexity": {
                "active": True,
                "priority": 2,
                "description": "Web-based research and information gathering"
            },
            "bios-q": {
                "active": True,
                "priority": 0,
                "description": "System initialization and context management"
            }
        },
        "subsystems": {
            "ATLAS": {
                "required": True,
                "description": "Visualization and cartography"
            },
            "CRONOS": {
                "required": True,
                "description": "State preservation and evolution"
            },
            "ETHIK": {
                "required": True,
                "description": "Ethical framework and validation"
            },
            "NEXUS": {
                "required": True,
                "description": "Modular analysis and integration"
            },
            "MASTER": {
                "required": True,
                "description": "Central coordination and oversight"
            }
        },
        "initialization": {
            "verify_structure": True,
            "load_context": True,
            "verify_dependencies": True,
            "display_banner": True,
            "load_setup_instructions": True
        },
        "logging": {
            "level": "INFO",
            "format": "quantum",
            "file": "bios_q.log"
        },
        "cursor_integration": {
            "auto_initialize": True,
            "setup_commands": [
                "cd /c/Eva\\ Guarani\\ EGOS/QUANTUM_PROMPTS",
                "pip install -r requirements.txt",
                "python -m pytest"
            ]
        }
    }
    
    # Salvar nova configuração
    config_file = config_path / "bios_q_config.json"
    with open(config_file, "w") as f:
        json.dump(bios_q_config, f, indent=4)
        
    print(f"Configuração migrada para {config_file}")

if __name__ == "__main__":
    migrate_bios_q_config() 