#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quantum Prompt Manager
====================

Sistema de gerenciamento e integração dos Quantum Prompts do EVA & GUARANI.
Responsável por:
1. Carregar prompts na ordem correta
2. Manter sincronização
3. Atualizar o prompt do Cursor
4. Gerenciar dependências
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime


class QuantumPromptManager:
    def __init__(self, config_path="config/quantum_prompts.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.loaded_prompts = {}
        self.master_content = ""

    def _load_config(self):
        """Carrega a configuração dos prompts"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return None

    def _load_prompt_file(self, path):
        """Carrega um arquivo de prompt"""
        try:
            abs_path = os.path.join(os.path.dirname(self.config_path), "..", path.lstrip("/"))
            with open(abs_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao carregar prompt {path}: {e}")
            return ""

    def _save_prompt_file(self, path, content):
        """Salva um arquivo de prompt"""
        try:
            abs_path = os.path.join(os.path.dirname(self.config_path), "..", path.lstrip("/"))
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Erro ao salvar prompt {path}: {e}")
            return False

    def load_all_prompts(self):
        """Carrega todos os prompts na ordem correta"""
        if not self.config:
            return False

        # Carregar master prompt primeiro
        self.master_content = self._load_prompt_file(self.config["master_prompt"])
        self.loaded_prompts["master_prompt"] = self.master_content

        # Carregar prompts dos subsistemas na ordem definida
        for system_name in self.config["load_order"][1:]:  # Skip master_prompt
            if system_name in self.config["subsystems"]:
                system = self.config["subsystems"][system_name]
                content = self._load_prompt_file(system["prompt_path"])
                self.loaded_prompts[system_name] = content

        return True

    def update_cursor_prompt(self):
        """Atualiza o prompt do Cursor com o conteúdo integrado"""
        if not self.loaded_prompts:
            self.load_all_prompts()

        # Criar conteúdo integrado
        integrated_content = [
            "# EVA & GUARANI - Integrated Quantum Prompt\n",
            f"# Generated: {datetime.now().isoformat()}\n\n",
            "## Master Context\n",
            self.master_content,
            "\n## Subsystem Contexts\n",
        ]

        # Adicionar prompts dos subsistemas
        for system_name in self.config["load_order"][1:]:
            if system_name in self.loaded_prompts:
                integrated_content.extend(
                    [f"\n### {system_name.upper()}\n", self.loaded_prompts[system_name]]
                )

        # Salvar no diretório do Cursor
        cursor_path = self.config["sync_paths"]["cursor"]
        prompt_path = os.path.join(cursor_path, "quantum_prompt.txt")

        try:
            os.makedirs(cursor_path, exist_ok=True)
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(integrated_content))
            return True
        except Exception as e:
            print(f"Erro ao atualizar prompt do Cursor: {e}")
            return False

    def create_subsystem_prompt(self, system_name, content):
        """Cria um novo prompt para um subsistema"""
        if not self.config:
            return False

        if system_name not in self.config["subsystems"]:
            print(f"Subsistema {system_name} não encontrado na configuração")
            return False

        system = self.config["subsystems"][system_name]
        return self._save_prompt_file(system["prompt_path"], content)

    def sync_all_prompts(self):
        """Sincroniza todos os prompts e atualiza o Cursor"""
        success = self.load_all_prompts()
        if success:
            return self.update_cursor_prompt()
        return False


def main():
    """Função principal para uso via linha de comando"""
    manager = QuantumPromptManager()

    print("EVA & GUARANI - Quantum Prompt Manager")
    print("======================================")

    if manager.sync_all_prompts():
        print("✓ Todos os prompts foram sincronizados com sucesso")
        print(f"✓ Prompt do Cursor atualizado em: {manager.config['sync_paths']['cursor']}")
    else:
        print("⚠ Erro ao sincronizar prompts")


if __name__ == "__main__":
    main()
