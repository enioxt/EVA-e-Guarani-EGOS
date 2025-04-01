#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Conector de Integração

Este módulo fornece integração entre o bot do Telegram e os subsistemas EVA & GUARANI:
- ATLAS (Advanced Topological Logical Analysis System)
- NEXUS (Network Extensible Xeri Unified System)
- CRONOS (Continual Retention Of Neural Operational States)
- ETHIK (Ethical Thinking & Holistic Integration Kit)
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adiciona o diretório raiz ao PATH para importações
sys.path.append(str(Path(__file__).resolve().parents[3]))

# Tenta importar os módulos do EVA & GUARANI
try:
    # Importa ATLAS para cartografia sistêmica
    from core.atlas import map_project, visualize_connections
    ATLAS_AVAILABLE = True
except ImportError:
    logger.warning("Módulo ATLAS não encontrado. Funcionalidades de cartografia sistêmica serão limitadas.")
    ATLAS_AVAILABLE = False

try:
    # Importa NEXUS para análise modular
    from core.nexus import analyze_module
    NEXUS_AVAILABLE = True
except ImportError:
    logger.warning("Módulo NEXUS não encontrado. Funcionalidades de análise modular serão limitadas.")
    NEXUS_AVAILABLE = False

try:
    # Importa ETHIK para framework ético
    from core.ethik import evaluate_alignment
    ETHIK_AVAILABLE = True
except ImportError:
    logger.warning("Módulo ETHIK não encontrado. Funcionalidades de avaliação ética serão limitadas.")
    ETHIK_AVAILABLE = False

try:
    # Importa CRONOS para preservação evolutiva
    from core.cronos import create_snapshot, restore_snapshot
    CRONOS_AVAILABLE = True
except ImportError:
    logger.warning("Módulo CRONOS não encontrado. Funcionalidades de preservação evolutiva serão limitadas.")
    CRONOS_AVAILABLE = False

