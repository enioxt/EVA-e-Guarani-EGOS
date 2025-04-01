#!/usr/bin/env python3
"""
MCP MANAGER - Model Context Protocol para EVA & GUARANI
========================================================================

Sistema para preservação de contexto em sessões do Cursor usando
Model Context Protocols (MCPs).

Funcionalidades:
- Criação, armazenamento e carregamento de MCPs
- Verificação de tamanho de contexto
- Suporte a restauração após resets do Cursor
- Compactação inteligente de contexto
========================================================================
"""

import os
import sys
import json
import datetime
import hashlib
import time
import shutil
from pathlib import Path

# Configurações
MCP_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "BIOS-Q", "mcp")
ACTIVE_DIR = os.path.join(MCP_ROOT, "active")
ARCHIVE_DIR = os.path.join(MCP_ROOT, "archive")
TEMPLATE_DIR = os.path.join(MCP_ROOT, "templates")

# Garantir que os diretórios existam
for dir_path in [MCP_ROOT, ACTIVE_DIR, ARCHIVE_DIR, TEMPLATE_DIR]:
    os.makedirs(dir_path, exist_ok=True)

class MCPProtocol:
    """
    Implementação do Model Context Protocol para preservação de contexto no Cursor
    """
    
    def __init__(self, session_id=None, topic=None):
        """Inicializa um novo MCP ou carrega um existente"""
        self.session_id = session_id or self._generate_session_id()
        self.topic = topic or "Sessão EVA & GUARANI"
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = self.created_at
        self.context_size = 0
        self.message_count = 0
        self.key_concepts = []
        self.entities = {}
        self.summaries = []
        self.status = "active"
        self.version = "1.0"
        self.related_mcps = []
        self.metadata = {
            "system": "EVA & GUARANI",
            "subsystem": "BIOS-Q",
            "encoding_version": "1.0"
        }
        
    def _generate_session_id(self):
        """Gera um ID único para a sessão"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"mcp_{timestamp}_{random_suffix}"
    
    def update_from_conversation(self, conversation_text, summary=None):
        """Atualiza o MCP com informações da conversa atual"""
        # Atualizações básicas
        self.updated_at = datetime.datetime.now().isoformat()
        self.context_size = len(conversation_text)
        self.message_count += 1
        
        # Extrair conceitos-chave
        # Em uma implementação real, usaríamos NLP para extrair conceitos
        # Aqui usamos uma simplificação
        words = conversation_text.split()
        unique_words = set(word.lower() for word in words if len(word) > 5)
        potential_concepts = list(unique_words)[:10]  # Simplificado
        for concept in potential_concepts:
            if concept not in self.key_concepts and len(self.key_concepts) < 20:
                self.key_concepts.append(concept)
                
        # Adicionar resumo se fornecido
        if summary:
            self.summaries.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "content": summary,
                "token_count": len(summary.split())
            })
    
    def save(self, path=None):
        """Salva o MCP no formato JSON"""
        if not path:
            path = os.path.join(ACTIVE_DIR, f"{self.session_id}.json")
            
        # Converter para JSON
        mcp_data = self.to_dict()
        
        # Salvar arquivo
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(mcp_data, f, indent=2)
            
        return path
    
    def to_dict(self):
        """Converte o MCP para dicionário"""
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "context_size": self.context_size,
            "message_count": self.message_count,
            "key_concepts": self.key_concepts,
            "entities": self.entities,
            "summaries": self.summaries,
            "status": self.status,
            "version": self.version,
            "related_mcps": self.related_mcps,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um MCP a partir de um dicionário"""
        mcp = cls(session_id=data.get("session_id"))
        mcp.topic = data.get("topic", mcp.topic)
        mcp.created_at = data.get("created_at", mcp.created_at)
        mcp.updated_at = data.get("updated_at", mcp.updated_at)
        mcp.context_size = data.get("context_size", 0)
        mcp.message_count = data.get("message_count", 0)
        mcp.key_concepts = data.get("key_concepts", [])
        mcp.entities = data.get("entities", {})
        mcp.summaries = data.get("summaries", [])
        mcp.status = data.get("status", "active")
        mcp.version = data.get("version", "1.0")
        mcp.related_mcps = data.get("related_mcps", [])
        mcp.metadata = data.get("metadata", {})
        return mcp
    
    @classmethod
    def load(cls, path):
        """Carrega um MCP a partir de um arquivo"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_cursor_format(self):
        """Converte o MCP para um formato que pode ser incluído numa conversa do Cursor"""
        # Criar uma versão compacta para incluir no prompt
        compact_version = {
            "mcp_id": self.session_id,
            "version": self.version,
            "topic": self.topic,
            "updated": self.updated_at,
            "concepts": self.key_concepts,
            "summary": self.summaries[-1]["content"] if self.summaries else "Sem resumo disponível"
        }
        
        # Formato para incluir na conversa
        cursor_format = (
            "<!-- MCP:START -->\n"
            f"```json\n{json.dumps(compact_version, indent=2)}\n```\n"
            "<!-- MCP:END -->\n\n"
            "O MCP acima contém o contexto compactado desta conversa. "
            "Por favor, mantenha-o e use-o para preservar o contexto em caso de reset."
        )
        
        return cursor_format
        
class MCPManager:
    """
    Gerencia MCPs para sessões do Cursor
    """
    
    @staticmethod
    def create_new_mcp(topic=None):
        """Cria um novo MCP"""
        mcp = MCPProtocol(topic=topic)
        file_path = mcp.save()
        return mcp, file_path
    
    @staticmethod
    def get_latest_mcp():
        """Recupera o MCP mais recente"""
        if not os.path.exists(ACTIVE_DIR):
            return None
            
        mcp_files = [f for f in os.listdir(ACTIVE_DIR) if f.endswith('.json')]
        if not mcp_files:
            return None
            
        # Ordenar por data de modificação (mais recente primeiro)
        mcp_files.sort(key=lambda f: os.path.getmtime(os.path.join(ACTIVE_DIR, f)), reverse=True)
        
        # Carregar o mais recente
        latest_path = os.path.join(ACTIVE_DIR, mcp_files[0])
        return MCPProtocol.load(latest_path)
    
    @staticmethod
    def archive_mcp(mcp):
        """Arquiva um MCP (move de active para archive)"""
        source_path = os.path.join(ACTIVE_DIR, f"{mcp.session_id}.json")
        if not os.path.exists(source_path):
            source_path = mcp.save()
            
        # Atualizar status
        mcp.status = "archived"
        mcp.save(source_path)
        
        # Mover para arquivo
        dest_path = os.path.join(ARCHIVE_DIR, f"{mcp.session_id}.json")
        shutil.move(source_path, dest_path)
        
        return dest_path
    
    @staticmethod
    def get_mcp_by_id(session_id):
        """Recupera um MCP específico pelo ID"""
        # Verificar em active
        active_path = os.path.join(ACTIVE_DIR, f"{session_id}.json")
        if os.path.exists(active_path):
            return MCPProtocol.load(active_path)
            
        # Verificar em archive
        archive_path = os.path.join(ARCHIVE_DIR, f"{session_id}.json")
        if os.path.exists(archive_path):
            return MCPProtocol.load(archive_path)
            
        return None
    
    @staticmethod
    def get_mcp_summary(mcp=None):
        """Gera um resumo de um MCP"""
        if not mcp:
            mcp = MCPManager.get_latest_mcp()
            if not mcp:
                return "Nenhum contexto anterior disponível."
        
        # Pegar o resumo mais recente
        if mcp.summaries:
            latest_summary = mcp.summaries[-1]["content"]
        else:
            latest_summary = "Sem resumo disponível."
            
        # Formatar mensagem
        return (
            f"Contexto da sessão anterior (MCP: {mcp.session_id}):\n\n"
            f"Tópico: {mcp.topic}\n"
            f"Última atualização: {mcp.updated_at}\n"
            f"Conceitos-chave: {', '.join(mcp.key_concepts[:5])}...\n\n"
            f"Resumo:\n{latest_summary}"
        )

# Funções para serem chamadas diretamente do Cursor

def save_current_mcp(conversation_text, topic=None, summary=None):
    """
    Salva o contexto atual em um MCP
    """
    # Buscar MCP existente ou criar novo
    mcp = MCPManager.get_latest_mcp()
    if not mcp or mcp.status != "active":
        mcp, _ = MCPManager.create_new_mcp(topic)
    
    # Atualizar com a conversa atual
    mcp.update_from_conversation(conversation_text, summary)
    
    # Salvar
    mcp_path = mcp.save()
    
    return {
        "status": "success",
        "message": f"MCP atualizado e salvo em {mcp_path}",
        "mcp_id": mcp.session_id,
        "cursor_format": mcp.to_cursor_format()
    }

def load_latest_mcp():
    """
    Carrega o MCP mais recente
    """
    mcp = MCPManager.get_latest_mcp()
    if not mcp:
        return {
            "status": "error",
            "message": "Nenhum MCP encontrado."
        }
    
    return {
        "status": "success",
        "message": f"MCP {mcp.session_id} carregado com sucesso.",
        "mcp_id": mcp.session_id,
        "cursor_format": mcp.to_cursor_format(),
        "summary": MCPManager.get_mcp_summary(mcp)
    }

def cmd_save_mcp(conversation_text=None, topic=None, summary=None):
    """Comando para salvar MCP a partir do Cursor"""
    if not conversation_text:
        # Estamos em uma situação onde o texto da conversa não foi fornecido
        # Em um caso real, precisaríamos buscar o texto da conversa
        return {
            "status": "error",
            "message": "Texto da conversa não fornecido.",
            "help": "Use !save_mcp com o texto da conversa atual."
        }
    
    result = save_current_mcp(conversation_text, topic, summary)
    
    # Resposta formatada para o Cursor
    response = (
        f"✅ MCP salvo com sucesso!\n\n"
        f"ID: {result['mcp_id']}\n"
        f"Status: {result['status']}\n\n"
        f"Para restaurar este contexto no futuro, use o comando:\n"
        f"`!load_mcp {result['mcp_id']}`\n\n"
        f"Para continuar a fazer atualizações automáticas do MCP, "
        f"simplesmente responda a esta mensagem normalmente."
    )
    
    return {
        "display": response,
        "mcp": result
    }

def cmd_load_mcp(mcp_id=None):
    """Comando para carregar MCP a partir do Cursor"""
    # Se um ID específico for passado, carregue esse MCP
    if mcp_id:
        mcp = MCPManager.get_mcp_by_id(mcp_id)
        if not mcp:
            return {
                "display": f"❌ MCP com ID '{mcp_id}' não encontrado.",
                "status": "error"
            }
    else:
        # Caso contrário, carregue o mais recente
        result = load_latest_mcp()
        if result["status"] == "error":
            return {
                "display": f"❌ {result['message']}",
                "status": "error"
            }
        
        mcp = MCPManager.get_mcp_by_id(result["mcp_id"])
    
    # Formatar resposta para o Cursor
    response = (
        f"✅ MCP carregado com sucesso!\n\n"
        f"{MCPManager.get_mcp_summary(mcp)}\n\n"
        f"ID do MCP: {mcp.session_id}\n"
        f"Número de mensagens: {mcp.message_count}\n"
        f"Tamanho do contexto: {mcp.context_size} caracteres\n\n"
        f"Para continuar com este contexto, simplesmente responda a esta mensagem normalmente."
    )
    
    return {
        "display": response,
        "mcp": mcp.to_dict(),
        "cursor_format": mcp.to_cursor_format()
    }

def cmd_help():
    """Mostra ajuda para os comandos MCP"""
    help_text = """
