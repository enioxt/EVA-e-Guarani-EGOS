import os
import sys
from pathlib import Path

# Diretórios problemáticos que queremos verificar
problematic_dirs = ['node_modules', '.venv', 'venv', 'quarantine', '__pycache__', '.git']

# Encontrar o backup mais recente
backup_dir = Path('C:/Eva Guarani EGOS/QUANTUM_PROMPTS/CRONOS/backups')
latest_backup = None
latest_time = 0

if not backup_dir.exists():
    print(f'Diretório de backup não encontrado: {backup_dir}')
    sys.exit(1)

for dir_path in backup_dir.iterdir():
    if dir_path.is_dir() and dir_path.name.startswith('system_backup_'):
        dir_time = os.path.getctime(dir_path)
        if dir_time > latest_time:
            latest_time = dir_time
            latest_backup = dir_path

if not latest_backup:
    print('Nenhum backup encontrado')
    sys.exit(1)

print(f'Verificando backup mais recente: {latest_backup.name}')
print('-' * 50)

# Procurar diretórios problemáticos
problem_found = False
for root, dirs, files in os.walk(latest_backup):
    for dir_name in dirs:
        if dir_name in problematic_dirs:
            rel_path = os.path.relpath(os.path.join(root, dir_name), latest_backup)
            print(f'❌ Diretório problemático encontrado: {rel_path}')
            problem_found = True

if not problem_found:
    print('✅ Nenhum diretório problemático encontrado no backup!')
    
# Calcular o tamanho do backup
total_size = 0
file_count = 0
for root, dirs, files in os.walk(latest_backup):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            total_size += os.path.getsize(file_path)
            file_count += 1
        except:
            pass

print(f'📊 Estatísticas do backup:')
print(f'   - Tamanho total: {total_size / (1024*1024):.2f} MB')
print(f'   - Número de arquivos: {file_count}')
