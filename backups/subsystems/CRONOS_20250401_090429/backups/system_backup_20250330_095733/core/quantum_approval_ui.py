#!/usr/bin/env python3
"""
Quantum Approval UI - Interface para aprovação de mudanças do Quantum Changelog
Permite revisar e aprovar alterações sugeridas pelo sistema de forma visual e segura.
"""

import os
import sys
import json
import datetime
import hashlib
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path

# Diretórios
STAGING_DIR = "staging"
CHANGELOG_FILE = f"{STAGING_DIR}/quantum_changelog.json"
HISTORY_DIR = f"{STAGING_DIR}/history"
BACKUP_DIR = f"{HISTORY_DIR}/backups"
QUANTUM_PROMPT = "QUANTUM_PROMPTS/core_principles.md"
BIOS_CONFIG = "config/ethik_chain_core.yaml"

# Constantes
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
QUANTUM_SIGNATURE = "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"


class QuantumApprovalUI:
    """Interface gráfica para aprovação de mudanças do Quantum Changelog"""

    def __init__(self, root):
        """Inicializa a interface com a janela principal"""
        self.root = root
        self.root.title("EVA & GUARANI - Quantum Approval System")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(800, 600)

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Accept.TButton", background="#4CAF50", foreground="black")
        self.style.configure("Reject.TButton", background="#f44336", foreground="black")
        self.style.configure("TLabel", font=("Arial", 11), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#f0f0f0")
        self.style.configure(
            "Quantum.TLabel", font=("Arial", 12), foreground="#6200ea", background="#f0f0f0"
        )

        # Variáveis
        self.entries = []
        self.current_entry_index = 0
        self.pending_changes = []
        self.selected_entries = set()
        self.changelog_data = None

        # Carregar dados
        self.load_changelog()

        # Criar interface
        self.create_ui()

    def load_changelog(self):
        """Carrega os dados do changelog"""
        try:
            # Garantir que os diretórios existam
            os.makedirs(STAGING_DIR, exist_ok=True)
            os.makedirs(HISTORY_DIR, exist_ok=True)
            os.makedirs(BACKUP_DIR, exist_ok=True)

            if os.path.exists(CHANGELOG_FILE):
                with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
                    self.changelog_data = json.load(f)

                # Extrair entradas pendentes
                self.entries = self.changelog_data.get("pending_review", [])

                # Ordenar por importância
                self.entries.sort(key=lambda x: x.get("importance", 0), reverse=True)
            else:
                self.changelog_data = {
                    "version": "1.0.0",
                    "last_updated": datetime.datetime.now().isoformat(),
                    "entries": [],
                    "pending_review": [],
                    "integration_history": [],
                }
                self.entries = []
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o changelog: {str(e)}")
            self.entries = []

    def save_changelog(self):
        """Salva as alterações no changelog"""
        try:
            if self.changelog_data:
                self.changelog_data["last_updated"] = datetime.datetime.now().isoformat()

                with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.changelog_data, f, indent=4, ensure_ascii=False)

                return True
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o changelog: {str(e)}")

        return False

    def create_ui(self):
        """Cria os elementos da interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Label(title_frame, text="EVA & GUARANI", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Label(title_frame, text="Quantum Approval System", style="Quantum.TLabel").pack(
            side=tk.LEFT, padx=10
        )

        # Informações
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.pending_label = ttk.Label(info_frame, text=f"Entradas pendentes: {len(self.entries)}")
        self.pending_label.pack(side=tk.LEFT)

        # Botões superiores
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Aprovar Selecionadas", command=self.approve_selected).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Rejeitar Selecionadas", command=self.reject_selected).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="Criar Proposta BIOS-Q", command=self.create_biosq_proposal
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Criar Backup", command=self.create_backup).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Atualizar", command=self.reload_data).pack(
            side=tk.RIGHT, padx=5
        )

        # Painel de lista e detalhes
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Criar painel dividido
        pane = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Lista de entradas
        list_frame = ttk.Frame(pane)
        pane.add(list_frame, weight=1)

        list_label = ttk.Label(list_frame, text="Entradas pendentes", style="Header.TLabel")
        list_label.pack(fill=tk.X, padx=5, pady=5)

        # Criar Treeview
        columns = ("id", "category", "importance", "source")
        self.entry_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        # Configurar cabeçalhos
        self.entry_tree.heading("id", text="ID")
        self.entry_tree.heading("category", text="Categoria")
        self.entry_tree.heading("importance", text="Importância")
        self.entry_tree.heading("source", text="Origem")

        # Configurar colunas
        self.entry_tree.column("id", width=100, anchor="w")
        self.entry_tree.column("category", width=100, anchor="w")
        self.entry_tree.column("importance", width=80, anchor="center")
        self.entry_tree.column("source", width=200, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.entry_tree.yview)
        self.entry_tree.configure(yscroll=scrollbar.set)

        # Posicionar elementos
        self.entry_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Vincular evento de seleção
        self.entry_tree.bind("<<TreeviewSelect>>", self.on_entry_selected)

        # Painel de detalhes
        details_frame = ttk.Frame(pane)
        pane.add(details_frame, weight=2)

        details_label = ttk.Label(details_frame, text="Detalhes da entrada", style="Header.TLabel")
        details_label.pack(fill=tk.X, padx=5, pady=5)

        # Área de informações
        info_details = ttk.Frame(details_frame)
        info_details.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(info_details, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_details, text="Categoria:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_details, text="Importância:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        ttk.Label(info_details, text="Origem:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_details, text="Data:").grid(row=4, column=0, sticky="w", padx=5, pady=2)

        self.id_label = ttk.Label(info_details, text="-")
        self.id_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.category_label = ttk.Label(info_details, text="-")
        self.category_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        self.importance_label = ttk.Label(info_details, text="-")
        self.importance_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        self.source_label = ttk.Label(info_details, text="-")
        self.source_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        self.date_label = ttk.Label(info_details, text="-")
        self.date_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        # Área de conteúdo
        ttk.Label(details_frame, text="Conteúdo:").pack(fill=tk.X, padx=5, pady=5, anchor="w")

        self.content_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=10)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Botões de aprovação/rejeição
        action_frame = ttk.Frame(details_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(
            action_frame, text="Aprovar", command=self.approve_current, style="Accept.TButton"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            action_frame, text="Rejeitar", command=self.reject_current, style="Reject.TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Barra de status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        self.status_label = ttk.Label(status_frame, text=QUANTUM_SIGNATURE)
        self.status_label.pack(side=tk.LEFT)

        # Popular a lista
        self.populate_entry_list()

    def populate_entry_list(self):
        """Popula a lista de entradas pendentes"""
        # Limpar lista atual
        for item in self.entry_tree.get_children():
            self.entry_tree.delete(item)

        # Adicionar entradas
        for entry in self.entries:
            entry_id = entry.get("id", "")
            category = entry.get("category", "")
            importance = f"{float(entry.get('importance', 0)) * 100:.0f}%"
            source = entry.get("source", "")

            item_id = self.entry_tree.insert(
                "", "end", values=(entry_id, category, importance, source)
            )

            # Marcar como selecionado se estiver na lista
            if entry_id in self.selected_entries:
                self.entry_tree.selection_add(item_id)

        # Atualizar rótulo
        self.pending_label.config(text=f"Entradas pendentes: {len(self.entries)}")

    def on_entry_selected(self, event):
        """Manipula a seleção de uma entrada na lista"""
        selection = self.entry_tree.selection()
        if selection:
            item = selection[0]
            entry_id = self.entry_tree.item(item, "values")[0]

            # Encontrar entrada correspondente
            entry = next((e for e in self.entries if e.get("id") == entry_id), None)
            if entry:
                # Preencher detalhes
                self.id_label.config(text=entry.get("id", "-"))
                self.category_label.config(text=entry.get("category", "-"))
                self.importance_label.config(text=f"{float(entry.get('importance', 0)) * 100:.0f}%")
                self.source_label.config(text=entry.get("source", "-"))

                # Converter timestamp para formato legível
                timestamp = entry.get("timestamp", "")
                if timestamp:
                    try:
                        dt = datetime.datetime.fromisoformat(timestamp)
                        self.date_label.config(text=dt.strftime("%d/%m/%Y %H:%M:%S"))
                    except:
                        self.date_label.config(text=timestamp)
                else:
                    self.date_label.config(text="-")

                # Preencher conteúdo
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(tk.END, entry.get("content", ""))

    def approve_current(self):
        """Aprova a entrada atualmente selecionada"""
        selection = self.entry_tree.selection()
        if selection:
            item = selection[0]
            entry_id = self.entry_tree.item(item, "values")[0]

            self.approve_entry(entry_id)
            self.populate_entry_list()

    def reject_current(self):
        """Rejeita a entrada atualmente selecionada"""
        selection = self.entry_tree.selection()
        if selection:
            item = selection[0]
            entry_id = self.entry_tree.item(item, "values")[0]

            self.reject_entry(entry_id)
            self.populate_entry_list()

    def approve_entry(self, entry_id):
        """Aprova uma entrada específica e a move para entradas aprovadas"""
        for i, entry in enumerate(self.entries):
            if entry.get("id") == entry_id:
                # Marcar como revisada
                entry["reviewed"] = True

                # Mover para entradas aprovadas
                self.changelog_data["entries"].append(entry)

                # Remover da lista pendente
                del self.entries[i]

                # Remover da seleção
                if entry_id in self.selected_entries:
                    self.selected_entries.remove(entry_id)

                # Salvar alterações
                self.save_changelog()

                # Atualizar status
                self.status_label.config(text=f"Entrada {entry_id} aprovada.")

                return True

        return False

    def reject_entry(self, entry_id):
        """Rejeita uma entrada específica e a remove do changelog"""
        for i, entry in enumerate(self.entries):
            if entry.get("id") == entry_id:
                # Remover da lista pendente
                del self.entries[i]

                # Remover da seleção
                if entry_id in self.selected_entries:
                    self.selected_entries.remove(entry_id)

                # Salvar alterações
                self.save_changelog()

                # Atualizar status
                self.status_label.config(text=f"Entrada {entry_id} rejeitada.")

                return True

        return False

    def approve_selected(self):
        """Aprova todas as entradas selecionadas"""
        selection = self.entry_tree.selection()
        if not selection:
            messagebox.showinfo("Informação", "Nenhuma entrada selecionada.")
            return

        count = 0
        for item in selection:
            entry_id = self.entry_tree.item(item, "values")[0]
            if self.approve_entry(entry_id):
                count += 1

        if count > 0:
            messagebox.showinfo("Informação", f"{count} entradas aprovadas com sucesso.")
            self.populate_entry_list()

    def reject_selected(self):
        """Rejeita todas as entradas selecionadas"""
        selection = self.entry_tree.selection()
        if not selection:
            messagebox.showinfo("Informação", "Nenhuma entrada selecionada.")
            return

        count = 0
        for item in selection:
            entry_id = self.entry_tree.item(item, "values")[0]
            if self.reject_entry(entry_id):
                count += 1

        if count > 0:
            messagebox.showinfo("Informação", f"{count} entradas rejeitadas com sucesso.")
            self.populate_entry_list()

    def create_biosq_proposal(self):
        """Cria uma proposta de atualização para a BIOS-Q"""
        if not self.changelog_data.get("entries"):
            messagebox.showinfo("Informação", "Não há entradas aprovadas para criar uma proposta.")
            return

        try:
            import yaml

            # Verificar se a BIOS-Q existe
            if not os.path.exists(BIOS_CONFIG):
                messagebox.showerror(
                    "Erro", f"Arquivo de configuração da BIOS-Q não encontrado: {BIOS_CONFIG}"
                )
                return

            # Carregar configuração da BIOS-Q
            with open(BIOS_CONFIG, "r", encoding="utf-8") as f:
                bios_config = yaml.safe_load(f)

            # Criar backup antes de modificar
            backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{BACKUP_DIR}/bios_q_backup_{backup_time}.yaml"

            os.makedirs(os.path.dirname(backup_file), exist_ok=True)

            with (
                open(BIOS_CONFIG, "r", encoding="utf-8") as src,
                open(backup_file, "w", encoding="utf-8") as dst,
            ):
                dst.write(src.read())

            # Modificar a configuração
            # Agrupar entradas por categoria
            entries_by_category = {}
            for entry in self.changelog_data["entries"]:
                if not entry.get("integrated", False):
                    category = entry.get("category", "other")
                    if category not in entries_by_category:
                        entries_by_category[category] = []
                    entries_by_category[category].append(entry)

            # Atualizar métricas
            if "metrics" in bios_config:
                metrics = bios_config["metrics"]

                # Calcular média ponderada de importância
                importance_sum = sum(
                    entry.get("importance", 0)
                    for cat in entries_by_category
                    for entry in entries_by_category[cat]
                )
                entries_count = sum(len(entries) for entries in entries_by_category.values())

                if entries_count > 0:
                    avg_importance = importance_sum / entries_count

                    # Incrementar métricas
                    for key in metrics:
                        metrics[key] = min(1.0, metrics[key] + avg_importance * 0.05)

            # Atualizar timestamp
            bios_config["timestamp_updated"] = datetime.datetime.now().isoformat()

            # Salvar proposta
            proposal_file = f"{STAGING_DIR}/bios_q_proposal.yaml"
            with open(proposal_file, "w", encoding="utf-8") as f:
                yaml.dump(bios_config, f, sort_keys=False, default_flow_style=False)

            # Verificar se deve aplicar diretamente
            if messagebox.askyesno(
                "Proposta Criada",
                f"Proposta criada com sucesso em {proposal_file}.\n\n"
                f"Deseja aplicá-la à BIOS-Q agora?",
            ):
                # Aplicar proposta
                with (
                    open(proposal_file, "r", encoding="utf-8") as src,
                    open(BIOS_CONFIG, "w", encoding="utf-8") as dst,
                ):
                    dst.write(src.read())

                # Marcar entradas como integradas
                for entry in self.changelog_data["entries"]:
                    if not entry.get("integrated", False):
                        entry["integrated"] = True
                        entry["integration_date"] = datetime.datetime.now().isoformat()

                # Adicionar ao histórico
                self.changelog_data["integration_history"].append(
                    {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "entries_count": entries_count,
                        "backup_file": backup_file,
                    }
                )

                # Salvar changelog
                self.save_changelog()

                messagebox.showinfo("Sucesso", "Proposta aplicada com sucesso à BIOS-Q.")
            else:
                messagebox.showinfo(
                    "Informação",
                    f"Proposta salva em {proposal_file}.\n"
                    f"Você pode aplicá-la manualmente mais tarde.",
                )

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar proposta: {str(e)}")

    def create_backup(self):
        """Cria um backup da BIOS-Q e changelog"""
        try:
            backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Backup da BIOS-Q
            if os.path.exists(BIOS_CONFIG):
                bios_backup = f"{BACKUP_DIR}/bios_q_backup_{backup_time}.yaml"
                os.makedirs(os.path.dirname(bios_backup), exist_ok=True)

                with (
                    open(BIOS_CONFIG, "r", encoding="utf-8") as src,
                    open(bios_backup, "w", encoding="utf-8") as dst,
                ):
                    dst.write(src.read())

            # Backup do prompt quântico
            if os.path.exists(QUANTUM_PROMPT):
                prompt_backup = f"{BACKUP_DIR}/quantum_prompt_backup_{backup_time}.md"

                with (
                    open(QUANTUM_PROMPT, "r", encoding="utf-8") as src,
                    open(prompt_backup, "w", encoding="utf-8") as dst,
                ):
                    dst.write(src.read())

            # Backup do changelog
            changelog_backup = f"{BACKUP_DIR}/changelog_backup_{backup_time}.json"

            with (
                open(CHANGELOG_FILE, "r", encoding="utf-8") as src,
                open(changelog_backup, "w", encoding="utf-8") as dst,
            ):
                dst.write(src.read())

            messagebox.showinfo("Sucesso", f"Backup criado com sucesso em {BACKUP_DIR}")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar backup: {str(e)}")

    def reload_data(self):
        """Recarrega os dados do changelog"""
        self.load_changelog()
        self.populate_entry_list()
        messagebox.showinfo("Sucesso", "Dados recarregados com sucesso.")


def main():
    """Função principal para iniciar a interface"""
    root = tk.Tk()
    app = QuantumApprovalUI(root)

    # Ícone do sistema (se disponível)
    try:
        root.iconbitmap("tools/assets/quantum_icon.ico")
    except:
        pass

    # Iniciar loop da interface
    root.mainloop()


if __name__ == "__main__":
    main()
