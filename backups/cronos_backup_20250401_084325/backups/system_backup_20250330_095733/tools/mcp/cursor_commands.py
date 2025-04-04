#!/usr/bin/env python3
"""
MCP - Comandos específicos para o ambiente Cursor
=================================================

Este módulo implementa os comandos de interação direta com o Cursor
para salvar e carregar contexto sem necessidade de selecionar todo o texto.

Comandos principais:
- !save_mcp: Salva o contexto atual
- !load_mcp: Carrega o contexto mais recente
"""

import os
import sys
import json
import datetime
from pathlib import Path

# Adiciona o diretório pai ao caminho de busca
sys.path.append(str(Path(__file__).resolve().parent))

# Importa módulos MCP
from mcp_capture import save_cursor_context
from mcp_restore import load_context_summary

# Importa o monitor de contexto
try:
    from context_monitor import (
        start_monitoring,
        get_status,
        add_message,
        force_save,
        register_limit_reached,
    )

    MONITOR_AVAILABLE = True
except ImportError:
    MONITOR_AVAILABLE = False

# Mapeamento de comandos
COMMANDS = {
    "!save_mcp": "save_mcp",
    "!load_mcp": "load_mcp",
    "!mcp_help": "show_help",
    "!mcp_list": "list_contexts",
    "save_mcp": "save_mcp",  # Adicionando sem o ! para facilitar
    "load_mcp": "load_mcp",  # Adicionando sem o ! para facilitar
    "mcp_help": "show_help",  # Adicionando sem o ! para facilitar
    "mcp_list": "list_contexts",  # Adicionando sem o ! para facilitar
    "@save": "show_save_command",  # Comandos simplificados para o chat
    "@load": "show_load_command",  # Comandos simplificados para o chat
    "@list": "show_list_command",  # Comandos simplificados para o chat
    "!mcp_status": "show_monitor_status",
    "mcp_status": "show_monitor_status",
    "@status": "show_monitor_status",
    "!update_limit": "update_context_limit",
    "update_limit": "update_context_limit",
    "@update": "show_update_limit_command",
}


def process_command(command, args=None):
    """Processa um comando MCP do Cursor"""
    cmd = command.lower()

    if cmd in COMMANDS:
        function_name = COMMANDS[cmd]
        try:
            # Chama a função com args se necessário
            if args:
                globals()[function_name](args)
            else:
                globals()[function_name]()
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            show_help()
    else:
        show_help()


