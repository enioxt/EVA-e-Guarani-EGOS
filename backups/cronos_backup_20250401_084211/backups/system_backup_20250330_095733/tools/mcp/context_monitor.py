#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monitor automático de contexto para MCP
Usa limites adaptativos baseados em dados empíricos
"""

import os
import time
import json
import threading
import datetime
import atexit
from pathlib import Path

# Importação de outros módulos MCP
try:
    from mcp_capture import save_cursor_context
except ImportError:
    print("Erro: Não foi possível importar o módulo mcp_capture")

# Configurações padrão
DEFAULT_CONTEXT_LIMIT = 100000  # Valor inicial conservador
SAFE_MARGIN = 0.90  # Usamos 90% do limite real para segurança
CHECK_INTERVAL = 60  # Verifica a cada 60 segundos
AUTO_SAVE_INTERVAL = 30 * 60  # Salva automaticamente a cada 30 minutos
MONITOR_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor_data.json")
CONTEXT_LIMITS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "BIOS-Q", "context_limits.json"
)

# Estado global
monitor_state = {
    "running": False,
    "messages": [],
    "current_size": 0,
    "message_count": 0,
    "capacity_used": 0.0,
    "last_check_time": time.time(),
    "last_save_time": time.time(),
    "threshold_reached": False,
    "context_limit": DEFAULT_CONTEXT_LIMIT,
    "context_source": "default",
}

# Lock para acesso concorrente
state_lock = threading.RLock()


def load_context_limits():
    """Carrega os limites de contexto do BIOS-Q"""
    try:
        # Certifica-se de que o diretório BIOS-Q existe
        bios_q_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIOS-Q")
        os.makedirs(bios_q_dir, exist_ok=True)

        if os.path.exists(CONTEXT_LIMITS_FILE):
            with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                content = content.strip()
                # Trata possíveis caracteres estranhos
                if content.startswith("}"):
                    content = content[1:]
                if not content.startswith("{"):
                    content = "{" + content

                try:
                    # Tenta carregar o JSON
                    limits = json.loads(content)

                    with state_lock:
                        if "cursor" in limits and limits["cursor"].get("measured", False):
                            # Usa o limite medido com margem de segurança
                            print(
                                f"[MCP] Limite empírico encontrado: {limits['cursor']['limit']} (safe: {limits['cursor']['safe_limit']})"
                            )
                            monitor_state["context_limit"] = limits["cursor"]["safe_limit"]
                            monitor_state["context_source"] = "empirical"
                            return True
                except json.JSONDecodeError as e:
                    print(f"[MCP] Erro ao decodificar JSON de limites: {e}")
                    return False
        return False
    except Exception as e:
        print(f"[MCP] Erro ao carregar limites de contexto: {e}")
        return False


def save_context_limits(platform, limit, measured=True):
    """Salva os limites de contexto no BIOS-Q"""
    try:
        # Certifica-se de que o diretório BIOS-Q existe
        bios_q_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "BIOS-Q")
        os.makedirs(bios_q_dir, exist_ok=True)

        # Carrega dados existentes ou cria novo
        limits = {}
        if os.path.exists(CONTEXT_LIMITS_FILE):
            with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
                limits = json.load(f)

        # Atualiza com o novo limite
        limits[platform] = {
            "limit": limit,
            "measured": measured,
            "last_updated": datetime.datetime.now().isoformat(),
            "safe_limit": int(limit * SAFE_MARGIN),
        }

        # Salva de volta
        with open(CONTEXT_LIMITS_FILE, "w", encoding="utf-8") as f:
            json.dump(limits, f, indent=2)

        print(
            f"[MCP] Limite de contexto para {platform} atualizado: {limit} (90% = {int(limit * SAFE_MARGIN)})"
        )
        return True
    except Exception as e:
        print(f"Erro ao salvar limites de contexto: {e}")
        return False


def save_monitor_state():
    """Salva o estado atual do monitor em um arquivo JSON"""
    try:
        with state_lock:
            with open(MONITOR_DATA_FILE, "w", encoding="utf-8") as f:
                # Salvamos apenas os dados essenciais, não todo o conteúdo
                save_data = {
                    "running": monitor_state["running"],
                    "current_size": monitor_state["current_size"],
                    "message_count": monitor_state["message_count"],
                    "capacity_used": monitor_state["capacity_used"],
                    "last_check_time": monitor_state["last_check_time"],
                    "last_save_time": monitor_state["last_save_time"],
                    "threshold_reached": monitor_state["threshold_reached"],
                    "context_limit": monitor_state["context_limit"],
                    "context_source": monitor_state["context_source"],
                }
                json.dump(save_data, f, indent=2)
    except Exception as e:
        print(f"Erro ao salvar estado do monitor: {e}")


def load_monitor_state():
    """Carrega o estado do monitor de um arquivo JSON"""
    try:
        if os.path.exists(MONITOR_DATA_FILE):
            with open(MONITOR_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                with state_lock:
                    for key, value in data.items():
                        if key in monitor_state:
                            monitor_state[key] = value
    except Exception as e:
        print(f"Erro ao carregar estado do monitor: {e}")


def add_message(content):
    """Adiciona uma mensagem ao monitor"""
    with state_lock:
        # Adiciona a mensagem à lista
        monitor_state["messages"].append(content)

        # Atualiza estatísticas
        monitor_state["current_size"] += len(content)
        monitor_state["message_count"] += 1
        monitor_state["capacity_used"] = (
            monitor_state["current_size"] / monitor_state["context_limit"]
        )

        # Salva o estado atual
        save_monitor_state()

        # Retorna True se estiver acima do limite de 80%
        return monitor_state["capacity_used"] >= 0.8


def register_limit_reached(size):
    """
    Registra que o limite foi atingido com um determinado tamanho.
    Deve ser chamada pelo usuário quando o Cursor solicitar um novo chat.
    """
    with state_lock:
        old_limit = monitor_state["context_limit"]
        # Salva o novo limite no BIOS-Q
        save_context_limits("cursor", size)

        # Atualiza o estado atual
        monitor_state["context_limit"] = int(size * SAFE_MARGIN)
        monitor_state["context_source"] = "empirical"
        monitor_state["capacity_used"] = (
            monitor_state["current_size"] / monitor_state["context_limit"]
        )

        # Salva o estado
        save_monitor_state()

        return {
            "old_limit": old_limit,
            "new_limit": monitor_state["context_limit"],
            "new_capacity": monitor_state["capacity_used"],
        }


def force_save():
    """Força um salvamento imediato do contexto"""
    try:
        print(
            f"[MCP Monitor] Executando salvamento forçado às {datetime.datetime.now().strftime('%H:%M:%S')}"
        )

        # Concatena todas as mensagens
        with state_lock:
            all_content = "\n".join(monitor_state["messages"])

        # Adiciona informações de final de contexto para facilitar a transição
        context_info = create_context_transition_info()
        all_content += "\n\n" + context_info

        # Salva no MCP
        result = save_cursor_context(all_content)

        # Atualiza o horário do último salvamento
        with state_lock:
            monitor_state["last_save_time"] = time.time()
            monitor_state["threshold_reached"] = False
            save_monitor_state()

        print(f"[MCP Monitor] Salvamento concluído: {result['filepath']}")
        return result
    except Exception as e:
        print(f"[MCP Monitor] Erro no salvamento forçado: {e}")
        return None


def create_context_transition_info():
    """Cria informações de transição para o final do contexto"""
    with state_lock:
        limite_percentual = monitor_state["capacity_used"] * 100

    info = f"""
