#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Dynamic Roadmap and Quantum Prompt Manager
Version: 7.5
Created: 2025-03-26

This module implements a dynamic system that automatically updates roadmaps
and quantum prompts based on the current state of the project.
"""

import os
import sys
import time
import yaml
import json
import logging
import datetime
from tqdm import tqdm
from colorama import init, Fore, Style
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

# Initialize colorama
init()

# Configure logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/dynamic_roadmap.log"), logging.StreamHandler(sys.stdout)],
)


class QuantumRoadmapManager:
    def __init__(self):
        self.quantum_prompts_dir = "QUANTUM_PROMPTS"
        self.master_dir = os.path.join(self.quantum_prompts_dir, "MASTER")
        self.subsystems = ["CRONOS", "ATLAS", "NEXUS", "ETHIK"]
        self.platform_components = ["Web", "Telegram", "Desktop", "Mobile"]

        # Cross-reference tracking
        self.doc_references = {}
        self.implementation_files = {}

        # Implementation phases
        self.phases = [
            {
                "id": 1,
                "name": "Core API Development",
                "components": ["BIOS-Q Core", "REST API", "Documentation"],
                "timeline": "Q2 2024",
                "dependencies": [],
            },
            {
                "id": 2,
                "name": "Web Interface",
                "components": ["Dashboard", "Visualizations", "ATLAS Integration"],
                "timeline": "Q2-Q3 2024",
                "dependencies": [1],
            },
            {
                "id": 3,
                "name": "Telegram Bot",
                "components": ["Commands", "Core Integration", "Media Handling"],
                "timeline": "Q3 2024",
                "dependencies": [1],
            },
            {
                "id": 4,
                "name": "Enhanced Visualization",
                "components": ["Mycelial Network", "Data Flow", "Subsystem Connections"],
                "timeline": "Q3-Q4 2024",
                "dependencies": [2],
            },
            {
                "id": 5,
                "name": "Multi-Layered Documentation",
                "components": ["Visual Metaphors", "Interactive Guides", "Technical Docs"],
                "timeline": "Q4 2024",
                "dependencies": [2, 4],
            },
            {
                "id": 6,
                "name": "Cross-Platform Expansion",
                "components": ["Electron Desktop", "Mobile Web", "Integration SDK"],
                "timeline": "Q1 2025",
                "dependencies": [2, 3, 4],
            },
        ]

        # Critical documentation files
        self.documentation_files = [
            "BIOS-Q/docs/platform_integration.md",
            "QUANTUM_PROMPTS/MASTER/quantum_context.md",
            "BIOS-Q/README.md",
            "BIOS-Q/docs/api.md",
        ]

        # State tracking
        self.state_history = []
        self.current_state = {}

        # Ensure directories exist
        os.makedirs(self.master_dir, exist_ok=True)
        for subsystem in self.subsystems:
            os.makedirs(os.path.join(self.quantum_prompts_dir, subsystem), exist_ok=True)

    def calculate_completion(self, subsystem):
        subsystem_dir = os.path.join(self.quantum_prompts_dir, subsystem)
        if not os.path.exists(subsystem_dir):
            return 0.0

        total_files = 0
        implemented_files = 0

        for root, _, files in os.walk(subsystem_dir):
            for file in files:
                if file.endswith(".py"):
                    total_files += 1
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            if len(content.strip()) > 0:
                                implemented_files += 1

                                # Track implementation files for cross-referencing
                                self.implementation_files[file_path] = {
                                    "subsystem": subsystem,
                                    "last_modified": os.path.getmtime(file_path),
                                    "size": os.path.getsize(file_path),
                                }
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {e}")

        return (implemented_files / total_files * 100) if total_files > 0 else 0.0

    def calculate_phase_completion(self, phase_id):
        # In a real implementation, this would check actual components
        # For now, return mock values based on phase_id
        # Earlier phases are considered more complete
        if phase_id == 1:
            return 40.0  # Core API is 40% complete
        elif phase_id == 2:
            return 15.0  # Web interface is 15% complete
        else:
            return 5.0  # Other phases are 5% complete

    def scan_documentation_files(self):
        """Scan documentation files to build cross-references"""
        logging.info(
            f"{Fore.BLUE}Scanning documentation files for cross-references...{Style.RESET_ALL}"
        )

        self.doc_references = {}

        for doc_file in tqdm(self.documentation_files, desc="Analyzing documentation"):
            if not os.path.exists(doc_file):
                continue

            try:
                with open(doc_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract references to other documentation
                refs = set()
                for other_doc in self.documentation_files:
                    if other_doc == doc_file:
                        continue

                    # Check if the file name is mentioned
                    if os.path.basename(other_doc) in content:
                        refs.add(other_doc)

                # Extract references to implementation files
                impl_refs = set()
                for impl_file in self.implementation_files:
                    if os.path.basename(impl_file) in content:
                        impl_refs.add(impl_file)

                # Store references
                self.doc_references[doc_file] = {
                    "documentation_refs": list(refs),
                    "implementation_refs": list(impl_refs),
                    "last_modified": os.path.getmtime(doc_file),
                    "size": os.path.getsize(doc_file),
                }

            except Exception as e:
                logging.error(f"Error processing documentation file {doc_file}: {e}")

        logging.info(
            f"{Fore.GREEN}Documentation analysis complete. Found {len(self.doc_references)} files with references.{Style.RESET_ALL}"
        )

    def save_state(self):
        """Save the current state for comparison and tracking"""
        timestamp = datetime.datetime.now().isoformat()

        state = {
            "timestamp": timestamp,
            "subsystem_completion": {},
            "phase_completion": {},
            "documentation_files": self.doc_references,
            "implementation_files": self.implementation_files,
        }

        # Add completion data
        for subsystem in self.subsystems:
            state["subsystem_completion"][subsystem] = self.calculate_completion(subsystem)

        for phase in self.phases:
            state["phase_completion"][phase["id"]] = self.calculate_phase_completion(phase["id"])

        # Add to history
        self.state_history.append(state)

        # Update current state
        self.current_state = state

        # Save state to disk
        state_dir = os.path.join("logs", "states")
        os.makedirs(state_dir, exist_ok=True)

        state_file = os.path.join(state_dir, f"roadmap_state_{timestamp.replace(':', '-')}.json")

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        logging.info(f"{Fore.GREEN}Saved current state to {state_file}{Style.RESET_ALL}")

        return state_file

    def compare_with_previous_state(self):
        """Compare the current state with the previous one to detect changes"""
        if len(self.state_history) < 2:
            logging.warning("No previous state available for comparison")
            return None

        current = self.state_history[-1]
        previous = self.state_history[-2]

        changes = {
            "timestamp": datetime.datetime.now().isoformat(),
            "previous_timestamp": previous["timestamp"],
            "subsystem_changes": {},
            "phase_changes": {},
            "documentation_changes": {},
            "implementation_changes": {},
        }

        # Check subsystem completion changes
        for subsystem in self.subsystems:
            current_completion = current["subsystem_completion"].get(subsystem, 0.0)
            previous_completion = previous["subsystem_completion"].get(subsystem, 0.0)

            if current_completion != previous_completion:
                changes["subsystem_changes"][subsystem] = {
                    "previous": previous_completion,
                    "current": current_completion,
                    "change": current_completion - previous_completion,
                }

        # Check phase completion changes
        for phase in self.phases:
            phase_id = phase["id"]
            current_completion = current["phase_completion"].get(str(phase_id), 0.0)
            previous_completion = previous["phase_completion"].get(str(phase_id), 0.0)

            if current_completion != previous_completion:
                changes["phase_changes"][str(phase_id)] = {
                    "name": phase["name"],
                    "previous": previous_completion,
                    "current": current_completion,
                    "change": current_completion - previous_completion,
                }

        # Check documentation changes
        current_docs = set(current["documentation_files"].keys())
        previous_docs = set(previous["documentation_files"].keys())

        # New documentation files
        for doc in current_docs - previous_docs:
            changes["documentation_changes"][doc] = {"type": "added"}

        # Removed documentation files
        for doc in previous_docs - current_docs:
            changes["documentation_changes"][doc] = {"type": "removed"}

        # Modified documentation files
        for doc in current_docs & previous_docs:
            current_modified = current["documentation_files"][doc]["last_modified"]
            previous_modified = previous["documentation_files"][doc]["last_modified"]

            if current_modified != previous_modified:
                current_refs = set(
                    current["documentation_files"][doc].get("documentation_refs", [])
                )
                previous_refs = set(
                    previous["documentation_files"][doc].get("documentation_refs", [])
                )

                changes["documentation_changes"][doc] = {
                    "type": "modified",
                    "new_references": list(current_refs - previous_refs),
                    "removed_references": list(previous_refs - current_refs),
                }

        # Save changes to disk
        changes_dir = os.path.join("logs", "changes")
        os.makedirs(changes_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        changes_file = os.path.join(changes_dir, f"roadmap_changes_{timestamp}.json")

        with open(changes_file, "w", encoding="utf-8") as f:
            json.dump(changes, f, indent=2)

        logging.info(f"{Fore.GREEN}Saved changes analysis to {changes_file}{Style.RESET_ALL}")

        return changes

    def update_roadmap(self):
        logging.info(f"{Fore.GREEN}Updating roadmap...{Style.RESET_ALL}")

        try:
            # Scan documentation for cross-referencing
            self.scan_documentation_files()

            # Calculate completion for each subsystem
            subsystem_completion = {}
            for subsystem in tqdm(self.subsystems, desc="Analyzing subsystems"):
                subsystem_completion[subsystem] = self.calculate_completion(subsystem)
                logging.info(f"{subsystem} completion: {subsystem_completion[subsystem]:.1f}%")

            # Calculate completion for each phase
            phase_completion = {}
            for phase in tqdm(self.phases, desc="Analyzing implementation phases"):
                phase_completion[phase["id"]] = self.calculate_phase_completion(phase["id"])
                logging.info(
                    f"Phase {phase['id']} ({phase['name']}) completion: {phase_completion[phase['id']]:.1f}%"
                )

            # Update roadmap.md
            roadmap_path = os.path.join(self.master_dir, "roadmap.md")
            with open(roadmap_path, "w") as f:
                f.write("# EVA & GUARANI - Implementation Roadmap\n\n")
                f.write(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # Subsystem section
                f.write("## Subsystems\n\n")
                for subsystem in self.subsystems:
                    f.write(f"### {subsystem}\n")
                    f.write(f"Implementation: {subsystem_completion[subsystem]:.1f}%\n\n")

                # Platform integration section
                f.write("## Platform Integration\n\n")
                f.write("```\n")
                f.write("                      ┌─────────────────┐\n")
                f.write("                      │   BIOS-Q Core   │\n")
                f.write("                      │  (Python/API)   │\n")
                f.write("                      └────────┬────────┘\n")
                f.write("                               │\n")
                f.write("                ┌──────────────┴───────────────┐\n")
                f.write("                │                              │\n")
                f.write("        ┌───────┴────────┐            ┌───────┴────────┐\n")
                f.write("        │  Web Frontend  │            │  Telegram Bot  │\n")
                f.write("        │   (JS/React)   │            │    (Python)    │\n")
                f.write("        └───────┬────────┘            └───────┬────────┘\n")
                f.write("                │                              │\n")
                f.write("      ┌─────────┴──────────┐          ┌───────┴────────┐\n")
                f.write("      │ Browser (All OS)   │          │ Telegram App   │\n")
                f.write("      │ (Web Application)  │          │ (All Platforms)│\n")
                f.write("      └────────────────────┘          └────────────────┘\n")
                f.write("```\n\n")

                # Implementation phases
                f.write("## Implementation Phases\n\n")
                f.write("| Phase | Name | Components | Timeline | Progress | Dependencies |\n")
                f.write("|-------|------|------------|----------|----------|-------------|\n")

                for phase in self.phases:
                    components = ", ".join(phase["components"])
                    dependencies = (
                        ", ".join([str(dep) for dep in phase["dependencies"]])
                        if phase["dependencies"]
                        else "None"
                    )
                    f.write(
                        f"| {phase['id']} | {phase['name']} | {components} | {phase['timeline']} | {phase_completion[phase['id']]:.1f}% | {dependencies} |\n"
                    )

                f.write("\n")

                # Communication strategy
                f.write("## Communication Strategy\n\n")
                f.write("### 1. Conceptual Map Visualization\n")
                f.write("- Interactive visualization of the mycelial network\n")
                f.write("- Show the quantum connections between CRONOS, ATLAS, NEXUS and ETHIK\n")
                f.write("- Visualize data flow through the system\n\n")

                f.write("### 2. ATLAS-First Implementation\n")
                f.write("- ATLAS component focuses on 'systemic cartography'\n")
                f.write("- Foundation of the user-facing experience\n")
                f.write("- Allow users to explore the project's structure visually\n\n")

                f.write("### 3. Multi-Layered Documentation\n")
                f.write(
                    "- Layer 1: Simple visual metaphors (mycelium network, quantum connections)\n"
                )
                f.write("- Layer 2: Interactive demonstrations of core capabilities\n")
                f.write("- Layer 3: Technical documentation with progressive disclosure\n\n")

                # Documentation Cross-References Section
                f.write("## Documentation References\n\n")
                f.write("| Document | References | Implementation Files |\n")
                f.write("|----------|------------|---------------------|\n")

                for doc_file, refs in self.doc_references.items():
                    doc_refs = ", ".join(
                        [os.path.basename(r) for r in refs.get("documentation_refs", [])]
                    )
                    impl_refs = ", ".join(
                        [os.path.basename(r) for r in refs.get("implementation_refs", [])]
                    )

                    if not doc_refs:
                        doc_refs = "None"
                    if not impl_refs:
                        impl_refs = "None"

                    f.write(f"| {os.path.basename(doc_file)} | {doc_refs} | {impl_refs} |\n")

            # Update quantum_prompt.txt
            prompt_path = "quantum_prompt.txt"
            with open(prompt_path, "w") as f:
                f.write("# EVA & GUARANI - Quantum Prompt v7.5\n\n")

                f.write("## Implementation Status:\n")

                f.write("### Subsystems:\n")
                for subsystem in self.subsystems:
                    f.write(f"{subsystem}: {subsystem_completion[subsystem]:.1f}%\n")

                f.write("\n### Integration Phases:\n")
                for phase in self.phases:
                    f.write(
                        f"Phase {phase['id']} ({phase['name']}): {phase_completion[phase['id']]:.1f}%\n"
                    )

                f.write("\n### Primary Platforms:\n")
                f.write("- Web Application (React/FastAPI)\n")
                f.write("- Telegram Bot Integration\n")
                f.write("- Future: Desktop & Mobile\n")

                # Add documentation references
                f.write("\n### Document Cross-References:\n")
                for doc_file, refs in self.doc_references.items():
                    doc_basename = os.path.basename(doc_file)
                    doc_refs = [os.path.basename(r) for r in refs.get("documentation_refs", [])]
                    if doc_refs:
                        f.write(f"{doc_basename} references: {', '.join(doc_refs)}\n")

            # Save state after update
            self.save_state()

            # Compare with previous state, if available
            if len(self.state_history) > 1:
                self.compare_with_previous_state()

            logging.info(f"{Fore.GREEN}Roadmap updated successfully!{Style.RESET_ALL}")

        except Exception as e:
            logging.error(f"{Fore.RED}Error updating roadmap: {e}{Style.RESET_ALL}")

    def export_cross_references(self, output_file="docs/cross_references.md"):
        """Export cross-references to a markdown document"""
        logging.info(f"{Fore.BLUE}Exporting cross-references...{Style.RESET_ALL}")

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("# EVA & GUARANI - Documentation Cross-References\n\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # Document to document references
                f.write("## Document to Document References\n\n")
                f.write("```mermaid\n")
                f.write("graph TD\n")

                # Add nodes
                for doc_file in self.doc_references:
                    doc_id = os.path.basename(doc_file).replace(".", "_")
                    doc_name = os.path.basename(doc_file)
                    f.write(f"    {doc_id}[{doc_name}]\n")

                # Add relationships
                for doc_file, refs in self.doc_references.items():
                    source_id = os.path.basename(doc_file).replace(".", "_")

                    for ref in refs.get("documentation_refs", []):
                        target_id = os.path.basename(ref).replace(".", "_")
                        f.write(f"    {source_id} --> {target_id}\n")

                f.write("```\n\n")

                # Document to implementation references
                f.write("## Document to Implementation References\n\n")

                for doc_file, refs in self.doc_references.items():
                    impl_refs = refs.get("implementation_refs", [])
                    if impl_refs:
                        f.write(f"### {os.path.basename(doc_file)}\n\n")
                        f.write("References the following implementation files:\n\n")

                        for impl in impl_refs:
                            f.write(f"- `{impl}`\n")

                        f.write("\n")

                # Add signature
                f.write("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

            logging.info(f"{Fore.GREEN}Cross-references exported to {output_file}{Style.RESET_ALL}")

        except Exception as e:
            logging.error(f"{Fore.RED}Error exporting cross-references: {e}{Style.RESET_ALL}")


def main():
    manager = QuantumRoadmapManager()
    manager.update_roadmap()
    manager.export_cross_references()

    # Additional information
    logging.info(f"{Fore.CYAN}Roadmap update complete.{Style.RESET_ALL}")
    logging.info(
        f"{Fore.CYAN}To access the state preservation system, use: python -m BIOS-Q.bios_q.cronos.state_preservation{Style.RESET_ALL}"
    )


if __name__ == "__main__":
    main()
