#!/usr/bin/env python3
import os
import json
from pathlib import Path

def test_bios_integration():
    print("\n🔍 Iniciando testes de integração do BIOS-Q...\n")
    
    # 1. Verificar estrutura de diretórios
    required_dirs = [
        "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\config",
        "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\storage\\cursor_context"
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Diretório não encontrado: {dir_path}")
            return False
        print(f"✅ Diretório encontrado: {dir_path}")
    
    # 2. Verificar arquivo de configuração
    config_path = "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\config\\bios_config.json"
    if not os.path.exists(config_path):
        print(f"❌ Arquivo de configuração não encontrado: {config_path}")
        return False
    
    try:
        # Primeiro, vamos ler o conteúdo do arquivo para debug
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"\n📄 Conteúdo do arquivo de configuração:")
            print(content)
            print("\n📊 Tamanho do arquivo:", len(content), "bytes")
            
        # Agora tentamos carregar como JSON
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print("\n✅ Arquivo de configuração carregado com sucesso")
            
            # Verificar estrutura do config
            required_keys = ['cursor_paths', 'bios_paths', 'integration']
            for key in required_keys:
                if key not in config:
                    print(f"❌ Chave '{key}' não encontrada no arquivo de configuração")
                    return False
                print(f"✅ Chave '{key}' encontrada no arquivo de configuração")
    except Exception as e:
        print(f"\n❌ Erro ao carregar configuração: {str(e)}")
        print(f"Tipo de erro: {type(e).__name__}")
        return False
    
    # 3. Verificar arquivo de integração
    integration_path = "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\cursor_integration.py"
    if not os.path.exists(integration_path):
        print(f"❌ Arquivo de integração não encontrado: {integration_path}")
        return False
    print(f"✅ Arquivo de integração encontrado: {integration_path}")
    
    # 4. Verificar caminhos do Cursor
    cursor_paths = [
        "C:\\Users\\Enidi\\AppData\\Roaming\\Cursor",
        "C:\\Users\\Enidi\\.cursor"
    ]
    
    for path in cursor_paths:
        if not os.path.exists(path):
            print(f"❌ Caminho do Cursor não encontrado: {path}")
            return False
        print(f"✅ Caminho do Cursor encontrado: {path}")
    
    # 5. Verificar permissões
    try:
        test_file = "C:\\Eva & Guarani - EGOS\\BIOS-Q\\BIOS_Q\\storage\\cursor_context\\test.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Permissões de escrita verificadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao verificar permissões: {e}")
        return False
    
    print("\n✨ Todos os testes passaram com sucesso!")
    return True

if __name__ == "__main__":
    test_bios_integration() 