## ⚠️ INFORMAÇÕES DE LIMITE DE CONTEXTO ⚠️

O contexto atual está em aproximadamente {limite_percentual:.1f}% do limite máximo seguro.
Se o Cursor solicitar um novo chat, isso indica que o limite real foi atingido.

### 🔄 PARA CONTINUAR NO NOVO CHAT:

1. Copie e execute o comando abaixo para carregar o contexto salvo:
```
cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py load_mcp
```

2. Se o Cursor solicitou um novo chat, informe o sistema para ajustar o limite:
```
cd /c/Eva\\ \\&\\ Guarani\\ -\\ EGOS/tools/mcp && python cursor_commands.py update_limit
```

### 📊 Status do Monitor:
- Mensagens registradas: {monitor_state["message_count"]}
- Caracteres: {monitor_state["current_size"]}
- Fonte do limite: {monitor_state["context_source"]}
"""
    return info


def check_context_size():
    """Verifica o tamanho do contexto e salva se necessário"""
    with state_lock:
        current_time = time.time()
        since_last_save = current_time - monitor_state["last_save_time"]

        # Verifica se atingiu 80% da capacidade
        if monitor_state["capacity_used"] >= 0.8 and not monitor_state["threshold_reached"]:
            print(
                f"[MCP Monitor] Contexto atingiu 80% da capacidade ({monitor_state['capacity_used']*100:.1f}%)"
            )
            monitor_state["threshold_reached"] = True
            threading.Thread(target=force_save).start()

        # Verifica se passou o tempo para salvamento automático (30 minutos)
        elif since_last_save >= AUTO_SAVE_INTERVAL:
            print(f"[MCP Monitor] Salvamento automático após {since_last_save/60:.1f} minutos")
            threading.Thread(target=force_save).start()

        # Atualiza o tempo da última verificação
        monitor_state["last_check_time"] = current_time
        save_monitor_state()


def monitor_thread_func():
    """Função principal do thread de monitoramento"""
    print(f"[MCP Monitor] Iniciado em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        with state_lock:
            monitor_state["running"] = True
            save_monitor_state()

        while True:
            # Verifica o tamanho do contexto
            check_context_size()

            # Aguarda o próximo ciclo
            time.sleep(CHECK_INTERVAL)

            # Verifica se o monitor ainda está rodando
            with state_lock:
                if not monitor_state["running"]:
                    break

    except Exception as e:
        print(f"[MCP Monitor] Erro no thread de monitoramento: {e}")
    finally:
        with state_lock:
            monitor_state["running"] = False
            save_monitor_state()

    print(f"[MCP Monitor] Finalizado em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def stop_monitoring():
    """Para o monitor de contexto"""
    with state_lock:
        monitor_state["running"] = False
        save_monitor_state()
    print("[MCP Monitor] Monitoramento interrompido")


def start_monitoring():
    """Inicia o monitor de contexto"""
    # Carrega os limites de contexto
    limit_loaded = load_context_limits()
    if limit_loaded:
        print(
            f"[MCP Monitor] Usando limite empírico de {monitor_state['context_limit']} caracteres"
        )
    else:
        print(f"[MCP Monitor] Usando limite padrão de {monitor_state['context_limit']} caracteres")

    # Carrega o estado anterior, se existir
    load_monitor_state()

    # Verifica se já está rodando
    with state_lock:
        if monitor_state["running"]:
            print("[MCP Monitor] Já está em execução")
            return

    # Inicia o thread de monitoramento
    monitor_thread = threading.Thread(target=monitor_thread_func, daemon=True)
    monitor_thread.start()

    # Registra a função para parar o monitoramento ao sair
    atexit.register(stop_monitoring)

    print("[MCP Monitor] Monitoramento iniciado")
    print(
        f"[MCP Monitor] Usando limite de {monitor_state['context_limit']} caracteres (fonte: {monitor_state['context_source']})"
    )

    return monitor_thread


def get_status():
    """Retorna o status atual do monitor"""
    with state_lock:
        return {
            "running": monitor_state["running"],
            "current_size": monitor_state["current_size"],
            "message_count": monitor_state["message_count"],
            "capacity_used": monitor_state["capacity_used"],
            "last_check_time": monitor_state["last_check_time"],
            "last_save_time": monitor_state["last_save_time"],
            "threshold_reached": monitor_state["threshold_reached"],
            "context_limit": monitor_state["context_limit"],
            "context_source": monitor_state["context_source"],
        }


def reset_monitor():
    """Reinicia o monitor com valores zerados"""
    with state_lock:
        monitor_state["messages"] = []
        monitor_state["current_size"] = 0
        monitor_state["message_count"] = 0
        monitor_state["capacity_used"] = 0.0
        monitor_state["threshold_reached"] = False
        save_monitor_state()
    print("[MCP Monitor] Monitor reiniciado")


# Função principal para execução direta
if __name__ == "__main__":
    print("[MCP] Monitor de contexto iniciando...")

    # Carrega limites do BIOS-Q
    if load_context_limits():
        print(
            f"[MCP] Limite carregado do BIOS-Q: {monitor_state['context_limit']} caracteres (empírico)"
        )
    else:
        print(f"[MCP] Usando limite padrão: {monitor_state['context_limit']} caracteres")
        print("[MCP] Este limite será ajustado automaticamente quando o cursor solicitar novo chat")

    print(f"[MCP] Intervalo de verificação: a cada {CHECK_INTERVAL} segundos")
    print(f"[MCP] Salvamento automático: a cada {AUTO_SAVE_INTERVAL/60} minutos")

    # Inicia o monitoramento
    monitor_thread = start_monitoring()

    try:
        # Mantém o programa rodando
        while True:
            time.sleep(10)
            with state_lock:
                if not monitor_state["running"]:
                    break
    except KeyboardInterrupt:
        print("\n[MCP] Interrupção de teclado. Finalizando...")
    finally:
        stop_monitoring()

    print("[MCP] Monitor de contexto finalizado.")
