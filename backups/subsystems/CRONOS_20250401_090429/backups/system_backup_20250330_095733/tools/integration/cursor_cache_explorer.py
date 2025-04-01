#!/usr/bin/env python3
import os
import json
from pathlib import Path
import logging

class CursorCacheExplorer:
    def __init__(self, workspace_root=None):
        """Inicializa o explorador de cache do Cursor"""
        self.workspace_root = workspace_root or os.getcwd()
        self.cursor_cache_dir = Path(self.workspace_root) / ".cursor" / "cache"
        self.logger = logging.getLogger("cursor_cache_explorer")
        
    def cache_exists(self):
        """Verifica se o cache do Cursor existe"""
        return self.cursor_cache_dir.exists()
        
    def list_cache_files(self):
        """Lista todos os arquivos de cache do Cursor"""
        if not self.cache_exists():
            self.logger.warning("Cache do Cursor não encontrado")
            return []
            
        return list(self.cursor_cache_dir.glob("*"))
        
    def get_index_files(self):
        """Retorna arquivos específicos de índice"""
        return list(self.cursor_cache_dir.glob("*.idx"))
        
    def get_embedding_files(self):
        """Retorna arquivos de embedding"""
        return list(self.cursor_cache_dir.glob("*embedding*"))
        
    def read_cache_file(self, filename):
        """Lê o conteúdo de um arquivo de cache"""
        file_path = self.cursor_cache_dir / filename
        if not file_path.exists():
            self.logger.error(f"Arquivo não encontrado: {file_path}")
            return None
            
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                # Tenta decodificar como JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Retorna conteúdo binário se não for JSON
                    return content
        except Exception as e:
            self.logger.error(f"Erro ao ler arquivo {file_path}: {str(e)}")
            return None

def main():
    explorer = CursorCacheExplorer()
    print(f"Cache do Cursor existe: {explorer.cache_exists()}")
    
    print("\nArquivos de cache:")
    for f in explorer.list_cache_files():
        print(f"- {f.name} ({f.stat().st_size} bytes)")
    
    print("\nArquivos de índice:")
    for f in explorer.get_index_files():
        print(f"- {f.name}")
        
    print("\nArquivos de embedding:")
    for f in explorer.get_embedding_files():
        print(f"- {f.name}")
    
if __name__ == "__main__":
    main()
