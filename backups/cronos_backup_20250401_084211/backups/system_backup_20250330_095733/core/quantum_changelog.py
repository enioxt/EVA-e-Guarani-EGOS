#!/usr/bin/env python3
"""
# ========================================================================
# QUANTUM CHANGELOG - EVA & GUARANI EVOLUTIONARY RECORD SYSTEM
# ========================================================================
#
# VERSION: 1.0.0 "Pear" - Quantum Context and Memory Preservation System
#
# WHAT IS THIS SYSTEM?
# ---------------------
# This system detects, stores, and manages important advances during the 
# development of the EVA & GUARANI project. It functions as a "quantum memory"
# that preserves context and progress, even with the context limits of LLMs.
#
# HOW TO USE:
# ----------
# 1. SCAN:       python core/quantum_changelog.py       (Option 1)
# 2. REVIEW:     python core/quantum_approval_ui.py     (Graphical interface)
# 3. UPDATE:     python core/quantum_changelog.py       (Option 3)
#
# On Windows, also use: start_quantum_review.bat
#
# MAIN FEATURES:
# -------------------
# - Automatic detection of code progress
# - Storage in protected area (staging)
# - Review with visual interface
# - Protection of Quantum Prompt and BIOS-Q
# - Automatic backups of all changes
#
# ========================================================================
"""

import os
import json
import datetime
import yaml
import hashlib
import re
import sys
from pathlib import Path
from itertools import zip_longest

# ========================================================================
# GLOBAL CONFIGURATIONS
# ========================================================================

# Main directories
STAGING_DIR = "staging"                                # Staging area
CHANGELOG_FILE = f"{STAGING_DIR}/quantum_changelog.json"  # Change log
HISTORY_DIR = f"{STAGING_DIR}/history"                 # Change history
BIOS_CONFIG = "config/ethik_chain_core.yaml"           # BIOS-Q configuration
QUANTUM_PROMPT = "QUANTUM_PROMPTS/core_principles.md"  # Main Quantum Prompt
QUANTUM_SIGNATURE = "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"        # Quantum signature

# System version
VERSION = "1.0.0"                                      # System version
VERSION_NAME = "Pear"                                  # Version name
VERSION_DESCRIPTION = "Quantum Context and Memory Preservation System"

# Padrões para detecção automática
PROGRESS_INDICATORS = [
    # Português
    "implementado", "criado", "concluído", "finalizado", "desenvolvido", "adicionado", 
    "completado", "melhorado", "refatorado", "otimizado", "avanço", "melhoria", 
    "evolução", "progresso",
    
    # Inglês
    "implemented", "created", "completed", "finished", "developed", "added",
    "improved", "refactored", "optimized", "breakthrough", "improvement", 
    "enhancement", "progress"
]

# ========================================================================
# CLASSE PRINCIPAL: QUANTUM CHANGELOG
# ========================================================================