## Comandos MCP para Preservação de Contexto

Para preservar seu contexto no Cursor, use:

- `!save_mcp` - Salva o contexto atual como um MCP
- `!load_mcp` - Carrega o MCP mais recente
- `!load_mcp <id>` - Carrega um MCP específico pelo ID
- `!mcp_status` - Mostra status do MCP atual
- `!mcp_help` - Mostra esta ajuda

Os MCPs (Model Context Protocols) permitem que você preserve o contexto
entre sessões diferentes do Cursor, evitando a perda de informações
quando a conversa fica muito longa ou quando o chat é resetado.
"""
    return {
        "display": help_text
    }

def prompt_for_mcp_save():
    """Gera um prompt para salvar MCP quando a conversa estiver ficando longa"""
    prompt = """
🔄 **Atenção: Conversa Longa Detectada**

A conversa atual está se aproximando do limite de tokens do Cursor.
É recomendável salvar um MCP (Model Context Protocol) agora para evitar perda de contexto.

**Opções:**
1. Digite `!save_mcp` para salvar o contexto atual
2. Para continuar sem salvar, basta ignorar esta mensagem
"""
    return prompt

def main():
    """Função principal para testes"""
    print("\n✧༺❀༻∞ EVA & GUARANI - MCP Manager ∞༺❀༻✧\n")
    
    # Testar criação de MCP
    mcp, path = MCPManager.create_new_mcp("Teste de MCP")
    print(f"MCP criado em: {path}")
    
    # Testar atualização
    mcp.update_from_conversation("Este é um teste do sistema de MCP para o EVA & GUARANI.", 
                                "Teste inicial do sistema MCP.")
    mcp.save()
    
    # Testar carregamento
    loaded = MCPManager.get_latest_mcp()
    print(f"MCP carregado: {loaded.session_id}")
    print(f"Tópico: {loaded.topic}")
    print(f"Tamanho do contexto: {loaded.context_size}")
    
    # Mostrar formato para o Cursor
    print("\nFormato para o Cursor:")
    print(loaded.to_cursor_format())
    
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

if __name__ == "__main__":
    main()