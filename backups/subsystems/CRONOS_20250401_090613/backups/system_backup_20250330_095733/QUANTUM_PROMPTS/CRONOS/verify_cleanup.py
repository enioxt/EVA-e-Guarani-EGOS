import os
import sys
from pathlib import Path
import datetime

# Configurações
project_root = Path("C:/Eva Guarani EGOS")
problematic_dirs = ["node_modules", ".venv", "venv", "quarantine", "__pycache__", ".git"]
backup_patterns = [
    "backup",
    "BACKUP",
    "bkp",
    "BKP",
    "BIOS-Q_backup",
    "blockchain_backup",
    "visualization_backup",
]

# 1. Verificar se o backup recente existe
print("🔍 Verificando backup preservado...")
latest_backup = None
latest_time = 0
backups_dir = project_root / "QUANTUM_PROMPTS/CRONOS/backups"

if not backups_dir.exists():
    print(f"❌ Diretório de backup não encontrado: {backups_dir}")
else:
    for dir_path in backups_dir.glob("system_backup_*"):
        if dir_path.is_dir():
            dir_time = os.path.getctime(dir_path)
            if dir_time > latest_time:
                latest_time = dir_time
                latest_backup = dir_path

    if latest_backup:
        print(f"✅ Backup preservado encontrado: {latest_backup.name}")

        # Calcular tamanho
        size = 0
        file_count = 0
        for root, dirs, files in os.walk(latest_backup):
            size += sum(
                os.path.getsize(os.path.join(root, name))
                for name in files
                if os.path.exists(os.path.join(root, name))
            )
            file_count += len(files)

        print(f"   💾 Tamanho: {size / (1024*1024):.2f} MB")
        print(f"   📄 Arquivos: {file_count}")

        # Verificar diretórios problemáticos
        problems = []
        for root, dirs, files in os.walk(latest_backup):
            for d in dirs:
                if d in problematic_dirs:
                    rel_path = os.path.relpath(os.path.join(root, d), latest_backup)
                    problems.append(rel_path)

        if problems:
            print(f"⚠️ Encontrados {len(problems)} diretórios problemáticos:")
            for p in problems[:5]:
                print(f"   - {p}")
            if len(problems) > 5:
                print(f"   ... e mais {len(problems) - 5}")
        else:
            print("✅ Nenhum diretório problemático encontrado no backup!")
    else:
        print("❌ Nenhum backup encontrado!")

# 2. Verificar se restaram outros backups
print("\n🔍 Procurando por backups remanescentes...")
remaining_backups = []

for root, dirs, files in os.walk(project_root):
    for dir_name in dirs:
        if any(pattern in dir_name.lower() for pattern in backup_patterns):
            # Verificar se não é o backup que preservamos
            if latest_backup and str(latest_backup) not in os.path.join(root, dir_name):
                rel_path = os.path.relpath(os.path.join(root, dir_name), project_root)
                remaining_backups.append(rel_path)

if remaining_backups:
    print(f"⚠️ Encontrados {len(remaining_backups)} backups remanescentes:")
    for backup in remaining_backups[:10]:
        print(f"   - {backup}")
    if len(remaining_backups) > 10:
        print(f"   ... e mais {len(remaining_backups) - 10}")
else:
    print("✅ Nenhum backup antigo remanescente encontrado!")

# 3. Verificar espaço em disco
try:
    import shutil

    total, used, free = shutil.disk_usage(project_root)
    print(f"\n💾 Espaço em disco:")
    print(f"   Total: {total / (1024**3):.2f} GB")
    print(f"   Usado: {used / (1024**3):.2f} GB")
    print(f"   Livre: {free / (1024**3):.2f} GB")
except:
    pass

print("\n✨ Verificação concluída!")
