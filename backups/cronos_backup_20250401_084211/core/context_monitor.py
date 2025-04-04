#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CRONOS - Context Retention and Operational Neural Optimization System
==================================================================

Sistema de preservação de contexto para EVA & GUARANI no ambiente Cursor IDE.
Anteriormente conhecido como Memory Context Protocol (MCP).

Funcionalidades:
- Monitoramento adaptativo de contexto
- Auto-save baseado em limites
- Backup preventivo
- Integração com BIOS-Q
"""

import os
import time
import json
import threading
import datetime
from pathlib import Path

# Configurações
DEFAULT_CONTEXT_LIMIT = 100000  # Limite inicial conservador
SAFE_MARGIN = 0.90  # Usa 90% do limite real para segurança
CHECK_INTERVAL = 60  # Verifica a cada 60 segundos
AUTO_SAVE_INTERVAL = 30 * 60  # Auto-save a cada 30 minutos

# Caminhos
CONFIG_DIR = Path(__file__).parent.parent / "config"
CONTEXT_LIMITS_FILE = CONFIG_DIR / "context_limits.json"
MONITOR_DATA_FILE = CONFIG_DIR / "monitor_data.json"

# Garantir que os diretórios existam
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Estado global
monitor_state = {
    "running": False,
    "current_size": 0,
    "message_count": 0,
    "capacity_used": 0.0,
    "last_check_time": time.time(),
    "last_save_time": time.time(),
    "threshold_reached": False,
    "context_limit": DEFAULT_CONTEXT_LIMIT,
    "context_source": "default",
}

# Thread safety
state_lock = threading.RLock()


def load_context_limits():
    """Carrega limites de contexto da configuração"""
    try:
        if CONTEXT_LIMITS_FILE.exists():
            with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
                limits = json.load(f)
                with state_lock:
                    if "cursor" in limits and limits["cursor"].get("measured", False):
                        monitor_state["context_limit"] = limits["cursor"]["safe_limit"]
                        monitor_state["context_source"] = "empirical"
                        return True
        return False
    except Exception as e:
        print(f"Erro ao carregar limites de contexto: {e}")
        return False


def save_context_limits(limit, measured=True):
    """Salva limites de contexto na configuração"""
    try:
        limits = {}
        if CONTEXT_LIMITS_FILE.exists():
            with open(CONTEXT_LIMITS_FILE, "r", encoding="utf-8") as f:
                limits = json.load(f)

        limits["cursor"] = {
            "limit": limit,
            "measured": measured,
            "last_updated": datetime.datetime.now().isoformat(),
            "safe_limit": int(limit * SAFE_MARGIN),
        }

        with open(CONTEXT_LIMITS_FILE, "w", encoding="utf-8") as f:
            json.dump(limits, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar limites de contexto: {e}")
        return False


def save_monitor_state():
    """Salva o estado do monitor em arquivo"""
    try:
        with open(MONITOR_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(monitor_state, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar estado do monitor: {e}")
        return False


def check_context_size():
    """Verifica o tamanho atual do contexto e aciona auto-save se necessário"""
    with state_lock:
        current_time = time.time()

        # Auto-save no intervalo
        if current_time - monitor_state["last_save_time"] >= AUTO_SAVE_INTERVAL:
            from . import cronos_capture  # Import aqui para evitar dependência circular

            cronos_capture.save_context()
            monitor_state["last_save_time"] = current_time

        # Atualiza estado
        monitor_state["last_check_time"] = current_time
        save_monitor_state()


def start_monitoring():
    """Inicia o thread de monitoramento"""

    def monitor_loop():
        while monitor_state["running"]:
            check_context_size()
            time.sleep(CHECK_INTERVAL)

    with state_lock:
        if not monitor_state["running"]:
            monitor_state["running"] = True
            thread = threading.Thread(target=monitor_loop, daemon=True)
            thread.start()
            return thread
    return None


def stop_monitoring():
    """Para o monitoramento"""
    with state_lock:
        monitor_state["running"] = False
        save_monitor_state()


def update_context_size(size):
    """Atualiza o tamanho atual do contexto"""
    with state_lock:
        monitor_state["current_size"] = size
        monitor_state["capacity_used"] = size / monitor_state["context_limit"]
        monitor_state["threshold_reached"] = monitor_state["capacity_used"] >= 0.8
        save_monitor_state()


def get_monitor_status():
    """Obtém o status atual do monitor"""
    with state_lock:
        return {
            "running": monitor_state["running"],
            "current_size": monitor_state["current_size"],
            "capacity_used": f"{monitor_state['capacity_used']*100:.1f}%",
            "context_limit": monitor_state["context_limit"],
            "source": monitor_state["context_source"],
            "last_check": datetime.datetime.fromtimestamp(
                monitor_state["last_check_time"]
            ).isoformat(),
            "last_save": datetime.datetime.fromtimestamp(
                monitor_state["last_save_time"]
            ).isoformat(),
        }


if __name__ == "__main__":
    print("Iniciando monitor de contexto CRONOS...")

    if load_context_limits():
        print(f"Limite empírico carregado: {monitor_state['context_limit']} caracteres")
    else:
        print(f"Usando limite padrão: {monitor_state['context_limit']} caracteres")

    monitor_thread = start_monitoring()

    try:
        while True:
            time.sleep(10)
            with state_lock:
                if not monitor_state["running"]:
                    break
    except KeyboardInterrupt:
        print("\nParando monitor...")
    finally:
        stop_monitoring()

    print("Monitor de contexto CRONOS finalizado.")
