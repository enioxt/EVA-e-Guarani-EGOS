#!/usr/bin/env python3
# tools/mcp/mcp_capture.py
import os
import json
import datetime
import re
from pathlib import Path

class MCPCapture:
    """Sistema de captura de contexto completo do Cursor para BIOS-Q"""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]  # Raiz do projeto
        self.context_dir = self.project_root / "CHATS" / "cursor_context"
        self.context_dir.mkdir(parents=True, exist_ok=True)
        
        # Estrutura para armazenamento do contexto
        self.context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "environment": "Cursor + Claude 3.7 Sonnet",
            "project": "EVA & GUARANI - EGOS",
            "modules_discussed": [],
            "conversation_full": "",
            "conversation_summary": "",
            "key_concepts": {},
            "action_items": [],
            "relationships": []
        }
    
    def manual_capture(self, conversation_summary):
        """Captura manual do contexto da conversa via resumo"""
        # Usa um resumo fornecido pelo assistente como alternativa ao copiar/colar
        self.context["conversation_summary"] = conversation_summary
        return True
            
    def add_module(self, module_name, description=""):
        """Adiciona um módulo à lista de módulos discutidos"""
        # Verifica se o módulo já foi adicionado para evitar duplicação
        for module in self.context["modules_discussed"]:
            if module["name"].lower() == module_name.lower():
                return
                
        self.context["modules_discussed"].append({
            "name": module_name,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def add_concept(self, concept_name, details):
        """Adiciona um conceito-chave ao contexto"""
        self.context["key_concepts"][concept_name] = {
            "details": details,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def add_relationship(self, source, target, relationship_type):
        """Adiciona um relacionamento entre componentes/conceitos"""
        self.context["relationships"].append({
            "source": source,
            "target": target,
            "type": relationship_type,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def save_context(self):
        """Salva o contexto em arquivo JSON"""
        filename = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.context_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
        
        print(f"Contexto completo salvo em: {filepath}")
        return filepath
    
    def auto_extract_modules(self, text=None):
        """Extrai automaticamente módulos mencionados na conversa"""
        # Lista de módulos conhecidos do EVA & GUARANI
        known_modules = {
            "ETHIK": "Sistema de Ética para EVA & GUARANI",
            "CRONOS": "Sistema de Preservação Evolutiva",
            "NEXUS": "Sistema de Análise Modular",
            "ATLAS": "Sistema de Cartografia Sistêmica",
            "BIOS-Q": "Sistema de Inicialização Quântica",
            "mycelium": "Sistema de análise de conexões",
            "MCP": "Memory Context Preservation",
            "tradutor": "Sistema de tradução interlínguas",
            "blockchain": "Sistema de registro imutável",
            "personas": "Sistema de variação contextual",
            "avatechartbot": "Bot de Telegram integrado",
            "quantum_prompts": "Prompts de alta complexidade"
        }
        
        # Texto para análise (resumo)
        analysis_text = text or self.context["conversation_summary"]
        
        # Busca por esses módulos na conversa
        if analysis_text:
            for module, description in known_modules.items():
                if module.lower() in analysis_text.lower():
                    self.add_module(module, description)

# Função para salvar contexto diretamente no Cursor via comando !save_mcp
def save_cursor_context(conversation_summary=None):
    """Salva o contexto diretamente no Cursor sem clipboard"""
    mcp = MCPCapture()
    
    # Usa o resumo fornecido
    if conversation_summary:
        mcp.manual_capture(conversation_summary)
    
    # Adiciona módulos principais do EVA & GUARANI sempre
    core_modules = {
        "ETHIK": "Sistema de Ética para EVA & GUARANI",
        "CRONOS": "Sistema de Preservação Evolutiva",
        "NEXUS": "Sistema de Análise Modular", 
        "ATLAS": "Sistema de Cartografia Sistêmica",
        "BIOS-Q": "Sistema de Inicialização Quântica",
        "mycelium": "Sistema de análise de conexões",
        "MCP": "Memory Context Preservation"
    }
    
    for module, desc in core_modules.items():
        mcp.add_module(module, desc)
    
    # Extrai módulos adicionais do texto
    if conversation_summary:
        mcp.auto_extract_modules(conversation_summary)
    
    # Adiciona relacionamentos fundamentais
    relationships = [
        ("BIOS-Q", "MCP", "contém"),
        ("MCP", "CURSOR", "integra com"),
        ("mycelium", "NEXUS", "analisa"),
        ("ATLAS", "mycelium", "visualiza")
    ]
    
    for src, tgt, rel in relationships:
        mcp.add_relationship(src, tgt, rel)
    
    # Salva o contexto completo
    filepath = mcp.save_context()
    
    return {
        "success": True,
        "filepath": str(filepath),
        "message": "Contexto salvo com sucesso no sistema MCP"
    }

if __name__ == "__main__":
    # Tenta extrair um resumo da linha de comando se fornecido
    import sys
    summary = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    result = save_cursor_context(summary)
    print(f"\nResultado: {result['message']}")
    print(f"Arquivo: {result['filepath']}")