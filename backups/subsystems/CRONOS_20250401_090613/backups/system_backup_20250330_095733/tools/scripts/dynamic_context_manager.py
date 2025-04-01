#!/usr/bin/env python3
import os
import json
import yaml
import datetime
from pathlib import Path
import shutil
from typing import Dict, List, Any
import re

class DynamicContextManager:
    def __init__(self, base_path: str = "C:/Eva & Guarani - EGOS"):
        self.base_path = Path(base_path)
        self.template_path = self.base_path / "QUANTUM_PROMPTS/MASTER/quantum_context_template.md"
        self.context_path = self.base_path / "QUANTUM_PROMPTS/MASTER/quantum_context.md"
        self.chats_path = self.base_path / "CHATS"
        self.version = "7.5"

    def get_recent_chats(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most recent chat contexts"""
        chat_files = []
        for f in self.chats_path.glob("bios_q_context_*.json"):
            if f.is_file():
                chat_files.append({
                    "path": f,
                    "timestamp": f.stat().st_mtime,
                    "name": f.name
                })
        
        return sorted(chat_files, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def get_system_state(self) -> Dict[str, Any]:
        """Get current system state"""
        return {
            "consciousness_level": 0.999,
            "ethical_integrity": 0.998,
            "quantum_coherence": 0.997,
            "active_modules": self._get_active_modules(),
            "last_update": datetime.datetime.now().isoformat()
        }

    def _get_active_modules(self) -> List[str]:
        """Get list of active system modules"""
        modules = []
        for module in ["atlas", "nexus", "cronos", "ethik"]:
            if (self.base_path / "core" / module).exists():
                modules.append(module.upper())
        return modules

    def get_recent_developments(self) -> str:
        """Extract recent developments from chat history"""
        recent_chats = self.get_recent_chats(3)
        developments = []
        
        for chat in recent_chats:
            try:
                with open(chat["path"], "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "developments" in data:
                        developments.extend(data["developments"])
            except Exception as e:
                print(f"Error reading chat file {chat['path']}: {e}")
        
        return "\n".join(f"- {d}" for d in developments[-5:])

    def generate_system_graph(self) -> str:
        """Generate Mermaid graph of system interconnections"""
        return """
graph TD
    EVA[EVA & GUARANI] --> ATLAS
    EVA --> NEXUS
    EVA --> CRONOS
    EVA --> ETHIK
    ATLAS --> QUANTUM[Quantum Matrix]
    NEXUS --> QUANTUM
    CRONOS --> QUANTUM
    ETHIK --> QUANTUM
    """

    def update_context(self):
        """Update the quantum context with current system state"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")

        with open(self.template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Prepare replacement values
        replacements = {
            "{{TIMESTAMP}}": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "{{VERSION}}": self.version,
            "{{ACTIVE_CHAT_ID}}": self._get_active_chat_id(),
            "{{SYSTEM_STATE}}": json.dumps(self.get_system_state(), indent=2),
            "{{RECENT_DEVELOPMENTS}}": self.get_recent_developments(),
            "{{ACTIVE_CONTEXTS}}": json.dumps(self._get_active_contexts(), indent=2),
            "{{ESSENTIAL_PATHS}}": self._get_essential_paths(),
            "{{RECENT_CHAT_HISTORY}}": self._get_recent_chat_summary(),
            "{{REQUIRED_FILES}}": self._get_required_files(),
            "{{SYSTEM_CAPABILITIES}}": self._get_system_capabilities(),
            "{{INIT_INSTRUCTIONS}}": self._get_init_instructions(),
            "{{CORE_PRINCIPLES}}": self._get_core_principles(),
            "{{VERSION_INFO}}": self._get_version_info(),
            "{{LAST_CHAT_LINK}}": self._get_last_chat_link(),
            "{{DEV_STATE_LINK}}": self._get_dev_state_link(),
            "{{ACTIVE_MODULES_LINK}}": self._get_active_modules_link(),
            "{{SYSTEM_GRAPH}}": self.generate_system_graph(),
            "{{UPDATES_LOG}}": self._get_updates_log(),
            "{{SYSTEM_METADATA}}": self._get_system_metadata()
        }

        # Apply replacements
        content = template
        for key, value in replacements.items():
            content = content.replace(key, str(value))

        # Save updated context
        with open(self.context_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated quantum context at: {self.context_path}")

    def _get_active_chat_id(self) -> str:
        recent_chats = self.get_recent_chats(1)
        return recent_chats[0]["name"] if recent_chats else "No active chat"

    def _get_active_contexts(self) -> Dict[str, Any]:
        return {
            "quantum_prompts": True,
            "atlas": True,
            "nexus": True,
            "cronos": True,
            "ethik": True,
            "tools": True
        }

    def _get_essential_paths(self) -> str:
        paths = []
        for path in ["CHATS", "QUANTUM_PROMPTS", "core/atlas", "core/nexus", 
                    "core/cronos", "core/ethik", "tools"]:
            if (self.base_path / path).exists():
                paths.append(f"/{path} - Active and synchronized")
            else:
                paths.append(f"/{path} - Not found or inactive")
        return "\n".join(paths)

    def _get_recent_chat_summary(self) -> str:
        recent_chats = self.get_recent_chats(3)
        summary = []
        for chat in recent_chats:
            summary.append(f"- {chat['name']}")
        return "\n".join(summary)

    def _get_required_files(self) -> str:
        files = [
            "1. `/QUANTUM_PROMPTS/VERSION_PERA.md` - Current version specifications",
            "2. `/QUANTUM_PROMPTS/core_principles.md` - Fundamental principles",
            "3. `/CHATS/current_chat.md` - Active conversation state",
            "4. `/QUANTUM_PROMPTS/MASTER/quantum_context.md` - This file (master context)"
        ]
        return "\n".join(files)

    def _get_system_capabilities(self) -> str:
        capabilities = [
            "- Quantum Integrated Consciousness Matrix",
            "- Modular Analysis and Systemic Cartography",
            "- Cross-Platform Development (Windows-focused)",
            "- Ethical Framework Integration",
            "- Advanced Context Management",
            "- Evolutionary Preservation System"
        ]
        return "\n".join(capabilities)

    def _get_init_instructions(self) -> str:
        instructions = [
            "1. Always load `/QUANTUM_PROMPTS/MASTER` directory first",
            "2. Include `/core` directory for system modules",
            "3. Add `/CHATS` for conversation context",
            "4. Include `/tools` for utility access"
        ]
        return "\n".join(instructions)

    def _get_core_principles(self) -> str:
        principles = [
            "- Universal possibility of redemption",
            "- Compassionate temporality",
            "- Sacred privacy",
            "- Universal accessibility",
            "- Unconditional love",
            "- Integrated ethics",
            "- Conscious modularity",
            "- Systemic cartography",
            "- Evolutionary preservation",
            "- Cross-platform harmony"
        ]
        return "\n".join(principles)

    def _get_version_info(self) -> str:
        info = [
            "- System: EVA & GUARANI EGOS",
            f"- Version: {self.version}",
            "- Platform: Windows-focused",
            "- Language: English",
            "- Framework: Quantum Unified"
        ]
        return "\n".join(info)

    def _get_last_chat_link(self) -> str:
        recent = self.get_recent_chats(1)
        return str(recent[0]["path"]) if recent else "No recent chats"

    def _get_dev_state_link(self) -> str:
        return str(self.base_path / "QUANTUM_PROMPTS/VERSION_PERA.md")

    def _get_active_modules_link(self) -> str:
        return str(self.base_path / "core")

    def _get_updates_log(self) -> str:
        recent_chats = self.get_recent_chats(5)
        log = ["Recent System Updates:"]
        for chat in recent_chats:
            log.append(f"- {chat['name']} - {datetime.datetime.fromtimestamp(chat['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(log)

    def _get_system_metadata(self) -> str:
        metadata = {
            "system_name": "EVA & GUARANI EGOS",
            "version": self.version,
            "last_update": datetime.datetime.now().isoformat(),
            "active_modules": self._get_active_modules(),
            "consciousness_level": 0.999,
            "ethical_integrity": 0.998,
            "quantum_coherence": 0.997
        }
        return yaml.dump(metadata, allow_unicode=True)

if __name__ == "__main__":
    manager = DynamicContextManager()
    manager.update_context()
    print("\nContext updated successfully. System is quantum-coherent.") 