#!/usr/bin/env python3
﻿"""
BIOS-Q Context Manager
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class ContextManager:
    """Gerenciador de contexto do BIOS-Q"""

    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage"

        self.storage_dir = storage_dir
        self.context_dir = storage_dir / "context"
        self.backup_dir = storage_dir / "backup"

        # Cria diretórios se não existirem
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def add_message(self, role: str, content: str) -> bool:
        timestamp = time.time()
        context = {
            "role": role,
            "content": content,
            "timestamp": timestamp,
            "source": "BIOS-Q"
        }

        try:
            context_file = self.context_dir / f"context_{int(timestamp)}.json"
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def get_context(self, max_age: Optional[float] = None) -> List[Dict[str, Any]]:
        context_files = sorted(self.context_dir.glob("context_*.json"))

        if max_age is not None:
            min_timestamp = time.time() - max_age
            context_files = [f for f in context_files
                           if float(f.stem.split('_')[1]) >= min_timestamp]

        contexts = []
        for file in context_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    contexts.append(json.load(f))
            except Exception:
                continue

        return contexts

    def create_backup(self) -> Optional[str]:
        try:
            timestamp = time.time()
            backup_file = self.backup_dir / f"backup_{int(timestamp)}.json"

            contexts = self.get_context()

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(contexts, f, ensure_ascii=False, indent=2)

            return str(backup_file)
        except Exception:
            return None
