#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Dynamic Roadmap and Quantum Prompt Manager
Version: 8.0
Created: 2025-03-30

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
import asyncio
import websockets
import git
from tqdm import tqdm
from colorama import init, Fore, Style
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from aiohttp import web
from ethik import EthicalValidator
from cronos import StatePreserver
from atlas import Visualizer
from nexus import Analyzer

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

        # Initialize subsystems
        self.ethical_validator = EthicalValidator()
        self.state_preserver = StatePreserver()
        self.visualizer = Visualizer()
        self.analyzer = Analyzer()

        # WebSocket clients
        self.clients = set()

        # Git integration
        self.repo = git.Repo(os.getcwd())

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

        # Initialize WebSocket server
        self.app = web.Application()
        self.app.router.add_get("/ws", self.websocket_handler)

        # Ensure directories exist
        os.makedirs(self.master_dir, exist_ok=True)
        for subsystem in self.subsystems:
            os.makedirs(os.path.join(self.quantum_prompts_dir, subsystem), exist_ok=True)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.clients.add(ws)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    # Handle incoming messages
                    data = json.loads(msg.data)
                    await self.handle_ws_message(ws, data)
        finally:
            self.clients.remove(ws)

        return ws

    async def broadcast_update(self, update_type: str, data: dict):
        """Broadcast updates to all connected clients"""
        message = json.dumps(
            {"type": update_type, "data": data, "timestamp": datetime.datetime.now().isoformat()}
        )
        for client in self.clients:
            await client.send_str(message)

    async def handle_ws_message(self, ws, data):
        """Handle incoming WebSocket messages"""
        msg_type = data.get("type")
        if msg_type == "get_status":
            await ws.send_json({"type": "status", "data": self.current_state})
        elif msg_type == "request_update":
            await self.update_roadmap()

    async def update_roadmap(self):
        """Enhanced update_roadmap with real-time updates and ethical validation"""
        try:
            # Ethical validation
            validation_result = await self.ethical_validator.validate_state(self.current_state)
            if not validation_result.is_valid:
                logging.error(f"Ethical validation failed: {validation_result.message}")
                return

            # Update state
            new_state = await self.calculate_new_state()

            # Preserve state with CRONOS
            await self.state_preserver.save_state(new_state)

            # Generate visualization with ATLAS
            visualization = await self.visualizer.create_visualization(new_state)

            # Analyze changes with NEXUS
            analysis = await self.analyzer.analyze_changes(self.current_state, new_state)

            # Update current state
            self.current_state = new_state

            # Broadcast updates
            await self.broadcast_update(
                "state_update",
                {"state": new_state, "visualization": visualization, "analysis": analysis},
            )

            # Update Git
            self.update_git_state()

            logging.info("Roadmap updated successfully")

        except Exception as e:
            logging.error(f"Error updating roadmap: {str(e)}")
            await self.broadcast_update("error", {"message": str(e)})

    def update_git_state(self):
        """Update Git repository with new state"""
        try:
            # Stage changes
            self.repo.index.add(
                [
                    "QUANTUM_PROMPTS/MASTER/quantum_roadmap.md",
                    "QUANTUM_PROMPTS/MASTER/quantum_context.md",
                ]
            )

            # Create commit
            self.repo.index.commit(f"Update quantum roadmap - {datetime.datetime.now()}")

            logging.info("Git state updated successfully")
        except Exception as e:
            logging.error(f"Error updating git state: {str(e)}")

    async def calculate_new_state(self):
        """Calculate new state with progress indicators"""
        new_state = {
            "version": "8.0",
            "last_updated": datetime.datetime.now().isoformat(),
            "subsystems": {},
            "phases": {},
            "ethical_metrics": await self.ethical_validator.calculate_metrics(),
            "visualization_metrics": await self.visualizer.calculate_metrics(),
            "analysis_metrics": await self.analyzer.calculate_metrics(),
        }

        # Calculate subsystem completion
        for subsystem in self.subsystems:
            completion = await self.calculate_completion(subsystem)
            new_state["subsystems"][subsystem] = {
                "completion": completion,
                "status": "active" if completion > 0 else "pending",
                "metrics": await self.analyzer.calculate_subsystem_metrics(subsystem),
            }

        # Calculate phase completion
        for phase in self.phases:
            completion = await self.calculate_phase_completion(phase["id"])
            new_state["phases"][phase["id"]] = {
                "completion": completion,
                "status": (
                    "completed"
                    if completion == 1
                    else "in_progress" if completion > 0 else "pending"
                ),
                "metrics": await self.analyzer.calculate_phase_metrics(phase["id"]),
            }

        return new_state

    async def start(self):
        """Start the WebSocket server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8080)
        await site.start()
        logging.info("WebSocket server started on ws://localhost:8080/ws")

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


async def main():
    """Main entry point"""
    manager = QuantumRoadmapManager()
    await manager.start()

    try:
        while True:
            await asyncio.sleep(60)  # Update every minute
            await manager.update_roadmap()
    except KeyboardInterrupt:
        logging.info("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
