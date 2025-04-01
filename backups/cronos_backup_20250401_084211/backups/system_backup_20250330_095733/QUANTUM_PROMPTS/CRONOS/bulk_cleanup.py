import os
import sys
import shutil
import time
from pathlib import Path
import datetime
import subprocess

# Configurações
project_root = Path('C:/Eva Guarani EGOS')
backup_patterns = ['backup', 'BACKUP', 'bkp', 'BKP', 'BIOS-Q_backup', 'blockchain_backup', 'visualization_backup']
problematic_patterns = ['.git', 'node_modules']

# Diretórios a serem preservados - sempre manteremos o backup mais recente
preserve_patterns = []

# Encontrar o backup mais recente para preservar
latest_backup = None
latest_time = 0
backups_dir = project_root / 'QUANTUM_PROMPTS/CRONOS/backups'
if backups_dir.exists():
    for dir_path in backups_dir.glob('system_backup_*'):
        if dir_path.is_dir():
            dir_time = os.path.getctime(dir_path)
            if dir_time > latest_time:
                latest_time = dir_time
                latest_backup = dir_path

if latest_backup:
    preserve_patterns.append(str(latest_backup))
    print(f'⭐ O backup mais recente será preservado: {latest_backup.name}')

print('🔍 Procurando por backups antigos para limpeza...')
print('-' * 60)

# Função para lidar com erros de permissão
def handle_permission_error(path):
    """Tenta forçar a exclusão de diretórios com problemas de permissão"""
    try:
        # Função Windows específica para forçar exclusão
        if os.name == 'nt':  # Windows
            subprocess.run(['cmd', '/c', f'rmdir /s /q "{path}"'], shell=True)
            return True
    except:
        pass
    return False

# Encontrar todos os diretórios que parecem ser backups
found_backups = []

for root, dirs, files in os.walk(project_root):
    # Ignorar o diretório de backups que queremos preservar
    skip = False
    for pattern in preserve_patterns:
        if pattern in root:
            skip = True
            break
    if skip:
        continue
        
    for dir_name in dirs:
        # Verificar se o nome sugere um backup
        if any(pattern in dir_name.lower() for pattern in backup_patterns):
            backup_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(backup_path, project_root)
            
            # Verificar se não é um diretório preservado
            if any(pattern in backup_path for pattern in preserve_patterns):
                continue
                
            # Obter data de criação e tamanho
            try:
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(backup_path))
                
                # Calcular tamanho estimado
                size = 0
                file_count = 0
                try:
                    for r, d, f in os.walk(backup_path):
                        for file in f:
                            file_path = os.path.join(r, file)
                            try:
                                size += os.path.getsize(file_path)
                                file_count += 1
                            except:
                                pass
                except:
                    # Em caso de erro, ainda adicionamos o backup à lista
                    pass
                            
                found_backups.append({
                    'path': backup_path,
                    'rel_path': rel_path,
                    'created': creation_time,
                    'size_mb': size / (1024*1024),
                    'file_count': file_count
                })
            except Exception as e:
                print(f"Erro ao processar {backup_path}: {e}")

# Ordenar backups por tamanho (maiores primeiro)
found_backups.sort(key=lambda x: x['size_mb'], reverse=True)

# Mostrar resumo
if not found_backups:
    print('✅ Nenhum backup antigo encontrado para limpar!')
    sys.exit(0)

total_size = sum(b['size_mb'] for b in found_backups)
print(f'📁 Encontrados {len(found_backups)} diretórios de backup antigos')
print(f'💾 Espaço total ocupado: {total_size:.2f} MB ({total_size/1024:.2f} GB)')
print('-' * 60)

# Mostrar os 10 maiores backups
print("📊 Os 10 maiores backups:")
for i, backup in enumerate(found_backups[:10]):
    print(f"{i+1}. {backup['rel_path']} - {backup['size_mb']:.2f} MB")

print('-' * 60)

# Perguntar como proceder
print("Opções de limpeza:")
print("1. Deletar TODOS os backups antigos de uma vez")
print("2. Rever e confirmar cada backup individualmente")
print("3. Cancelar operação")

choice = input("Escolha uma opção (1-3): ")