def save_mcp(args=None):
    """Salva o contexto atual no MCP"""
    # Cria um resumo da conversa atual baseado no que o assistente sabe
    current_conversation = create_conversation_summary()

    # Registra a mensagem no monitor se disponível
    if MONITOR_AVAILABLE:
        add_message(current_conversation)

    # Salva usando o capturador
    result = save_cursor_context(current_conversation)

    # Retorna um formato amigável para o Cursor
    print("\n# [CURSOR] Contexto Salvo via MCP\n")
    print(f"✅ **Contexto salvo com sucesso!**\n")
    print(f"📂 Arquivo: {result['filepath']}")
    print(f"⏱️ Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Resume os módulos capturados
    summarize_captured_modules(result["filepath"])

    # Exibe informações do monitor se disponível
    if MONITOR_AVAILABLE:
        status = get_status()
        print(f"\n## Status do Monitor:\n")
        print(f"📊 Capacidade utilizada: {status['capacity_used']*100:.1f}%")
        print(f"📝 Mensagens registradas: {status['message_count']}")
        if status["capacity_used"] >= 0.8:
            print(f"\n⚠️ **Atenção**: Contexto acima de 80% da capacidade!")
            print(f"   Salvamento automático ativado.")


def load_mcp(args=None):
    """Carrega o contexto mais recente do MCP"""
    summary = load_context_summary()

    if summary:
        print("\n# [CURSOR] Contexto Carregado via MCP\n")
        print(summary)
    else:
        print("\n# [CURSOR] Falha ao Carregar Contexto\n")
        print("❌ Não foi possível encontrar um contexto salvo anteriormente.")
        print("Por favor, utilize !save_mcp primeiro para salvar um contexto.")


def show_help():
    """Exibe ajuda sobre comandos MCP"""
    help_text = """
# [CURSOR] Comandos MCP Disponíveis

Use estes comandos para gerenciar o contexto da conversa no Cursor:

- `!save_mcp` - Salva o contexto atual da conversa
- `!load_mcp` - Carrega o contexto mais recente
- `!mcp_list` - Lista todos os contextos salvos
- `!mcp_help` - Exibe esta ajuda
- `!mcp_status` - Exibe o status do monitor de contexto

O sistema MCP (Memory Context Preservation) permite salvar e restaurar
o contexto da conversa sem precisar selecionar todo o texto.

O monitor de contexto está ativado e salvará automaticamente quando atingir 80%
da capacidade estimada ou a cada 30 minutos para evitar perda de dados.
    """
    print(help_text)


def list_contexts(args=None):
    """Lista todos os contextos salvos"""
    # Encontra o diretório de contexto
    project_root = Path(__file__).resolve().parents[2]
    context_dir = project_root / "CHATS" / "cursor_context"

    if not context_dir.exists():
        print("\n# [CURSOR] Nenhum Contexto Encontrado\n")
        print("❌ O diretório de contextos não existe.")
        return

    # Lista todos os arquivos de contexto
    context_files = list(context_dir.glob("session_*.json"))

    if not context_files:
        print("\n# [CURSOR] Nenhum Contexto Encontrado\n")
        print("❌ Não há contextos salvos.")
        return

    # Ordena por data de modificação (mais recente primeiro)
    context_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    print("\n# [CURSOR] Contextos Salvos\n")
    for i, file in enumerate(context_files[:10], 1):  # Limita a 10 contextos
        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        print(f"{i}. **{file.name}** - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def create_conversation_summary():
    """Cria um resumo da conversa atual baseado no que o assistente sabe"""
    summary = """
Conversa sobre o sistema MCP (Memory Context Preservation) no EVA & GUARANI EGOS:

- Discussão sobre limitações do ambiente Cursor e seleção de texto via Ctrl+A
- Desenvolvimento e otimização do sistema MCP para funcionar sem Ctrl+A
- Criação/atualização de arquivos:
  - tools/mcp/mcp_capture.py - captura de contexto sem depender de Ctrl+A
  - tools/mcp/mcp_restore.py - restauração do contexto em formato otimizado
  - tools/mcp/cursor_commands.py - comandos para executar MCP diretamente no Cursor
  - tools/mcp/save_mcp.bat e load_mcp.bat - scripts para execução no Windows

- Discussão sobre requisitos para preservação de contexto no ambiente Cursor
- Integração com o sistema BIOS-Q
- Fluxo de trabalho para salvar contexto:
  1. Receber o comando !save_mcp
  2. Capturar informações da conversa atual
  3. Extrair módulos e conceitos-chave
  4. Salvar em JSON para uso posterior

- Módulos relacionados: ETHIK, ATLAS, NEXUS, CRONOS, BIOS-Q, mycelium
- Integração com projetos: avatechartbot (bot Telegram)
    """
    return summary


def summarize_captured_modules(filepath):
    """Resume os módulos capturados no contexto"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            context = json.load(f)

        if not context.get("modules_discussed"):
            print("\n**Nenhum módulo específico capturado.**")
            return

        print("\n## Módulos Capturados:\n")
        for module in context["modules_discussed"]:
            print(f"- **{module['name']}**: {module.get('description', '')}")
    except:
        print("\n**Não foi possível resumir os módulos capturados.**")


def show_save_command(args=None):
    """Mostra o comando para salvar contexto"""
    print("\n# [CURSOR] Comando para Salvar Contexto MCP")
    print("\nExecute no terminal:")
    print("```")
    print("cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py save_mcp")
    print("```")
    print("\nOu abra o explorador de arquivos e execute o script:")
    print("```")
    print("C:\\Eva & Guarani - EGOS\\tools\\mcp\\save.bat")
    print("```")


def show_load_command(args=None):
    """Mostra o comando para carregar contexto"""
    print("\n# [CURSOR] Comando para Carregar Contexto MCP")
    print("\nExecute no terminal:")
    print("```")
    print("cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py load_mcp")
    print("```")
    print("\nOu abra o explorador de arquivos e execute o script:")
    print("```")
    print("C:\\Eva & Guarani - EGOS\\tools\\mcp\\load.bat")
    print("```")


def show_list_command(args=None):
    """Mostra o comando para listar contextos"""
    print("\n# [CURSOR] Comando para Listar Contextos MCP")
    print("\nExecute no terminal:")
    print("```")
    print("cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py mcp_list")
    print("```")


def show_monitor_status(args=None):
    """Exibe o status atual do monitor de contexto"""
    if not MONITOR_AVAILABLE:
        print("\n# [CURSOR] Monitor de Contexto não disponível\n")
        print("❌ O módulo de monitoramento não está disponível.")
        return

    status = get_status()

    print("\n# [CURSOR] Status do Monitor de Contexto\n")
    print(f"📊 **Capacidade utilizada**: {status['capacity_used']*100:.1f}%")
    print(f"📝 **Mensagens registradas**: {status['message_count']}")
    print(f"📏 **Tamanho estimado**: {status['current_size']} caracteres")
    print(
        f"📏 **Limite atual**: {status['context_limit']} caracteres (fonte: {status['context_source']})"
    )
    print(
        f"⏱️ **Último salvamento**: {datetime.datetime.fromtimestamp(status['last_save_time']).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"🔄 **Monitoramento ativo**: {status['running']}")

    # Aviso de capacidade
    if status["capacity_used"] >= 0.8:
        print(f"\n⚠️ **Atenção**: Contexto acima de 80% da capacidade!")
        print(f"   Salvamento automático ativado.")
    elif status["capacity_used"] >= 0.7:
        print(f"\n⚠️ **Aviso**: Contexto se aproximando de 80% da capacidade.")
        print(f"   Considere salvar em breve.")


def update_context_limit(args=None):
    """Atualiza o limite de contexto com o tamanho atual quando o Cursor solicita novo chat"""
    if not MONITOR_AVAILABLE:
        print("\n# [CURSOR] Monitor de Contexto não disponível\n")
        print("❌ O módulo de monitoramento não está disponível.")
        return

    status = get_status()
    current_size = status["current_size"]

    if args and len(args) > 0:
        try:
            # Se um valor explícito foi fornecido, use-o
            current_size = int(args[0])
        except ValueError:
            print(f"⚠️ Valor inválido: {args[0]}")
            print("Usando o tamanho atual como referência")

    # Registra o limite atingido
    result = register_limit_reached(current_size)

    print("\n# [CURSOR] Limite de Contexto Atualizado\n")
    print(f"✅ **Limite atualizado com base em dados empíricos**\n")
    print(f"📏 Limite anterior: {result['old_limit']} caracteres")
    print(f"📏 Novo limite: {result['new_limit']} caracteres (90% do máximo real)")
    print(f"📊 Capacidade agora: {result['new_capacity']*100:.1f}%")
    print("\nEsta informação foi salva no BIOS-Q e será usada em todas as sessões futuras.")
    print("O sistema se adaptará automaticamente a futuros ajustes de limite.")

    if result["new_capacity"] >= 0.8:
        print("\n⚠️ **Atenção**: Com o novo limite, você já está acima de 80% da capacidade!")
        print("Recomendamos iniciar um novo chat em breve.")


def show_update_limit_command(args=None):
    """Mostra o comando para atualizar o limite de contexto"""
    print("\n# [CURSOR] Comando para Atualizar Limite de Contexto")
    print("\nSe o Cursor solicitou um novo chat, execute no terminal:")
    print("```")
    print(
        "cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py update_limit"
    )
    print("```")
    print("\nIsso ajustará automaticamente o limite com base no tamanho real do contexto atual.")


# Inicia o monitoramento automaticamente
if MONITOR_AVAILABLE:
    try:
        start_monitoring()
        print("[MCP] Monitor de contexto iniciado. Salvamento automático a 80% ativado.")
    except Exception as e:
        print(f"[MCP] Erro ao iniciar o monitor: {e}")

if __name__ == "__main__":
    # Processa comandos da linha de comando
    if len(sys.argv) > 1:
        command = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else None
        process_command(command, args)
    else:
        show_help()
