import os
import sys
from pathlib import Path
import datetime

# Procurar por pastas de backup em toda a estrutura
project_root = Path('C:/Eva Guarani EGOS')
backup_patterns = ['backup', 'BACKUP', 'bkp', 'BKP', 'BIOS-Q_backup', 'blockchain_backup', 'visualization_backup']
problematic_dirs = ['node_modules', '.venv', 'venv', 'quarantine', '__pycache__', '.git']

print('🔍 Procurando por backups antigos no sistema...')
print('-' * 60)

# Encontrar todos os diretórios que parecem ser backups
found_backups = []

for root, dirs, files in os.walk(project_root):
    # Ignorar o diretório de backups recém-criado
    if 'CRONOS\\backups\\system_backup_' in root:
        continue
        
    for dir_name in dirs:
        # Verificar se o nome sugere um backup
        if any(pattern in dir_name for pattern in backup_patterns):
            backup_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(backup_path, project_root)
            
            # Obter data de criação e tamanho
            try:
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(backup_path))
                
                # Calcular tamanho estimado
                size = 0
                file_count = 0
                for r, d, f in os.walk(backup_path):
                    for file in f:
                        file_path = os.path.join(r, file)
                        try:
                            size += os.path.getsize(file_path)
                            file_count += 1
                        except:
                            pass
                            
                found_backups.append({
                    'path': backup_path,
                    'rel_path': rel_path,
                    'created': creation_time,
                    'size_mb': size / (1024*1024),
                    'file_count': file_count
                })
            except:
                pass

# Ordenar backups por data (mais recentes primeiro)
found_backups.sort(key=lambda x: x['created'], reverse=True)

# Mostrar resumo
if not found_backups:
    print('✅ Nenhum backup antigo encontrado no sistema!')
else:
    print(f'📁 Encontrados {len(found_backups)} diretórios de backup antigos:')
    total_size = sum(b['size_mb'] for b in found_backups)
    print(f'💾 Espaço total ocupado: {total_size:.2f} MB ({total_size/1024:.2f} GB)')
    print('-' * 60)
    
    # Mostrar detalhes dos 10 maiores backups
    for i, backup in enumerate(sorted(found_backups, key=lambda x: x['size_mb'], reverse=True)[:10]):
        print(f"{i+1}. {backup['rel_path']}")
        print(f"   📅 Criado em: {backup['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   💾 Tamanho: {backup['size_mb']:.2f} MB")
        print(f"   📄 Arquivos: {backup['file_count']}")
        
        # Verificar problemas
        has_problems = False
        for r, d, f in os.walk(backup['path']):
            for dir_name in d:
                if dir_name in problematic_dirs:
                    if not has_problems:
                        print(f"   ⚠️ Problemas encontrados:")
                        has_problems = True
                    rel_problem_path = os.path.relpath(os.path.join(r, dir_name), backup['path'])
                    print(f"      - {rel_problem_path}")
                    break
            if has_problems:
                break
                
        print('-' * 40)
