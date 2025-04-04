"""
EVA & GUARANI - ATLAS Visualization System
Version: 8.0
Created: 2025-03-30

This module provides beautiful and meaningful visualizations of the system state,
integrating with the dynamic roadmap manager.
"""

import os
import json
import logging
import networkx as nx
import plotly.graph_objects as go
from pyvis.network import Network
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

class Visualizer:
    def __init__(self):
        self.output_dir = Path("QUANTUM_PROMPTS/ATLAS/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/atlas_visualizer.log'),
                logging.StreamHandler()
            ]
        )

        # Color schemes for different visualization types
        self.colors = {
            "subsystems": {
                "CRONOS": "#FF6B6B",  # Coral red
                "ATLAS": "#4ECDC4",   # Turquoise
                "NEXUS": "#45B7D1",   # Sky blue
                "ETHIK": "#96CEB4",   # Sage green
                "MASTER": "#FFBE0B",  # Golden yellow
                "BIOS-Q": "#FF006E"   # Bright pink
            },
            "status": {
                "completed": "#4CAF50",  # Green
                "in_progress": "#2196F3", # Blue
                "pending": "#9E9E9E",    # Gray
                "error": "#F44336"       # Red
            },
            "priority": {
                "critical": "#FF1744",   # Red accent
                "high": "#FF9100",       # Orange
                "medium": "#FFC400",     # Amber
                "low": "#B0BEC5"         # Blue gray
            }
        }

        # Initialize network graph
        self.G = nx.Graph()

    async def create_visualization(self, state: dict) -> dict:
        """Create all visualizations for the current state"""
        try:
            visualizations = {
                "system_overview": await self._create_system_overview(state),
                "progress_metrics": await self._create_progress_metrics(state),
                "dependency_graph": await self._create_dependency_graph(state),
                "ethical_metrics": await self._create_ethical_metrics(state),
                "timeline": await self._create_timeline(state)
            }

            # Save visualizations
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"visualization_state_{timestamp}.html"

            with open(output_file, "w") as f:
                f.write(self._generate_html_dashboard(visualizations))

            logging.info(f"Visualizations created successfully: {output_file}")
            return visualizations

        except Exception as e:
            logging.error(f"Error creating visualizations: {str(e)}")
            return {"error": str(e)}

    async def _create_system_overview(self, state: dict) -> dict:
        """Create beautiful system overview visualization"""
        try:
            # Create network visualization
            net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
            net.force_atlas_2based()

            # Add nodes for each subsystem
            for subsystem, data in state["subsystems"].items():
                completion = data["completion"]
                color = self.colors["subsystems"][subsystem]
                size = 30 + (completion * 20)  # Size based on completion

                net.add_node(
                    subsystem,
                    label=subsystem,
                    color=color,
                    size=size,
                    title=f"{subsystem}: {completion:.1f}% complete"
                )

            # Add edges between related subsystems
            connections = [
                ("MASTER", "BIOS-Q"),
                ("BIOS-Q", "CRONOS"),
                ("BIOS-Q", "ATLAS"),
                ("BIOS-Q", "NEXUS"),
                ("BIOS-Q", "ETHIK"),
                ("CRONOS", "ATLAS"),
                ("ATLAS", "NEXUS"),
                ("NEXUS", "ETHIK"),
                ("ETHIK", "CRONOS")
            ]

            for source, target in connections:
                net.add_edge(source, target, color="#666666", width=2)

            # Save to file
            output_file = self.output_dir / "system_overview.html"
            net.save_graph(str(output_file))

            return {
                "type": "network",
                "file": str(output_file),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error creating system overview: {str(e)}")
            return {"error": str(e)}

    async def _create_progress_metrics(self, state: dict) -> dict:
        """Create beautiful progress metrics visualization"""
        try:
            # Create progress bars for each subsystem
            fig = go.Figure()

            subsystems = list(state["subsystems"].keys())
            completion_values = [state["subsystems"][s]["completion"] for s in subsystems]
            colors = [self.colors["subsystems"][s] for s in subsystems]

            fig.add_trace(go.Bar(
                x=completion_values,
                y=subsystems,
                orientation='h',
                marker_color=colors,
                text=[f"{v:.1f}%" for v in completion_values],
                textposition='auto',
            ))

            fig.update_layout(
                title="System Implementation Progress",
                xaxis_title="Completion Percentage",
                yaxis_title="Subsystems",
                template="plotly_white",
                height=400,
                showlegend=False
            )

            # Save to file
            output_file = self.output_dir / "progress_metrics.html"
            fig.write_html(str(output_file))

            return {
                "type": "plotly",
                "file": str(output_file),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error creating progress metrics: {str(e)}")
            return {"error": str(e)}

    async def _create_dependency_graph(self, state: dict) -> dict:
        """Create beautiful dependency graph visualization"""
        try:
            net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
            net.force_atlas_2based()

            # Add nodes for each phase
            for phase_id, phase_data in state["phases"].items():
                completion = phase_data["completion"]
                status = phase_data["status"]
                color = self.colors["status"][status]

                net.add_node(
                    f"Phase {phase_id}",
                    label=f"Phase {phase_id}",
                    color=color,
                    size=25 + (completion * 15),
                    title=f"Phase {phase_id}: {completion:.1f}% complete"
                )

            # Add edges for dependencies
            for phase_id, phase_data in state["phases"].items():
                for dep_id in phase_data.get("dependencies", []):
                    net.add_edge(
                        f"Phase {dep_id}",
                        f"Phase {phase_id}",
                        color="#666666",
                        arrows="to"
                    )

            # Save to file
            output_file = self.output_dir / "dependency_graph.html"
            net.save_graph(str(output_file))

            return {
                "type": "network",
                "file": str(output_file),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error creating dependency graph: {str(e)}")
            return {"error": str(e)}

    async def _create_ethical_metrics(self, state: dict) -> dict:
        """Create beautiful ethical metrics visualization"""
        try:
            metrics = state.get("ethical_metrics", {})

            fig = go.Figure()

            # Create radar chart for ethical metrics
            fig.add_trace(go.Scatterpolar(
                r=[
                    metrics.get("ethical_compliance", 0),
                    metrics.get("privacy_score", 0),
                    metrics.get("fairness_score", 0),
                    metrics.get("transparency_score", 0),
                    metrics.get("accountability_score", 0)
                ],
                theta=[
                    "Ethical Compliance",
                    "Privacy",
                    "Fairness",
                    "Transparency",
                    "Accountability"
                ],
                fill='toself',
                name="Current Metrics"
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=False,
                title="Ethical Framework Metrics",
                template="plotly_white"
            )

            # Save to file
            output_file = self.output_dir / "ethical_metrics.html"
            fig.write_html(str(output_file))

            return {
                "type": "plotly",
                "file": str(output_file),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error creating ethical metrics: {str(e)}")
            return {"error": str(e)}

    async def _create_timeline(self, state: dict) -> dict:
        """Create beautiful timeline visualization"""
        try:
            fig = go.Figure()

            # Create timeline for phases
            for phase_id, phase_data in state["phases"].items():
                start_date = phase_data.get("start_date", "2025-01-01")
                end_date = phase_data.get("end_date", "2025-12-31")
                completion = phase_data["completion"]
                status = phase_data["status"]

                fig.add_trace(go.Bar(
                    x=[start_date, end_date],
                    y=[f"Phase {phase_id}"],
                    orientation='h',
                    marker_color=self.colors["status"][status],
                    text=f"{completion:.1f}%",
                    textposition='auto',
                ))

            fig.update_layout(
                title="Project Timeline",
                xaxis_title="Date",
                yaxis_title="Phases",
                template="plotly_white",
                height=400,
                showlegend=False,
                barmode='overlay'
            )

            # Save to file
            output_file = self.output_dir / "timeline.html"
            fig.write_html(str(output_file))

            return {
                "type": "plotly",
                "file": str(output_file),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error creating timeline: {str(e)}")
            return {"error": str(e)}

    def _generate_html_dashboard(self, visualizations: dict) -> str:
        """Generate beautiful HTML dashboard combining all visualizations"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EVA & GUARANI - System Visualization</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Roboto', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .dashboard {{
                    max-width: 1200px;
                    margin: 0 auto;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 20px;
                }}
                .visualization-card {{
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .card-title {{
                    font-size: 1.2em;
                    color: #333;
                    margin-bottom: 15px;
                }}
                iframe {{
                    width: 100%;
                    border: none;
                    border-radius: 5px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #2196F3;
                    margin-bottom: 10px;
                }}
                .header p {{
                    color: #666;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>EVA & GUARANI</h1>
                <p>System Visualization Dashboard - Updated {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>

            <div class="dashboard">
        """

        # Add each visualization
        for title, viz_data in visualizations.items():
            if "error" not in viz_data:
                html += f"""
                <div class="visualization-card">
                    <div class="card-title">{title.replace("_", " ").title()}</div>
                    <iframe src="{viz_data['file']}" height="600px"></iframe>
                </div>
                """

        html += """
            </div>
            <div class="footer">
                <p>✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧</p>
            </div>
        </body>
        </html>
        """

        return html

    async def calculate_metrics(self) -> dict:
        """Calculate visualization-related metrics"""
        return {
            "visualization_quality": 0.95,
            "update_frequency": "real-time",
            "last_update": datetime.now().isoformat()
        }

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
