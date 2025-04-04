#!/usr/bin/env python3
# tools/mcp/mcp_restore.py
import os
import json
import datetime
import glob
from pathlib import Path


class MCPRestore:
    """Sistema de restauração de contexto do BIOS-Q para o Cursor"""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.context_dir = self.project_root / "CHATS" / "cursor_context"

    def get_latest_context(self):
        """Obtém o arquivo de contexto mais recente"""
        files = list(self.context_dir.glob("session_*.json"))
        if not files:
            return None

        # Ordena por data de modificação (mais recente primeiro)
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        return latest_file

    def load_context(self, filepath=None):
        """Carrega o contexto de um arquivo específico ou o mais recente"""
        if filepath is None:
            filepath = self.get_latest_context()
            if filepath is None:
                print("Nenhum arquivo de contexto encontrado.")
                return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                context = json.load(f)
                print(f"Contexto carregado de: {filepath}")
                return context
        except Exception as e:
            print(f"Erro ao carregar contexto: {e}")
            return None

    def create_summary(self, context):
        """Cria um resumo do contexto para ser usado no início de uma nova conversa"""
        if not context:
            return "Nenhum contexto disponível."

        # Formata um resumo estruturado e conciso para o ambiente Cursor
        timestamp = context.get("timestamp", "desconhecido")
        try:
            # Converte ISO para formato legível
            dt = datetime.datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            formatted_time = timestamp

        summary = [
            "# [CURSOR] Contexto Restaurado via MCP\n",
            f"📅 **Data**: {formatted_time}",
        ]

        # Adiciona módulos de forma concisa
        modules = context.get("modules_discussed", [])
        if modules:
            module_names = [f"`{m['name']}`" for m in modules]
            summary.append(f"\n**Módulos**: {', '.join(module_names)}")

        # Conceitos-chave (limitado aos 5 principais)
        key_concepts = context.get("key_concepts", {})
        if key_concepts:
            concepts = list(key_concepts.keys())[:5]
            summary.append(f"\n**Conceitos**: {', '.join(concepts)}")

        # Relacionamentos importantes (limitado aos 3 principais)
        relationships = context.get("relationships", [])
        if relationships:
            rel_summary = []
            for i, rel in enumerate(relationships[:3]):
                rel_summary.append(f"{rel['source']} {rel['type']} {rel['target']}")
            if rel_summary:
                summary.append(f"\n**Conexões**: {'; '.join(rel_summary)}")

        # Resumo da conversa
        conversation_summary = context.get("conversation_summary", "")
        if conversation_summary:
            summary.append("\n## Resumo da Conversa\n")
            # Limita o tamanho do resumo
            if len(conversation_summary) > 500:
                summary.append(conversation_summary[:500] + "...")
            else:
                summary.append(conversation_summary)

        # Se não houver resumo, mas houver o texto completo
        elif context.get("conversation_full"):
            summary.append("\n## Tópicos da Conversa\n")
            # Extrai apenas alguns tópicos do texto completo (últimas 50 palavras)
            words = context.get("conversation_full", "").split()
            if len(words) > 50:
                summary.append("- Discussão sobre: " + " ".join(words[-50:]) + "...")

        return "\n".join(summary)


# Função para ser chamada pelo comando !load_mcp
def load_context_summary():
    """Carrega e formata o resumo do contexto mais recente"""
    mcp = MCPRestore()
    context = mcp.load_context()

    if context:
        summary = mcp.create_summary(context)
        return summary
    else:
        return "# [CURSOR] Falha ao Carregar Contexto\n\n❌ Não foi possível encontrar um contexto salvo anteriormente."


if __name__ == "__main__":
    summary = load_context_summary()
    print(summary)