class QuantumChangelog:
    """
    Sistema de registro evolutivo que preserva avanços importantes
    
    Este sistema permite:
    1. Detectar automaticamente progressos no código
    2. Armazenar esses progressos em um registro seguro
    3. Revisar e aprovar progressos para integração
    4. Gerar propostas de atualização para a BIOS-Q
    5. Manter backups e histórico de todas as alterações
    """
    
    def __init__(self):
        """Inicializa o sistema de changelog com os diretórios e arquivos necessários"""
        self._ensure_directories()
        self.changelog = self._load_changelog()
        self.bios_config = self._load_bios_config()
        
        # Mostrar informações da versão
        print(f"\n{QUANTUM_SIGNATURE}")
        print(f"QUANTUM CHANGELOG v{VERSION} '{VERSION_NAME}'")
        print(f"{VERSION_DESCRIPTION}")
        print(f"Iniciado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
    def _ensure_directories(self):
        """Garante que os diretórios necessários existam"""
        os.makedirs(STAGING_DIR, exist_ok=True)
        os.makedirs(HISTORY_DIR, exist_ok=True)
        os.makedirs(f"{HISTORY_DIR}/backups", exist_ok=True)
    
    def _load_changelog(self):
        """
        Carrega o arquivo de changelog ou cria um novo
        
        Retorna:
            dict: Estrutura de dados do changelog
        """
        if os.path.exists(CHANGELOG_FILE):
            try:
                with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
                    changelog = json.load(f)
                print(f"✅ Changelog carregado: {len(changelog.get('entries', []))} entradas aprovadas, {len(changelog.get('pending_review', []))} pendentes")
                return changelog
            except Exception as e:
                print(f"⚠️ Erro ao carregar changelog: {str(e)}")
                return self._create_empty_changelog()
        else:
            print("ℹ️ Criando novo arquivo de changelog")
            return self._create_empty_changelog()
    
    def _create_empty_changelog(self):
        """
        Cria uma estrutura vazia para o changelog
        
        Retorna:
            dict: Estrutura básica do changelog
        """
        return {
            "version": VERSION,
            "version_name": VERSION_NAME,
            "last_updated": datetime.datetime.now().isoformat(),
            "entries": [],             # Entradas aprovadas
            "pending_review": [],      # Entradas pendentes de revisão
            "integration_history": []  # Histórico de integrações
        }
    
    def _load_bios_config(self):
        """
        Carrega a configuração da BIOS-Q
        
        Retorna:
            dict: Configuração da BIOS-Q ou None se não encontrada
        """
        try:
            if os.path.exists(BIOS_CONFIG):
                with open(BIOS_CONFIG, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                print(f"✅ Configuração da BIOS-Q carregada de {BIOS_CONFIG}")
                return config
            print(f"⚠️ Arquivo de configuração da BIOS-Q não encontrado: {BIOS_CONFIG}")
            return None
        except Exception as e:
            print(f"⚠️ Erro ao carregar BIOS Config: {str(e)}")
            return None
    
    def _save_changelog(self):
        """
        Salva o changelog atualizado
        
        Retorna:
            bool: True se salvou com sucesso, False caso contrário
        """
        self.changelog["last_updated"] = datetime.datetime.now().isoformat()
        try:
            with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.changelog, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Erro ao salvar changelog: {str(e)}")
            return False
    
    def add_entry(self, content, source, category="development", importance=0.5):
        """
        Adiciona uma entrada ao changelog
        
        Argumentos:
            content (str): Conteúdo da entrada (o avanço realizado)
            source (str): Origem da entrada (arquivo, módulo, etc.)
            category (str): Categoria da entrada (development, feature, bugfix, etc.)
            importance (float): Importância da entrada (0.0 a 1.0)
            
        Retorna:
            bool: True se adicionou com sucesso, False caso contrário
        """
        # Gerar hash único para a entrada
        entry_hash = hashlib.md5(f"{content}_{source}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()
        
        # Criar entrada
        entry = {
            "id": entry_hash[:10],
            "timestamp": datetime.datetime.now().isoformat(),
            "content": content,
            "source": source,
            "category": category,
            "importance": importance,
            "reviewed": False,
            "integrated": False,
            "tags": []
        }
        
        # Adicionar à lista pendente de revisão
        self.changelog["pending_review"].append(entry)
        
        # Salvar changelog
        return self._save_changelog()
    
    def review_entries(self):
        """
        Lista todas as entradas pendentes de revisão
        
        Retorna:
            list: Lista de entradas pendentes
        """
        if not self.changelog["pending_review"]:
            print("Não há entradas pendentes de revisão.")
            return []
        
        print("\n=== ENTRADAS PENDENTES DE REVISÃO ===")
        for i, entry in enumerate(self.changelog["pending_review"]):
            print(f"{i+1}. [{entry['category']}] {entry['content'][:100]}...")
            print(f"   Fonte: {entry['source']}")
            print(f"   Importância: {entry['importance']}")
            print(f"   ID: {entry['id']}")
            print()
        
        return self.changelog["pending_review"]
    
    def approve_entry(self, entry_id, tags=None):
        """
        Aprova uma entrada para integração
        
        Argumentos:
            entry_id (str): ID da entrada a ser aprovada
            tags (list): Tags opcionais para categorizar a entrada
            
        Retorna:
            bool: True se aprovou com sucesso, False caso contrário
        """
        for i, entry in enumerate(self.changelog["pending_review"]):
            if entry["id"] == entry_id:
                # Marcar como revisada
                entry["reviewed"] = True
                
                # Adicionar tags se fornecidas
                if tags:
                    entry["tags"] = tags
                
                # Mover para entradas aprovadas
                self.changelog["entries"].append(entry)
                del self.changelog["pending_review"][i]
                
                # Salvar changelog
                result = self._save_changelog()
                if result:
                    print(f"✅ Entrada {entry_id} aprovada com sucesso")
                return result
        
        print(f"⚠️ Entrada com ID {entry_id} não encontrada.")
        return False
    
    def reject_entry(self, entry_id):
        """
        Remove uma entrada pendente de revisão
        
        Argumentos:
            entry_id (str): ID da entrada a ser rejeitada
            
        Retorna:
            bool: True se rejeitou com sucesso, False caso contrário
        """
        for i, entry in enumerate(self.changelog["pending_review"]):
            if entry["id"] == entry_id:
                del self.changelog["pending_review"][i]
                result = self._save_changelog()
                if result:
                    print(f"✅ Entrada {entry_id} rejeitada com sucesso")
                return result
        
        print(f"⚠️ Entrada com ID {entry_id} não encontrada.")
        return False
    
    def scan_file_for_progress(self, file_path):
        """
        Analisa um arquivo em busca de indicadores de progresso
        
        Argumentos:
            file_path (str): Caminho para o arquivo a ser escaneado
            
        Retorna:
            bool: True se encontrou progressos, False caso contrário
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se há comentários indicando progresso
            progress_found = False
            
            # Procurar por indicadores de progresso
            progress_matches = []
            for indicator in PROGRESS_INDICATORS:
                pattern = re.compile(f"(?i)[^a-z]({indicator})[^a-z]")
                matches = pattern.finditer(content)
                for match in matches:
                    # Pegar o contexto (100 caracteres antes e depois)
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 100)
                    context = content[start:end]
                    progress_matches.append((indicator, context))
                    progress_found = True
            
            if progress_found:
                for indicator, context in progress_matches:
                    # Adicionar ao changelog com importância média
                    self.add_entry(
                        content=f"Progresso detectado ({indicator}): {context}",
                        source=file_path,
                        category="auto-detected",
                        importance=0.5
                    )
                
                return True
            
            return False
                
        except Exception as e:
            print(f"⚠️ Erro ao escanear arquivo {file_path}: {str(e)}")
            return False
    
    def create_bios_q_proposal(self):
        """
        Cria uma proposta de atualização para a BIOS-Q baseada nas entradas aprovadas
        
        Retorna:
            str: Caminho para o arquivo de proposta ou None se houver erro
        """
        if not self.changelog.get("entries"):
            print("⚠️ Não há entradas aprovadas para integração.")
            return None
        
        if not self.bios_config:
            print("⚠️ Não foi possível carregar a configuração da BIOS-Q.")
            return None
        
        # Criar cópia do BIOS Config
        proposed_config = self.bios_config.copy()
        
        # Agrupar entradas por categoria
        entries_by_category = {}
        for entry in self.changelog["entries"]:
            if not entry.get("integrated", False):
                category = entry.get("category", "other")
                if category not in entries_by_category:
                    entries_by_category[category] = []
                entries_by_category[category].append(entry)
        
        # Verificar se há entradas não integradas
        entries_count = sum(len(entries) for entries in entries_by_category.values())
        if entries_count == 0:
            print("⚠️ Não há entradas pendentes de integração.")
            return None
            
        print(f"\n=== CRIANDO PROPOSTA DE ATUALIZAÇÃO ===")
        print(f"Entradas por categoria:")
        for category, entries in entries_by_category.items():
            print(f"- {category}: {len(entries)} entradas")
        
        # Atualizar métricas e progresso
        if "metrics" in proposed_config:
            metrics = proposed_config["metrics"]
            
            # Contar entradas por importância
            importance_sum = sum(entry.get("importance", 0) for cat in entries_by_category for entry in entries_by_category[cat])
            
            # Calcular média ponderada
            avg_importance = importance_sum / max(1, entries_count)
            
            print(f"\nMétricas a serem atualizadas:")
            print(f"- Importância média: {avg_importance:.2f}")
            
            # Incrementar métricas baseado na importância média
            for key in metrics:
                old_value = metrics[key]
                new_value = min(1.0, metrics[key] + avg_importance * 0.05)
                metrics[key] = new_value
                print(f"- {key}: {old_value:.2f} → {new_value:.2f}")
        
        # Atualizar timestamp
        proposed_config["timestamp_updated"] = datetime.datetime.now().isoformat()
        
        # Adicionar informações da versão 'Pear'
        if "version_info" not in proposed_config:
            proposed_config["version_info"] = {}
        
        proposed_config["version_info"]["changelog_version"] = VERSION
        proposed_config["version_info"]["changelog_name"] = VERSION_NAME
        proposed_config["version_info"]["last_update"] = datetime.datetime.now().isoformat()
        
        # Salvar proposta
        proposal_file = f"{STAGING_DIR}/bios_q_proposal.yaml"
        try:
            with open(proposal_file, 'w', encoding='utf-8') as f:
                yaml.dump(proposed_config, f, sort_keys=False, default_flow_style=False)
            
            print(f"\n✅ Proposta de atualização da BIOS-Q criada em {proposal_file}")
            return proposal_file
        except Exception as e:
            print(f"⚠️ Erro ao criar proposta de atualização: {str(e)}")
            return None
    
    def apply_proposal(self, backup=True):
        """
        Aplica a proposta de atualização à BIOS-Q
        
        Argumentos:
            backup (bool): Se deve criar backup antes de aplicar
            
        Retorna:
            bool: True se aplicou com sucesso, False caso contrário
        """
        proposal_file = f"{STAGING_DIR}/bios_q_proposal.yaml"
        if not os.path.exists(proposal_file):
            print("⚠️ Nenhuma proposta de atualização encontrada.")
            return False
        
        # Criar backup
        backup_file = None
        if backup:
            backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{HISTORY_DIR}/backups/bios_q_backup_{backup_time}.yaml"
            try:
                with open(BIOS_CONFIG, 'r', encoding='utf-8') as src, \
                     open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                print(f"✅ Backup da BIOS-Q criado em {backup_file}")
            except Exception as e:
                print(f"⚠️ Erro ao criar backup: {str(e)}")
                return False
        
        # Aplicar proposta
        try:
            with open(proposal_file, 'r', encoding='utf-8') as src, \
                 open(BIOS_CONFIG, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            # Marcar entradas como integradas
            integrated_count = 0
            for entry in self.changelog["entries"]:
                if not entry.get("integrated", False):
                    entry["integrated"] = True
                    entry["integration_date"] = datetime.datetime.now().isoformat()
                    integrated_count += 1
            
            # Adicionar ao histórico de integrações
            self.changelog["integration_history"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "entries_count": integrated_count,
                "backup_file": backup_file
            })
            
            # Salvar changelog
            self._save_changelog()
            
            print(f"✅ Proposta aplicada com sucesso à BIOS-Q")
            print(f"✅ {integrated_count} entradas marcadas como integradas")
            
            return True
        except Exception as e:
            print(f"⚠️ Erro ao aplicar proposta: {str(e)}")
            return False
    
    def scan_directory(self, directory, extensions=None):
        """
        Escaneia um diretório em busca de arquivos com indicadores de progresso
        
        Argumentos:
            directory (str): Diretório a ser escaneado
            extensions (list): Lista de extensões de arquivo a serem escaneadas
            
        Retorna:
            int: Número de arquivos com progresso encontrados
        """
        if extensions is None:
            extensions = ['.py', '.md', '.js', '.html', '.css', '.json', '.yaml', '.yml']
        
        try:
            count = 0
            total_files = 0
            path = Path(directory)
            
            print(f"🔍 Escaneando diretório: {directory}")
            
            for ext in extensions:
                for file_path in path.glob(f"**/*{ext}"):
                    total_files += 1
                    if self.scan_file_for_progress(str(file_path)):
                        count += 1
                        print(f"   ✅ Progresso detectado em: {file_path}")
            
            print(f"✓ Escaneamento concluído: {count} arquivos com progresso de {total_files} arquivos verificados")
            return count
        except Exception as e:
            print(f"⚠️ Erro ao escanear diretório {directory}: {str(e)}")
            return 0

# ========================================================================
# FUNÇÕES DE UTILIDADE PARA USO DIRETO
# ========================================================================

def register_progress(content, source, category="development", importance=0.5):
    """
    Função de utilidade para registrar progresso no changelog
    
    Argumentos:
        content (str): Descrição do progresso
        source (str): Origem do progresso (arquivo, módulo, etc.)
        category (str): Categoria do progresso
        importance (float): Importância do progresso (0.0 a 1.0)
        
    Exemplo:
        >>> register_progress("Implementada a função de login", "auth.py", "feature", 0.8)
    """
    changelog = QuantumChangelog()
    return changelog.add_entry(
        content=content,
        source=source,
        category=category,
        importance=importance
    )

def scan_for_progress():
    """
    Interface de linha de comando para escanear diretórios
    
    Esta função escaneia diretórios principais do projeto em busca de 
    indicadores de progresso e os registra automaticamente.
    """
    print("\n✧༺❀༻∞ EVA & GUARANI - Escaneando progresso quântico ∞༺❀༻✧\n")
    
    changelog = QuantumChangelog()
    
    # Escanear diretórios principais
    directories = ['core', 'modules', 'QUANTUM_PROMPTS', 'ui', 'tools', 'docs']
    total_progress = 0
    
    print("Diretórios a serem escaneados:")
    for directory in directories:
        if os.path.exists(directory):
            print(f"- {directory}")
    
    print("\nIniciando escaneamento...")
    for directory in directories:
        if os.path.exists(directory):
            progress = changelog.scan_directory(directory)
            total_progress += progress
    
    # Exibir entradas pendentes
    if total_progress > 0:
        print(f"\n✅ Total de arquivos com progresso detectado: {total_progress}")
        print("\nRevisando entradas pendentes...")
        changelog.review_entries()
    else:
        print("\n⚠️ Nenhum progresso detectado nos diretórios escaneados.")
    
    print("\n✧༺❀༻∞ EVA & GUARANI - Escaneamento concluído ∞༺❀༻✧\n")

def review_progress():
    """
    Interface de linha de comando para revisar progresso pendente
    
    Esta função permite revisar e aprovar/rejeitar entradas pendentes
    de forma interativa pela linha de comando.
    """
    print("\n✧༺❀༻∞ EVA & GUARANI - Revisando progresso quântico ∞༺❀༻✧\n")
    
    changelog = QuantumChangelog()
    entries = changelog.review_entries()
    
    if not entries:
        print("Não há entradas pendentes para revisar.")
        return
    
    print("\nOpções:")
    print("1. Aprovar todas as entradas")
    print("2. Aprovar entradas selecionadas")
    print("3. Rejeitar todas as entradas")
    print("4. Rejeitar entradas selecionadas")
    print("5. Sair sem fazer alterações")
    
    choice = input("\nEscolha uma opção (1-5): ")
    
    if choice == "1":
        for entry in entries:
            changelog.approve_entry(entry["id"])
        print("✅ Todas as entradas foram aprovadas.")
    
    elif choice == "2":
        print("Digite os números das entradas que deseja aprovar, separados por vírgula:")
        selections = input("> ")
        try:
            indices = [int(s.strip()) - 1 for s in selections.split(",")]
            for idx in indices:
                if 0 <= idx < len(entries):
                    changelog.approve_entry(entries[idx]["id"])
            print("✅ Entradas selecionadas foram aprovadas.")
        except Exception as e:
            print(f"⚠️ Erro ao processar seleção: {str(e)}")
    
    elif choice == "3":
        for entry in entries:
            changelog.reject_entry(entry["id"])
        print("✅ Todas as entradas foram rejeitadas.")
    
    elif choice == "4":
        print("Digite os números das entradas que deseja rejeitar, separados por vírgula:")
        selections = input("> ")
        try:
            indices = [int(s.strip()) - 1 for s in selections.split(",")]
            for idx in indices:
                if 0 <= idx < len(entries):
                    changelog.reject_entry(entries[idx]["id"])
            print("✅ Entradas selecionadas foram rejeitadas.")
        except Exception as e:
            print(f"⚠️ Erro ao processar seleção: {str(e)}")
    
    print("\n✧༺❀༻∞ EVA & GUARANI - Revisão concluída ∞༺❀༻✧\n")

def create_proposal():
    """
    Cria uma proposta de atualização para a BIOS-Q
    
    Esta função cria uma proposta de atualização baseada nas entradas
    aprovadas e pergunta se deve aplicá-la imediatamente.
    """
    print("\n✧༺❀༻∞ EVA & GUARANI - Criando proposta para BIOS-Q ∞༺❀༻✧\n")
    
    changelog = QuantumChangelog()
    proposal_file = changelog.create_bios_q_proposal()
    
    if proposal_file:
        print(f"\nProposta de atualização criada em {proposal_file}")
        print("⚠️ IMPORTANTE: Revise este arquivo antes de aplicá-lo à BIOS-Q.")
        
        choice = input("\nDeseja aplicar esta proposta agora? (s/n): ")
        if choice.lower() == "s":
            print("\nAplicando proposta...")
            changelog.apply_proposal()
    
    print("\n✧༺❀༻∞ EVA & GUARANI - Processo concluído ∞༺❀༻✧\n")

def create_documentation():
    """
    Cria documentação sobre a versão atual do sistema
    
    Esta função gera um arquivo de documentação com informações sobre
    a versão atual, recursos e instruções de uso.
    """
    print("\n✧༺❀༻∞ EVA & GUARANI - Criando documentação ∞༺❀༻✧\n")
    
    # Criar arquivo de documentação
    doc_file = f"{STAGING_DIR}/QUANTUM_CHANGELOG_DOCS.md"
    
    try:
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(f"""# Quantum Changelog - Versão {VERSION} "{VERSION_NAME}"

{QUANTUM_SIGNATURE}

## Sobre o Sistema

{VERSION_DESCRIPTION}

O Quantum Changelog é um sistema criado para capturar e preservar avanços importantes durante o 
desenvolvimento do projeto EVA & GUARANI. Ele funciona como uma "memória quântica" que preserva 
o contexto e os avanços, mesmo com os limites de contexto dos LLMs.

## Como Usar

### Detecção de Progressos

```bash
python core/quantum_changelog.py
# Escolha a opção 1 - Escanear diretórios
```

### Revisão com Interface Gráfica

```bash
# No Windows
start_quantum_review.bat

# Ou diretamente
python core/quantum_approval_ui.py
```

### Revisão pela Linha de Comando

```bash
python core/quantum_changelog.py
# Escolha a opção 2 - Revisar progresso pendente
```

### Criar Proposta para BIOS-Q

```bash
python core/quantum_changelog.py
# Escolha a opção 3 - Criar proposta de atualização
```

## Funcionalidades Principais

1. **Detecção Automática** - Encontra progressos no código sem intervenção manual
2. **Área de Staging** - Armazena mudanças em área segura antes da integração
3. **Interface Visual** - Permite revisar e aprovar mudanças de forma intuitiva
4. **Integração com BIOS-Q** - Atualiza métricas e configurações baseadas em progressos reais
5. **Backups Automáticos** - Cria backup antes de qualquer modificação

## Estrutura de Diretórios

```
staging/                     # Área de staging
├── quantum_changelog.json  # Registro de progressos
├── bios_q_proposal.yaml    # Proposta de atualização
├── history/                # Histórico de alterações
│   └── backups/            # Backups automáticos
└── QUANTUM_CHANGELOG_DOCS.md  # Esta documentação
```

## Princípios Quânticos Implementados

- **Preservação Evolutiva** - Backup quântico que mantém a essência permitindo transformação
- **Modularidade Consciente** - Entendimento profundo das partes e do todo
- **Cartografia Sistêmica** - Mapeamento preciso de conexões e potencialidades

{QUANTUM_SIGNATURE}
""")
        
        print(f"✅ Documentação criada em {doc_file}")
    except Exception as e:
        print(f"⚠️ Erro ao criar documentação: {str(e)}")

def main():
    """
    Função principal com menu interativo de opções
    
    Esta função apresenta um menu com as principais operações do sistema
    e permite ao usuário escolher a operação desejada.
    """
    print("\n✧༺❀༻∞ EVA & GUARANI - Quantum Changelog ∞༺❀༻✧\n")
    print(f"Versão {VERSION} - '{VERSION_NAME}'")
    print(f"{VERSION_DESCRIPTION}\n")
    
    print("MENU DE OPÇÕES:")
    print("1. Escanear diretórios por progresso")
    print("2. Revisar progresso pendente")
    print("3. Criar proposta de atualização")
    print("4. Aplicar proposta à BIOS-Q")
    print("5. Registrar progresso manualmente")
    print("6. Criar documentação do sistema")
    print("7. Sair")
    
    choice = input("\nEscolha uma opção (1-7): ")
    
    if choice == "1":
        scan_for_progress()
    elif choice == "2":
        review_progress()
    elif choice == "3":
        create_proposal()
    elif choice == "4":
        changelog = QuantumChangelog()
        if changelog.apply_proposal():
            print("✅ Proposta aplicada com sucesso à BIOS-Q.")
        else:
            print("⚠️ Não foi possível aplicar a proposta à BIOS-Q.")
    elif choice == "5":
        print("\n=== REGISTRAR PROGRESSO MANUALMENTE ===\n")
        content = input("Descrição do progresso: ")
        source = input("Origem (arquivo/módulo): ")
        category = input("Categoria (development, feature, bugfix, etc.): ") or "development"
        
        importance_str = input("Importância (baixa, média, alta ou valor de 0.0-1.0): ") or "0.5"
        importance = 0.5
        
        # Converter importância de texto para valor
        if importance_str.lower() == "baixa":
            importance = 0.3
        elif importance_str.lower() == "média":
            importance = 0.5
        elif importance_str.lower() == "alta":
            importance = 0.8
        else:
            try:
                importance = float(importance_str)
                importance = max(0.0, min(1.0, importance))  # Limitar entre 0 e 1
            except:
                importance = 0.5
        
        if register_progress(content, source, category, importance):
            print("✅ Progresso registrado com sucesso.")
        else:
            print("⚠️ Erro ao registrar progresso.")
    
    elif choice == "6":
        create_documentation()
    
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

# Inicializar quando executado diretamente
if __name__ == "__main__":
    # Se receber um argumento, executa a função correspondente
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "1":
            scan_for_progress()
        elif arg == "2":
            review_progress()
        elif arg == "3":
            create_proposal()
        elif arg == "4":
            QuantumChangelog().apply_proposal()
        elif arg == "5":
            # Registrar progresso interativo
            main()  # Usar menu para modo interativo
        elif arg == "6":
            create_documentation()
    else:
        # Sem argumentos, mostrar menu interativo
        main() 