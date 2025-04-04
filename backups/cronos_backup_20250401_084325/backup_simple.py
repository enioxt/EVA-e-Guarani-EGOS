import os
import shutil
import datetime
from pathlib import Path

# Configurações simplificadas
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
]
excluded_exts = [".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".zip", ".tar", ".gz", ".rar"]
project_root = Path("C:/Eva Guarani EGOS")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = project_root / "QUANTUM_PROMPTS/CRONOS/backups" / f"system_backup_{timestamp}"

print(f"Iniciando backup para: {backup_dir}")

# Criar diretório de backup
os.makedirs(backup_dir, exist_ok=True)

# Contadores
files_copied = 0
files_skipped = 0

# Percorrer arquivos
for root, dirs, files in os.walk(project_root):
    # Evitar recursão
    if str(backup_dir) in root:
        continue

    # Remover diretórios excluídos
    dirs[:] = [d for d in dirs if d not in excluded_dirs]

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
        except Exception as e:
            print(f"Erro ao copiar {src_path}: {e}")

print(
    f"✅ Backup concluído! Arquivos copiados: {files_copied}, Arquivos ignorados: {files_skipped}"
)
print(f"📁 Localização: {backup_dir}")
