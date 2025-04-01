#!/usr/bin/env python3
"""
EVA & GUARANI - BIOS-Q Cursor Integration
Script de inicialização para integração com Cursor IDE
"""

import sys
from pathlib import Path
from BIOS_Q import BIOSQCursor

def main():
    """Função principal"""
    try:
        # Inicializa o BIOS-Q
        bios_q = BIOSQCursor()
        
        # Verifica argumentos
        if len(sys.argv) < 2:
            print("Uso: python start_cursor_bios.py [save|load]")
            sys.exit(1)
            
        command = sys.argv[1]
        
        # Executa comando
        if command == "save":
            bios_q.save_context()
        elif command == "load":
            bios_q.load_context()
        else:
            print(f"Comando inválido: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Erro ao executar BIOS-Q: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 