#!/usr/bin/env python3
"""
Script para configuração e verificação do BIOS-Q
"""

import os
import sys
import shutil
from pathlib import Path


def create_directory_structure():
    """Cria a estrutura de diretórios necessária para o BIOS-Q"""
    base_dir = Path(__file__).parent.parent / "BIOS-Q"

    # Estrutura de diretórios
    directories = [
        "",
        "core",
        "ethics",
        "integration",
        "quantum",
        "storage",
        "storage/quantum",
        "storage/context",
    ]

    # Cria os diretórios
    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)

    print(f"✓ Estrutura de diretórios criada em {base_dir}")
    return base_dir


def copy_ethik_principles():
    """Copia princípios éticos do ETHIK para o BIOS-Q"""
    ethik_dir = Path(__file__).parent.parent.parent / "core" / "ethik"
    bios_ethics_dir = Path(__file__).parent.parent / "BIOS-Q" / "ethics"

    if not ethik_dir.exists():
        print(f"✗ Diretório ETHIK não encontrado em {ethik_dir}")
        return False

    try:
        # Copiar arquivo de configuração ética
        if (ethik_dir / "ethik_config.json").exists():
            shutil.copy(ethik_dir / "ethik_config.json", bios_ethics_dir / "ethik_config.json")
            print(f"✓ Configuração ETHIK copiada para BIOS-Q")

        return True
    except Exception as e:
        print(f"✗ Erro ao copiar princípios ETHIK: {str(e)}")
        return False


def verify_installation():
    """Verifica se a instalação foi bem-sucedida"""
    bios_dir = Path(__file__).parent.parent / "BIOS-Q"

    # Verifica se os diretórios existem
    directories = ["core", "ethics", "integration", "quantum", "storage"]
    missing = [d for d in directories if not (bios_dir / d).exists()]

    if missing:
        print(f"✗ Diretórios ausentes: {', '.join(missing)}")
        return False

    print("✓ Verificação de diretórios concluída com sucesso")

    # Tenta importar o BIOS-Q
    sys.path.append(str(bios_dir.parent))
    try:
        from BIOS_Q import biosq

        print(f"✓ BIOS-Q importado com sucesso")

        # Verifica componentes
        status = biosq.get_status()
        print(f"✓ Arquitetos ativos: {', '.join(status['architects_active'])}")
        print(f"✓ ETHIK conectado: {status['ethik_connected']}")

        return True
    except Exception as e:
        print(f"✗ Erro ao importar BIOS-Q: {str(e)}")
        return False


def main():
    """Função principal"""
    print("=== Configurando BIOS-Q ===")

    # Cria estrutura de diretórios
    base_dir = create_directory_structure()

    # Copia princípios éticos
    copy_ethik_principles()

    # Verifica instalação
    if verify_installation():
        print("\n✓ BIOS-Q configurado com sucesso!")
        print(f"  Diretório base: {base_dir}")
        print("\nPara usar o BIOS-Q, importe-o em seus scripts Python:")
        print("  from tools.BIOS_Q import biosq")
    else:
        print("\n✗ Configuração do BIOS-Q incompleta. Revise os erros acima.")


if __name__ == "__main__":
    main()