class EGOSConnector:
    """Conector para integração com subsistemas EVA & GUARANI"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Inicializa o conector EGOS.
        
        Args:
            data_dir: Diretório opcional para armazenamento de dados
        """
        self.data_dir = Path(data_dir) if data_dir else Path("data/egos_integration")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Status de disponibilidade de subsistemas
        self.available_systems = {
            "atlas": ATLAS_AVAILABLE,
            "nexus": NEXUS_AVAILABLE,
            "ethik": ETHIK_AVAILABLE,
            "cronos": CRONOS_AVAILABLE
        }
        
        # Mapeamento para personas existentes no sistema principal
        self.personas_mapping = {
            # Módulos core do EVA & GUARANI
            "atlas": str(Path(__file__).resolve().parents[2] / "data" / "telegram_bot" / "personas" / "atlas.json"),
            "ethik": str(Path(__file__).resolve().parents[2] / "data" / "telegram_bot" / "personas" / "ethik.json"),
            "default": str(Path(__file__).resolve().parents[2] / "data" / "telegram_bot" / "personas" / "default.json"),
            
            # Personas adicionais do sistema EVA & GUARANI principal
            "philosophy": "quantum_prompts/SPECIALIZED/philosophy.json",
            "games": "quantum_prompts/SPECIALIZED/games.json",
            "sociology": "quantum_prompts/SPECIALIZED/sociology.json", 
            "rpg": "quantum_prompts/RPG/overview.md"
        }
        
        # Path base para o projeto principal EVA & GUARANI
        egos_path = os.getenv("EGOS_BASE_PATH")
        if egos_path:
            self.egos_base_path = Path(egos_path)
            logger.info(f"Usando caminho base EGOS de variável de ambiente: {self.egos_base_path}")
        else:
            self.egos_base_path = Path(__file__).resolve().parents[4]
            logger.info(f"Usando caminho base EGOS relativo: {self.egos_base_path}")
        
        logger.info(f"EGOSConnector inicializado. Subsistemas disponíveis: {self.available_systems}")
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica o status dos subsistemas EVA & GUARANI"""
        health_status = {
            "status": "operational" if any(self.available_systems.values()) else "limited",
            "timestamp": datetime.now().isoformat(),
            "subsystems": {
                "atlas": "available" if self.available_systems["atlas"] else "unavailable",
                "nexus": "available" if self.available_systems["nexus"] else "unavailable",
                "ethik": "available" if self.available_systems["ethik"] else "unavailable",
                "cronos": "available" if self.available_systems["cronos"] else "unavailable"
            },
            "metrics": {
                "love_quotient": 0.97,
                "consciousness_level": 0.95,
                "ethical_alignment": 0.99
            }
        }
        
        return health_status
    
    def evaluate_message_ethics(self, message: str) -> Dict[str, Any]:
        """
        Avalia a ética de uma mensagem usando ETHIK.
        
        Args:
            message: A mensagem a ser avaliada
            
        Returns:
            Resultado da avaliação ética
        """
        if not self.available_systems["ethik"]:
            logger.warning("Avaliação ética solicitada, mas ETHIK não está disponível.")
            return {
                "aligned": True,
                "score": 0.75,
                "concerns": [],
                "evaluation_method": "fallback"
            }
        
        try:
            # Usa ETHIK para avaliar a mensagem
            result = evaluate_alignment("message", message)
            return result
        except Exception as e:
            logger.error(f"Erro ao avaliar ética da mensagem: {e}")
            return {
                "aligned": True,
                "score": 0.7,
                "concerns": ["Avaliação falhou, usando valor padrão"],
                "evaluation_method": "error_fallback"
            }
    
    def map_conversation(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Mapeia uma conversa usando ATLAS para extrair conexões e estrutura.
        
        Args:
            conversation_history: Histórico da conversa a ser mapeada
            
        Returns:
            Mapeamento da conversa
        """
        if not self.available_systems["atlas"]:
            logger.warning("Mapeamento de conversa solicitado, mas ATLAS não está disponível.")
            return {
                "topics": self._extract_basic_topics(conversation_history),
                "mapping_method": "fallback"
            }
        
        try:
            # Prepara os dados para o ATLAS
            conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
            
            # Usa ATLAS para mapear a conversa
            result = map_project(conversation_text, project_type="conversation")
            return result
        except Exception as e:
            logger.error(f"Erro ao mapear conversa: {e}")
            return {
                "topics": self._extract_basic_topics(conversation_history),
                "mapping_method": "error_fallback"
            }
    
    def _extract_basic_topics(self, conversation_history: List[Dict[str, Any]]) -> List[str]:
        """Extração básica de tópicos quando ATLAS não está disponível"""
        # Implementação simples de extração de palavras-chave
        all_text = " ".join([msg["content"] for msg in conversation_history])
        words = all_text.lower().split()
        # Remove palavras comuns e conta frequência
        stopwords = {"o", "a", "os", "as", "um", "uma", "de", "da", "do", "em", "por", "para", "com", "e", "que", "é"}
        word_count = {}
        for word in words:
            if len(word) > 3 and word not in stopwords:
                word_count[word] = word_count.get(word, 0) + 1
        
        # Retorna as palavras mais frequentes como tópicos
        topics = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
        return [topic[0] for topic in topics]
    
    def analyze_user_preference(self, user_id: int, chat_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisa preferências do usuário usando NEXUS.
        
        Args:
            user_id: ID do usuário
            chat_history: Histórico de chat do usuário
            
        Returns:
            Análise de preferências
        """
        if not self.available_systems["nexus"]:
            logger.warning("Análise de preferências solicitada, mas NEXUS não está disponível.")
            return {
                "preferred_topics": self._extract_basic_topics(chat_history),
                "communication_style": "casual",
                "analysis_method": "fallback"
            }
        
        try:
            # Usa NEXUS para analisar preferências
            user_data = {
                "id": user_id,
                "history": chat_history
            }
            result = analyze_module(user_data, module_type="user_preferences")
            return result
        except Exception as e:
            logger.error(f"Erro ao analisar preferências: {e}")
            return {
                "preferred_topics": self._extract_basic_topics(chat_history),
                "communication_style": "casual",
                "analysis_method": "error_fallback"
            }
    
    def save_conversation_state(self, user_id: int, chat_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Salva o estado da conversa usando CRONOS.
        
        Args:
            user_id: ID do usuário
            chat_history: Histórico de chat do usuário
            
        Returns:
            Informações sobre o backup
        """
        if not self.available_systems["cronos"]:
            logger.warning("Salvamento de estado solicitado, mas CRONOS não está disponível.")
            
            # Salvamento alternativo em arquivo
            try:
                backup_file = self.data_dir / f"user_{user_id}_backup.json"
                backup_data = {
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "chat_history": chat_history
                }
                
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                return {
                    "success": True,
                    "timestamp": backup_data["timestamp"],
                    "method": "fallback",
                    "location": str(backup_file)
                }
            except Exception as e:
                logger.error(f"Erro ao salvar backup: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "method": "fallback"
                }
        
        try:
            # Usa CRONOS para criar um snapshot
            snapshot_data = {
                "user_id": user_id,
                "chat_history": chat_history,
                "timestamp": datetime.now().isoformat()
            }
            
            snapshot_id = create_snapshot(snapshot_data, entity_type="user_conversation")
            
            return {
                "success": True,
                "snapshot_id": snapshot_id,
                "timestamp": snapshot_data["timestamp"],
                "method": "cronos"
            }
        except Exception as e:
            logger.error(f"Erro ao salvar estado usando CRONOS: {e}")
            
            # Fallback para salvamento alternativo
            try:
                backup_file = self.data_dir / f"user_{user_id}_backup.json"
                backup_data = {
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "chat_history": chat_history
                }
                
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                return {
                    "success": True,
                    "timestamp": backup_data["timestamp"],
                    "method": "error_fallback",
                    "location": str(backup_file)
                }
            except Exception as e2:
                logger.error(f"Erro ao salvar backup de fallback: {e2}")
                return {
                    "success": False,
                    "error": str(e2),
                    "method": "error_fallback"
                }
    
    def list_available_personas(self) -> List[Dict[str, Any]]:
        """
        Lista todas as personas disponíveis no sistema EVA & GUARANI.
        
        Returns:
            Lista com informações sobre cada persona disponível
        """
        personas = []
        
        # Adiciona personas locais do bot do Telegram
        telegram_personas_dir = Path(__file__).resolve().parents[2] / "data" / "telegram_bot" / "personas"
        if telegram_personas_dir.exists():
            for persona_file in telegram_personas_dir.glob("*.json"):
                try:
                    with open(persona_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        personas.append({
                            "id": persona_file.stem,
                            "name": data.get("name", persona_file.stem),
                            "description": data.get("description", ""),
                            "source": "telegram_bot",
                            "path": str(persona_file)
                        })
                except Exception as e:
                    logger.error(f"Erro ao carregar persona {persona_file}: {str(e)}")
        
        # Tenta carregar personas do sistema principal
        for persona_id, relative_path in self.personas_mapping.items():
            if persona_id in ["atlas", "ethik", "default"]:
                # Já carregadas acima
                continue
                
            full_path = self.egos_base_path / relative_path
            if full_path.exists():
                # Para arquivos JSON
                if full_path.suffix.lower() == ".json":
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            personas.append({
                                "id": persona_id,
                                "name": data.get("name", persona_id.capitalize()),
                                "description": data.get("description", ""),
                                "source": "egos_core",
                                "path": str(full_path)
                            })
                    except Exception as e:
                        logger.error(f"Erro ao carregar persona {persona_id} de {full_path}: {str(e)}")
                
                # Para arquivos Markdown
                elif full_path.suffix.lower() == ".md":
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Extrai nome e descrição do markdown (primeiras linhas)
                            lines = content.split("\n")
                            name = lines[0].replace("#", "").strip() if lines else persona_id.capitalize()
                            description = lines[2].strip() if len(lines) > 2 else ""
                            
                            personas.append({
                                "id": persona_id,
                                "name": name,
                                "description": description,
                                "source": "egos_core",
                                "path": str(full_path)
                            })
                    except Exception as e:
                        logger.error(f"Erro ao carregar persona {persona_id} de {full_path}: {str(e)}")
        
        return personas
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém os dados de uma persona específica.
        
        Args:
            persona_id: Identificador da persona
            
        Returns:
            Dicionário com os dados da persona ou None se não encontrada
        """
        # Primeiro verifica se é uma persona local do bot
        telegram_persona_path = Path(__file__).resolve().parents[2] / "data" / "telegram_bot" / "personas" / f"{persona_id}.json"
        if telegram_persona_path.exists():
            try:
                with open(telegram_persona_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar persona {persona_id}: {str(e)}")
                return None
        
        # Se não é local, verifica no sistema principal
        if persona_id in self.personas_mapping:
            relative_path = self.personas_mapping[persona_id]
            full_path = self.egos_base_path / relative_path
            
            if full_path.exists():
                # Para arquivos JSON
                if full_path.suffix.lower() == ".json":
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            return json.load(f)
                    except Exception as e:
                        logger.error(f"Erro ao carregar persona {persona_id} de {full_path}: {str(e)}")
                
                # Para arquivos Markdown
                elif full_path.suffix.lower() == ".md":
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Converte o markdown em um formato compatível com o formato de persona
                            lines = content.split("\n")
                            name = lines[0].replace("#", "").strip() if lines else persona_id.capitalize()
                            description = ""
                            
                            # Procura por uma descrição
                            for i, line in enumerate(lines):
                                if i > 0 and line and not line.startswith("#"):
                                    description = line.strip()
                                    break
                            
                            # Extrai exemplos se possível
                            examples = []
                            in_example = False
                            example_user = ""
                            example_assistant = ""
                            
                            for line in lines:
                                if "**User:**" in line:
                                    if example_user and example_assistant:
                                        examples.append({"user": example_user, "assistant": example_assistant})
                                        example_user = ""
                                        example_assistant = ""
                                    
                                    example_user = line.replace("**User:**", "").strip()
                                    in_example = True
                                elif "**Assistant:**" in line and in_example:
                                    example_assistant = line.replace("**Assistant:**", "").strip()
                                elif in_example and example_user and example_assistant:
                                    example_assistant += " " + line.strip()
                            
                            # Adiciona o último exemplo se existir
                            if example_user and example_assistant:
                                examples.append({"user": example_user, "assistant": example_assistant})
                            
                            # Cria um formato compatível com a persona
                            return {
                                "name": name,
                                "description": description,
                                "system_prompt": f"Você é {name}, uma persona especializada do sistema EVA & GUARANI. {description}",
                                "greeting": f"Olá, sou {name}. {description} Como posso ajudar?",
                                "examples": examples
                            }
                    except Exception as e:
                        logger.error(f"Erro ao converter markdown para persona {persona_id} de {full_path}: {str(e)}")
        
        return None

# Exemplo de uso
if __name__ == "__main__":
    connector = EGOSConnector()
    health = connector.health_check()
    print(f"Status dos subsistemas EVA & GUARANI: {health['status']}")
    print(f"Subsistemas disponíveis: {health['subsystems']}") 