if choice == '1':
    # Confirmação final
    confirm = input(f"ATENÇÃO: Você vai deletar {len(found_backups)} backups totalizando {total_size:.2f} MB. Digite 'SIM' para confirmar: ")
    if confirm != 'SIM':
        print("Operação cancelada.")
        sys.exit(0)
        
    # Deletar todos os backups
    deleted = 0
    failed = 0
    failed_list = []
    total_freed = 0
    
    for i, backup in enumerate(found_backups):
        print(f"Deletando [{i+1}/{len(found_backups)}]: {backup['rel_path']} ({backup['size_mb']:.2f} MB)")
        try:
            # Verificar se contém arquivos problemáticos
            has_problematic = False
            for prob in problematic_patterns:
                if prob in backup['path'].lower():
                    has_problematic = True
                    break
                    
            if has_problematic:
                # Tentar método alternativo para diretórios problemáticos
                success = handle_permission_error(backup['path'])
                if success:
                    deleted += 1
                    total_freed += backup['size_mb']
                else:
                    failed += 1
                    failed_list.append(backup['rel_path'])
            else:
                # Método padrão para diretórios normais
                shutil.rmtree(backup['path'])
                deleted += 1
                total_freed += backup['size_mb']
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            failed += 1
            failed_list.append(backup['rel_path'])
    
    # Mostrar resumo
    print('-' * 60)
    print(f"✅ Limpeza concluída!")
    print(f"📊 Backups deletados: {deleted}")
    print(f"📊 Backups com erro: {failed}")
    print(f"💾 Espaço liberado: {total_freed:.2f} MB ({total_freed/1024:.2f} GB)")
    
    if failed > 0:
        print("\n⚠️ Os seguintes backups não puderam ser deletados:")
        for path in failed_list[:10]:
            print(f"  - {path}")
        if len(failed_list) > 10:
            print(f"  ... e mais {len(failed_list) - 10} backups")
        
        print("\nDica: Para resolver problemas com arquivos .git, feche todos os programas que possam estar usando o repositório")
        print("      e tente executar o script novamente, ou use o Windows Explorer para deletar manualmente.")
        
elif choice == '2':
    # Confirmar cada backup individualmente
    deleted = 0
    failed = 0
    total_freed = 0
    
    for i, backup in enumerate(found_backups):
        print(f"{i+1}/{len(found_backups)}. {backup['rel_path']}")
        print(f"   📅 Criado em: {backup['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   💾 Tamanho: {backup['size_mb']:.2f} MB")
        print(f"   📄 Arquivos: {backup['file_count']}")
        
        # Confirmar exclusão
        confirm = input(f"   🗑️ Deletar este backup? (s/N): ").lower()
        if confirm == 's':
            try:
                # Verificar se contém arquivos problemáticos
                has_problematic = False
                for prob in problematic_patterns:
                    if prob in backup['path'].lower():
                        has_problematic = True
                        break
                        
                if has_problematic:
                    # Tentar método alternativo para diretórios problemáticos
                    success = handle_permission_error(backup['path'])
                    if success:
                        print(f"   ✅ Backup deletado com sucesso!")
                        deleted += 1
                        total_freed += backup['size_mb']
                    else:
                        print(f"   ❌ Erro ao deletar: Arquivos em uso ou permissão negada")
                        failed += 1
                else:
                    # Método padrão para diretórios normais
                    shutil.rmtree(backup['path'])
                    print(f"   ✅ Backup deletado com sucesso!")
                    deleted += 1
                    total_freed += backup['size_mb']
            except Exception as e:
                print(f"   ❌ Erro ao deletar: {e}")
                failed += 1
        else:
            print(f"   ℹ️ Backup mantido.")
        
        print('-' * 40)
    
    # Mostrar resumo
    print('-' * 60)
    print(f"✅ Limpeza concluída!")
    print(f"📊 Backups deletados: {deleted}")
    print(f"📊 Backups mantidos ou com erro: {len(found_backups) - deleted}")
    print(f"💾 Espaço liberado: {total_freed:.2f} MB ({total_freed/1024:.2f} GB)")
    
else:
    print("Operação cancelada.")
