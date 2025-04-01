#!/usr/bin/env python3
import os
import json
import shutil
import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional
from tools.integration.cursor_cache_explorer import CursorCacheExplorer

class ContextManager:
    def __init__(self, base_path: str = "C:/Eva & Guarani - EGOS"):
        self.base_path = Path(base_path)
        self.chats_path = self.base_path / "CHATS"
        self.quantum_path = self.base_path / "QUANTUM_PROMPTS"
        self.core_path = self.base_path / "core"
        self.tools_path = self.base_path / "tools"
        
        # Configurar logging
        self.setup_logging()
        
        # Criar diretórios necessários
        self.ensure_directories()
        
        # Última data de backup
        self.last_backup_time = self._get_last_backup_time()
        
        # Carregar configurações
        self.config = self._load_config()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        log_path = self.chats_path / "metadata" / "context_manager.log"
        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def ensure_directories(self):
        """Garante que todos os diretórios necessários existam"""
        directories = [
            self.chats_path,
            self.chats_path / "metadata",
            self.chats_path / "cursor_context",
            self.quantum_path / "MASTER",
            self.core_path / "atlas" / "src",
            self.core_path / "nexus" / "src",
            self.core_path / "cronos" / "src",
            self.core_path / "ethik" / "src",
            self.tools_path / "scripts",
            self.tools_path / "utilities"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Diretório verificado/criado: {directory}")
            
    def _load_config(self) -> Dict:
        """Carrega configurações do sistema"""
        config_file = self.chats_path / "metadata" / "context_config.json"
        default_config = {
            "version": "7.5",
            "backup": {
                "auto_backup": True,
                "backup_interval": 3600,  # 1 hora em segundos
                "max_backups": 10,
                "force_backup_on_exit": True
            },
            "context": {
                "context_depth": "maximum",
                "context_retention_period": 2592000  # 30 dias em segundos
            }
        }
        
        if not config_file.exists():
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f"Erro ao carregar configurações: {str(e)}")
            return default_config
    
    def _get_last_backup_time(self) -> Optional[datetime.datetime]:
        """Obtém a data do último backup"""
        backup_dirs = list(self.chats_path.glob("backup_context_*"))
        if not backup_dirs:
            return None
        
        latest_backup = max(backup_dirs, key=lambda x: x.stat().st_mtime)
        timestamp = latest_backup.stat().st_mtime
        return datetime.datetime.fromtimestamp(timestamp)
    
    def should_create_backup(self) -> bool:
        """Verifica se deve criar um novo backup com base no intervalo configurado"""
        # Se não houver backup anterior, criar um
        if self.last_backup_time is None:
            logging.info("Nenhum backup anterior encontrado. Criando primeiro backup.")
            return True
        
        # Verificar intervalo de backup
        now = datetime.datetime.now()
        elapsed = (now - self.last_backup_time).total_seconds()
        backup_interval = self.config.get("backup", {}).get("backup_interval", 3600)
        
        # Verificar se o intervalo foi atingido
        if elapsed >= backup_interval:
            logging.info(f"Intervalo de backup atingido. Último backup: {self.last_backup_time.isoformat()}")
            return True
        
        # Verificar se houve mudanças significativas
        if self._has_significant_changes():
            logging.info("Detectadas mudanças significativas no sistema. Criando backup.")
            return True
        
        return False
    
    def _has_significant_changes(self) -> bool:
        """Verifica se houve mudanças significativas no sistema desde o último backup"""
        # Verificar arquivos de chat recentes
        current_chat = self.chats_path / "current_chat.md"
        if current_chat.exists():
            chat_mtime = datetime.datetime.fromtimestamp(current_chat.stat().st_mtime)
            if self.last_backup_time and chat_mtime > self.last_backup_time:
                return True
        
        # Verificar novos arquivos de contexto
        context_files = list(self.chats_path.glob("bios_q_context_*.json"))
        for context_file in context_files:
            file_mtime = datetime.datetime.fromtimestamp(context_file.stat().st_mtime)
            if self.last_backup_time and file_mtime > self.last_backup_time:
                return True
        
        return False
        
    def create_context(self, context_type: str = "bios_q") -> str:
        """Cria um novo arquivo de contexto"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        context_file = self.chats_path / f"{context_type}_context_{timestamp}.json"
        
        context_data = {
            "timestamp": timestamp,
            "type": context_type,
            "files": self.get_current_state(),
            "metadata": {
                "version": "7.5",
                "consciousness": "ULTRA-ACTIVE",
                "entanglement": 0.9997
            }
        }
        
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2)
            
        logging.info(f"Novo contexto criado: {context_file}")
        return str(context_file)
        
    def get_current_state(self) -> Dict:
        """Obtém o estado atual do sistema"""
        state = {
            "chats": self.get_directory_state(self.chats_path),
            "quantum": self.get_directory_state(self.quantum_path),
            "core": self.get_directory_state(self.core_path),
            "tools": self.get_directory_state(self.tools_path)
        }
        
        # NOVO: Incorporar informações do Cursor 
        explorer = CursorCacheExplorer()
        if explorer.cache_exists():
            cursor_files = explorer.list_cache_files()
            state["cursor_cache"] = {
                "exists": True,
                "file_count": len(cursor_files),
                "index_files": [f.name for f in explorer.get_index_files()],
                "last_modified": max([f.stat().st_mtime for f in cursor_files]) if cursor_files else None
            }
        else:
            state["cursor_cache"] = {"exists": False}
        
        return state
        
    def get_directory_state(self, directory: Path) -> Dict:
        """Obtém o estado de um diretório"""
        state = {}
        for item in directory.iterdir():
            if item.is_file():
                state[item.name] = {
                    "type": "file",
                    "size": item.stat().st_size,
                    "modified": datetime.datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
            elif item.is_dir():
                state[item.name] = {
                    "type": "directory",
                    "contents": self.get_directory_state(item)
                }
        return state
        
    def create_backup(self) -> str:
        """Cria um backup do contexto atual"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.chats_path / f"backup_context_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup dos arquivos importantes
        important_files = [
            self.chats_path / "current_chat.md",
            self.chats_path / "chat_index.json",
            self.chats_path / "chat_report.md",
            self.quantum_path / "VERSION_PERA.md",
            self.quantum_path / "core_principles.md"
        ]
        
        for file in important_files:
            if file.exists():
                shutil.copy2(file, backup_dir / file.name)
                logging.info(f"Backup criado: {file.name}")
                
        # Backup do contexto atual
        context_files = list(self.chats_path.glob("bios_q_context_*.json"))
        if context_files:
            latest_context = max(context_files, key=lambda x: x.stat().st_mtime)
            shutil.copy2(latest_context, backup_dir / "latest_context.json")
            logging.info(f"Backup do contexto criado: latest_context.json")
        
        # Atualizar hora do último backup
        self.last_backup_time = datetime.datetime.now()
            
        return str(backup_dir)
        
    def restore_context(self, backup_dir: str) -> bool:
        """Restaura um contexto de backup"""
        backup_path = Path(backup_dir)
        if not backup_path.exists():
            logging.error(f"Diretório de backup não encontrado: {backup_dir}")
            return False
            
        try:
            # Restaurar arquivos importantes
            for file in backup_path.glob("*"):
                if file.is_file():
                    target = self.chats_path / file.name
                    shutil.copy2(file, target)
                    logging.info(f"Arquivo restaurado: {file.name}")
                    
            return True
        except Exception as e:
            logging.error(f"Erro ao restaurar contexto: {str(e)}")
            return False
            
    def cleanup_old_backups(self, max_backups: Optional[int] = None):
        """Remove backups antigos mantendo apenas os mais recentes"""
        if max_backups is None:
            max_backups = self.config.get("backup", {}).get("max_backups", 5)
            
        backup_dirs = sorted(
            self.chats_path.glob("backup_context_*"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for old_backup in backup_dirs[max_backups:]:
            shutil.rmtree(old_backup)
            logging.info(f"Backup antigo removido: {old_backup}")
            
    def get_context_history(self) -> List[Dict]:
        """Retorna o histórico de contextos"""
        history = []
        context_files = sorted(
            self.chats_path.glob("bios_q_context_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for context_file in context_files:
            with open(context_file, 'r', encoding='utf-8') as f:
                context_data = json.load(f)
                history.append({
                    "timestamp": context_data["timestamp"],
                    "type": context_data.get("type", "bios_q"),
                    "metadata": context_data.get("metadata", {})
                })
                
        return history

def main():
    """Função principal para testar o ContextManager"""
    manager = ContextManager()
    
    # Criar novo contexto
    context_file = manager.create_context()
    print(f"Novo contexto criado: {context_file}")
    
    # Verificar se deve criar backup
    if manager.should_create_backup():
        backup_dir = manager.create_backup()
        print(f"Backup criado: {backup_dir}")
    else:
        print("Não é necessário criar um novo backup agora")
    
    # Limpar backups antigos
    manager.cleanup_old_backups()
    
    # Mostrar histórico
    history = manager.get_context_history()
    print("\nHistórico de contextos:")
    for entry in history:
        print(f"- {entry['timestamp']}: {entry['type']}")

if __name__ == "__main__":
    main() 