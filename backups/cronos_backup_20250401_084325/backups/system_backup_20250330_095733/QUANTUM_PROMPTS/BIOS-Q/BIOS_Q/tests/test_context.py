#!/usr/bin/env python3
import os
import json
import shutil
from datetime import datetime


def test_context_system():
    print("\n🔍 Iniciando testes do sistema de contexto...\n")

    # 1. Verificar diretório de contexto
    context_dir = "C:\\Eva & Guarani - EGOS\\CHATS"
    if not os.path.exists(context_dir):
        print(f"❌ Diretório de contexto não encontrado: {context_dir}")
        return False
    print(f"✅ Diretório de contexto encontrado: {context_dir}")

    # 2. Verificar arquivos de contexto recentes
    context_files = [
        f
        for f in os.listdir(context_dir)
        if f.startswith("bios_q_context_") and f.endswith(".json")
    ]
    if not context_files:
        print("❌ Nenhum arquivo de contexto encontrado")
        return False
    print(f"✅ Arquivos de contexto encontrados: {len(context_files)}")

    # 3. Verificar arquivo de chat atual
    current_chat = os.path.join(context_dir, "current_chat.md")
    if not os.path.exists(current_chat):
        print("❌ Arquivo de chat atual não encontrado")
        return False
    print("✅ Arquivo de chat atual encontrado")

    # 4. Testar criação de novo contexto
    test_context = {
        "timestamp": datetime.now().isoformat(),
        "project": "EVA & GUARANI - EGOS",
        "environment": "Cursor + Claude 3.7 Sonnet",
        "signature": "TEST_CONTEXT_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
        "test_data": "Este é um contexto de teste",
    }

    test_file = os.path.join(
        context_dir, f"test_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    try:
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_context, f, indent=2)
        print("✅ Teste de criação de contexto bem-sucedido")

        # Verificar se o arquivo foi criado corretamente
        with open(test_file, "r", encoding="utf-8") as f:
            loaded_context = json.load(f)
            if loaded_context["test_data"] == test_context["test_data"]:
                print("✅ Verificação de leitura do contexto bem-sucedida")
            else:
                print("❌ Erro na verificação do contexto")
                return False

        # Limpar arquivo de teste
        os.remove(test_file)
        print("✅ Limpeza do arquivo de teste bem-sucedida")

    except Exception as e:
        print(f"❌ Erro ao testar criação de contexto: {str(e)}")
        return False

    # 5. Verificar backup de contexto
    backup_dir = os.path.join(
        context_dir, "backup_context_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print("✅ Diretório de backup criado")

    # 6. Testar backup de arquivos importantes
    important_files = ["current_chat.md", "chat_index.json", "chat_report.md"]

    for file in important_files:
        src = os.path.join(context_dir, file)
        if os.path.exists(src):
            dst = os.path.join(backup_dir, file)
            shutil.copy2(src, dst)
            print(f"✅ Backup de {file} realizado")
        else:
            print(f"⚠️ Arquivo {file} não encontrado para backup")

    print("\n✨ Todos os testes de contexto passaram com sucesso!")
    return True


if __name__ == "__main__":
    test_context_system()
