import os
import shutil
import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("CRONOS-Backup")

# Configurações
project_root = Path("C:/Eva Guarani EGOS")
excluded_dirs = [
    "node_modules",
    ".venv",
    "venv",
    "quarantine",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "tmp",
    "temp",
]
excluded_exts = [
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".dll",
    ".exe",
    ".zip",
    ".tar",
    ".gz",
    ".rar",
    ".jar",
    ".war",
    ".class",
]

# Criar diretório de backup
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = project_root / "QUANTUM_PROMPTS/CRONOS/backups" / f"system_backup_{timestamp}"

print(f"🚀 Criando novo backup em: {backup_dir}")

# Criar diretório de backup e todos os diretórios pai
os.makedirs(backup_dir, exist_ok=True)

# Contadores
files_copied = 0
files_skipped = 0
dirs_skipped = 0
dirs_copied = 0
bytes_copied = 0

# Percorrer arquivos
for root, dirs, files in os.walk(project_root):
    # Evitar recursão
    if str(backup_dir) in root:
        continue

    # Remover diretórios excluídos da lista de diretórios a processar (in-place)
    dirs_before = len(dirs)
    dirs[:] = [d for d in dirs if d not in excluded_dirs]
    dirs_skipped += dirs_before - len(dirs)

    # Processar arquivos
    for file in files:
        src_path = os.path.join(root, file)
        if any(src_path.endswith(ext) for ext in excluded_exts):
            files_skipped += 1
            continue

        # Criar caminho relativo
        rel_path = os.path.relpath(src_path, project_root)
        dst_path = os.path.join(backup_dir, rel_path)

        # Criar diretórios pai
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        # Copiar arquivo
        try:
            shutil.copy2(src_path, dst_path)
            files_copied += 1
            bytes_copied += os.path.getsize(src_path)
            dirs_copied += 1
        except Exception as e:
            print(f"❌ Erro ao copiar {src_path}: {e}")

print(f"✅ Backup concluído! Estatísticas:")
print(f"📊 Arquivos copiados: {files_copied}")
print(f"📊 Arquivos ignorados: {files_skipped}")
print(f"📊 Diretórios ignorados: {dirs_skipped}")
print(f"💾 Tamanho total: {bytes_copied / (1024*1024):.2f} MB")
print(f"📁 Localização: {backup_dir}")

# Verificar se o backup contém arquivos problemáticos
problems_found = 0
for root, dirs, files in os.walk(backup_dir):
    for d in dirs:
        if d in excluded_dirs:
            rel_path = os.path.relpath(os.path.join(root, d), backup_dir)
            print(f"⚠️ Diretório problemático encontrado: {rel_path}")
            problems_found += 1

if problems_found == 0:
    print("✅ Nenhum diretório problemático encontrado no backup!")
else:
    print(f"⚠️ Encontrados {problems_found} diretórios problemáticos no backup!")

print("✨ EVA & GUARANI - Sistema de backup CRONOS otimizado")
