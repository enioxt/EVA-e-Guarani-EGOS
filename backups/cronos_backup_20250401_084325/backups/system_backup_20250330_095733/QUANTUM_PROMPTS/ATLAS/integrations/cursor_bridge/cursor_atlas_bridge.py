#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from tools.integration.cursor_cache_explorer import CursorCacheExplorer
from core.atlas import map_project, visualize_mapping


class CursorAtlasBridge:
    def __init__(self):
        """Inicializa a ponte entre Cursor e ATLAS"""
        self.explorer = CursorCacheExplorer()

    def extract_file_structure(self):
        """Extrai a estrutura de arquivos do cache do Cursor"""
        # Esta é uma implementação inicial - precisaremos adaptar
        # baseado no formato real dos arquivos de cache

        structure = {"files": [], "directories": []}

        if not self.explorer.cache_exists():
            print("Cache do Cursor não encontrado")
            return structure

        # Procurar por arquivos que contêm estrutura de arquivos
        # (implementação a ser refinada após análise dos arquivos)
        index_files = self.explorer.get_index_files()
        for idx_file in index_files:
            content = self.explorer.read_cache_file(idx_file.name)
            if content and isinstance(content, dict):
                # Lógica de extração a ser implementada após análise
                # dos arquivos reais
                pass

        return structure

    def generate_atlas_mapping(self, output_path="atlas_from_cursor.json"):
        """Gera um mapeamento do ATLAS usando dados do Cursor"""
        # Extrair estrutura
        structure = self.extract_file_structure()

        # Transformar para formato compatível com ATLAS
        atlas_data = {
            "nodes": [],
            "edges": [],
            "metadata": {"source": "cursor_cache", "timestamp": str(datetime.datetime.now())},
        }

        # Mapear usando ATLAS
        mapping = map_project(atlas_data)

        # Visualizar
        visualize_mapping(mapping, output_path)

        return mapping


def main():
    bridge = CursorAtlasBridge()

    print("Extraindo estrutura do cache do Cursor...")
    structure = bridge.extract_file_structure()

    print(
        f"Encontrados {len(structure['files'])} arquivos e {len(structure['directories'])} diretórios"
    )

    print("Gerando mapeamento do ATLAS...")
    mapping = bridge.generate_atlas_mapping()

    print(f"Mapeamento gerado com {len(mapping['nodes'])} nós e {len(mapping['edges'])} conexões")


if __name__ == "__main__":
    main()
