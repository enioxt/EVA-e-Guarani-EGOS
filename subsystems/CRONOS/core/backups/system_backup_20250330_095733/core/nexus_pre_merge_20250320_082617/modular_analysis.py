#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NEXUS - Modular Analysis Subsystem
Responsible for the detailed analysis of the EVA & GUARANI system components
Version: 8.0.0
Date: 19/03/2025
"""

import os
import sys
import json
import logging
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple, Set

# Logging configuration
logger = logging.getLogger("EVA_GUARANI.NEXUS")

class Nexus:
    """
    Main class of the NEXUS subsystem, responsible for modular analysis.
    
    NEXUS performs in-depth analysis of the system components, evaluating
    their structure, quality, cohesion, and coupling. It provides insights into
    the architecture and suggests optimizations to improve modularity.
    """
    
    def __init__(self, config: Dict[str, Any], system_root: Path):
        """
        Initializes the NEXUS subsystem
        
        Args:
            config: NEXUS subsystem configuration
            system_root: System root path
        """
        self.logger = logger
        self.logger.info("🧠 Initializing NEXUS subsystem v8.0.0 🧠")
        
        self.config = config
        self.system_root = system_root
        self.enabled = config.get("enabled", True)
        self.analysis_depth = config.get("analysis_depth", "comprehensive")
        self.modular_threshold = config.get("modular_threshold", 0.8)
        self.report_format = config.get("report_format", "markdown")
        self.dependency_tracking = config.get("dependency_tracking", True)
        
        # System state
        self.is_running = False
        self.module_cache: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.analysis_results: Dict[str, Dict[str, Any]] = {}
        self.dependencies: Dict[str, Dict[str, Any]] = {}
        
        # Metrics
        self.metrics: Dict[str, Any] = {
            "modules_analyzed": 0,
            "issues_found": 0,
            "optimizations_suggested": 0,
            "architectural_patterns": set(),
            "last_analysis_time": None
        }
        
        self.logger.info(f"NEXUS initialized with depth {self.analysis_depth} and threshold {self.modular_threshold}")
        
    def start(self) -> bool:
        """
        Starts the NEXUS subsystem.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.enabled:
            self.logger.warning("NEXUS is disabled in the settings")
            return False
            
        if self.is_running:
            self.logger.warning("NEXUS is already running")
            return False
            
        self.logger.info("Starting NEXUS subsystem")
        
        # Initialize structures
        self._initialize_module_cache()
        
        self.is_running = True
        self.logger.info("NEXUS started successfully")
        return True
        
    def stop(self) -> bool:
        """
        Stops the NEXUS subsystem.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        if not self.is_running:
            self.logger.warning("NEXUS is not running")
            return False
            
        self.logger.info("Stopping NEXUS subsystem")
        
        # Save analysis results if necessary
        self._persist_analysis_results()
        
        self.is_running = False
        self.logger.info("NEXUS stopped successfully")
        return True
        
    def _initialize_module_cache(self) -> None:
        """Initializes the system module cache"""
        self.logger.info("Initializing system module cache")
        
        # Here the initial indexing of modules would be done
        # For now, we just simulate with a basic structure
        
        self.module_cache = {
            "core": {
                "egos": {
                    "path": "core/egos",
                    "files": ["main.py", "core.py", "loader.py"],
                    "complexity": 0.75,
                    "dependencies": ["atlas", "nexus", "cronos", "ethik"]
                },
                "atlas": {
                    "path": "core/atlas",
                    "files": ["cartography.py", "visualization.py", "mapper.py"],
                    "complexity": 0.65,
                    "dependencies": ["modules/quantum"]
                },
                "nexus": {
                    "path": "core/nexus",
                    "files": ["modular_analysis.py", "quality.py", "metrics.py"],
                    "complexity": 0.70,
                    "dependencies": ["modules/analysis"]
                },
                "cronos": {
                    "path": "core/cronos",
                    "files": ["preservation.py", "backup.py", "versioning.py"],
                    "complexity": 0.60,
                    "dependencies": ["data/logs"]
                },
                "ethik": {
                    "path": "core/ethik",
                    "files": ["principles.py", "evaluation.py", "guidelines.py"],
                    "complexity": 0.80,
                    "dependencies": ["modules/integration"]
                }
            },
            "modules": {
                "quantum": {
                    "path": "modules/quantum",
                    "files": ["entanglement.py", "superposition.py", "wave_function.py"],
                    "complexity": 0.85,
                    "dependencies": []
                },
                "analysis": {
                    "path": "modules/analysis",
                    "files": ["patterns.py", "anomalies.py", "insights.py"],
                    "complexity": 0.70,
                    "dependencies": []
                },
                "integration": {
                    "path": "modules/integration",
                    "files": ["connector.py", "adapters.py", "protocols.py"],
                    "complexity": 0.65,
                    "dependencies": ["integrations/api", "integrations/bots"]
                }
            }
        }
        
        # Build dependency graph
        self._build_dependency_graph()
        
        self.logger.info(f"Module cache initialized with {sum(len(category) for category in self.module_cache.values())} modules")
        
    def _build_dependency_graph(self) -> None:
        """Builds the dependency graph between modules"""
        self.logger.info("Building dependency graph")
        
        self.dependencies = {}
        
        # Traverse all modules and their dependencies
        for category, modules in self.module_cache.items():
            for module_name, module_info in modules.items():
                module_path = f"{category}/{module_name}"
                self.dependencies[module_path] = {
                    "direct": module_info.get("dependencies", []),
                    "indirect": [],
                    "dependents": []
                }
        
        # Add dependents and indirect dependencies
        for module_path, deps in self.dependencies.items():
            for direct_dep in deps["direct"]:
                if direct_dep in self.dependencies:
                    self.dependencies[direct_dep]["dependents"].append(module_path)
                    
                    # Add indirect dependencies (level 1 only)
                    for indirect_dep in self.dependencies[direct_dep].get("direct", []):
                        if indirect_dep not in deps["direct"] and indirect_dep != module_path:
                            deps["indirect"].append(indirect_dep)
        
        self.logger.info(f"Dependency graph built with {len(self.dependencies)} modules")
        
    def analyze_module(self, module_path: str) -> Dict[str, Any]:
        """
        Performs a detailed analysis of a module
        
        Args:
            module_path: Path of the module to be analyzed
            
        Returns:
            Dict: Analysis results
        """
        self.logger.info(f"Analyzing module: {module_path}")
        
        # Check if the module exists in the cache
        parts = module_path.split("/")
        if len(parts) < 2:
            self.logger.error(f"Invalid module path: {module_path}")
            return {"error": "Invalid module path"}
            
        category, name = parts[0], parts[1]
        
        if category not in self.module_cache or name not in self.module_cache[category]:
            self.logger.error(f"Module not found: {module_path}")
            return {"error": "Module not found"}
            
        # Retrieve module information
        module_info = self.module_cache[category][name]
        
        # Here the detailed analysis would be implemented
        # For now, we return simulated data
        
        # Calculate quality metrics
        quality_metrics = self._calculate_quality_metrics(module_info)
        
        # Check architectural patterns
        patterns = self._identify_patterns(module_info)
        
        # Generate optimization suggestions
        optimizations = self._suggest_optimizations(module_info, quality_metrics)
        
        # Analyze dependencies
        dependency_analysis = self._analyze_dependencies(module_path)
        
        # Assemble analysis result
        analysis = {
            "module": module_path,
            "files": module_info["files"],
            "quality": quality_metrics,
            "patterns": patterns,
            "optimizations": optimizations,
            "dependencies": dependency_analysis,
            "overall_score": self._calculate_overall_score(quality_metrics),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Update metrics
        self.metrics["modules_analyzed"] += 1
        self.metrics["issues_found"] += len(optimizations)
        self.metrics["optimizations_suggested"] += len(optimizations)
        self.metrics["architectural_patterns"].update(patterns)
        self.metrics["last_analysis_time"] = datetime.datetime.now()
        
        # Store result in cache
        self.analysis_results[module_path] = analysis
        
        self.logger.info(f"Module {module_path} analysis completed with score {analysis['overall_score']:.2f}")
        return analysis
        
    def _calculate_quality_metrics(self, module_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates quality metrics for a module
        
        Args:
            module_info: Module information
            
        Returns:
            Dict: Quality metrics
        """
        # Simulated quality metrics
        file_count = len(module_info.get("files", []))
        complexity = module_info.get("complexity", 0.5)
        dependency_count = len(module_info.get("dependencies", []))
        
        # Calculate simulated metrics
        cohesion = max(0.0, min(1.0, 0.9 - (0.05 * dependency_count)))
        coupling = max(0.0, min(1.0, 0.1 + (0.1 * dependency_count)))
        maintainability = max(0.0, min(1.0, 0.8 - (0.1 * complexity)))
        testability = max(0.0, min(1.0, 0.75 - (0.05 * complexity)))
        
        return {
            "cohesion": cohesion,
            "coupling": coupling,
            "complexity": complexity,
            "maintainability": maintainability,
            "testability": testability,
            "file_count": file_count,
            "dependency_count": dependency_count
        }
        
    def _identify_patterns(self, module_info: Dict[str, Any]) -> List[str]:
        """
        Identifies architectural patterns in a module
        
        Args:
            module_info: Module information
            
        Returns:
            List: Identified patterns
        """
        # Simulated pattern identification
        patterns = []
        
        files = [f.lower() for f in module_info.get("files", [])]
        
        if any("factory" in f for f in files):
            patterns.append("factory")
            
        if any("adapter" in f for f in files):
            patterns.append("adapter")
            
        if any("singleton" in f for f in files):
            patterns.append("singleton")
            
        if "core.py" in files:
            patterns.append("core")
            
        if any("service" in f for f in files):
            patterns.append("service")
            
        # Add random pattern for example
        import random
        other_patterns = ["mvc", "observer", "strategy", "command", "repository"]
        patterns.append(random.choice(other_patterns))
        
        return patterns
        
    def _suggest_optimizations(self, module_info: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggests optimizations for a module
        
        Args:
            module_info: Module information
            metrics: Quality metrics
            
        Returns:
            List: Optimization suggestions
        """
        optimizations = []
        
        # Suggestions based on metrics
        if metrics["cohesion"] < 0.7:
            optimizations.append({
                "type": "cohesion",
                "severity": "medium",
                "description": "Low cohesion detected. Consider refactoring to improve module cohesion.",
                "suggested_action": "Separate responsibilities into more specific classes/functions."
            })
            
        if metrics["coupling"] > 0.5:
            optimizations.append({
                "type": "coupling",
                "severity": "high",
                "description": "High coupling detected. Reduce dependencies between modules.",
                "suggested_action": "Implement more abstract interfaces or patterns like Dependency Injection."
            })
            
        if metrics["complexity"] > 0.7:
            optimizations.append({
                "type": "complexity",
                "severity": "high",
                "description": "High complexity. Simplify the code.",
                "suggested_action": "Refactor complex methods, extract helper functions."
            })
            
        if metrics["maintainability"] < 0.6:
            optimizations.append({
                "type": "maintainability",
                "severity": "medium",
                "description": "Low maintainability. Improve clarity and documentation.",
                "suggested_action": "Add documentation, improve variable names, simplify logic."
            })
            
        # Limit to 3 optimizations to avoid overload
        return optimizations[:3]
        
    def _analyze_dependencies(self, module_path: str) -> Dict[str, Any]:
        """
        Analyzes the dependencies of a module
        
        Args:
            module_path: Module path
            
        Returns:
            Dict: Dependency analysis
        """
        if module_path not in self.dependencies:
            return {
                "error": "Module not found in dependency graph"
            }
            
        deps = self.dependencies[module_path]
        
        # Analyze circular dependencies
        circular = []
        for dep in deps["direct"]:
            if module_path in self.dependencies.get(dep, {}).get("direct", []):
                circular.append(dep)
                
        # Calculate dependency metrics
        analysis = {
            "direct_count": len(deps["direct"]),
            "indirect_count": len(deps["indirect"]),
            "dependents_count": len(deps["dependents"]),
            "circular": circular,
            "direct": deps["direct"],
            "indirect": deps["indirect"],
            "dependents": deps["dependents"],
            "has_circular": len(circular) > 0,
            "dependency_depth": self._calculate_dependency_depth(module_path)
        }
        
        return analysis
        
    def _calculate_dependency_depth(self, module_path: str, visited: Optional[Set[str]] = None) -> int:
        """
        Calculates the maximum depth of the dependency tree
        
        Args:
            module_path: Module path
            visited: Set of already visited modules (to avoid cycles)
            
        Returns:
            int: Maximum depth
        """
        if visited is None:
            visited = set()
            
        if module_path in visited:
            return 0
            
        visited.add(module_path)
        
        if module_path not in self.dependencies:
            return 0
            
        direct_deps = self.dependencies[module_path]["direct"]
        
        if not direct_deps:
            return 0
            
        return 1 + max([self._calculate_dependency_depth(dep, visited.copy()) for dep in direct_deps], default=0)
        
    def _calculate_overall_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculates the overall score of the module
        
        Args:
            metrics: Quality metrics
            
        Returns:
            float: Overall score (0 to 1)
        """
        # Define weights for each metric
        weights = {
            "cohesion": 0.25,
            "coupling": 0.25,  # Note: coupling should be inverted as lower values are better
            "complexity": 0.15,  # Should also be inverted
            "maintainability": 0.20,
            "testability": 0.15
        }
        
        # Calculate score
        score = 0.0
        score += metrics["cohesion"] * weights["cohesion"]
        score += (1 - metrics["coupling"]) * weights["coupling"]
        score += (1 - metrics["complexity"]) * weights["complexity"]
        score += metrics["maintainability"] * weights["maintainability"]
        score += metrics["testability"] * weights["testability"]
        
        return score
        
    def _persist_analysis_results(self) -> None:
        """Persists the analysis results to disk"""
        self.logger.info("Persisting analysis results")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir = self.system_root / "data" / "nexus" / "results"
        result_dir.mkdir(parents=True, exist_ok=True)
        
        result_path = result_dir / f"analysis_results_{timestamp}.json"
        
        try:
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "metadata": {
                        "timestamp": timestamp,
                        "version": "8.0.0",
                        "metrics": {k: list(v) if isinstance(v, set) else v for k, v in self.metrics.items()}
                    },
                    "results": self.analysis_results
                }, f, indent=2, default=str)
                
            self.logger.info(f"Results persisted in {result_path}")
        except Exception as e:
            self.logger.error(f"Error persisting results: {str(e)}")
        
    def generate_system_report(self, format: str = "markdown") -> Union[str, Dict[str, Any]]:
        """
        Generates a system report based on the analyses performed
        
        Args:
            format: Report format (markdown, json)
            
        Returns:
            Union[str, Dict]: Report in the specified format
        """
        self.logger.info(f"Generating system report in {format} format")
        
        # Check if there are enough analyses
        if len(self.analysis_results) == 0:
            self.logger.warning("No analysis available to generate report")
            return "No modules have been analyzed yet" if format == "markdown" else {"error": "No modules analyzed"}
            
        # Calculate global metrics
        overall_scores = [result["overall_score"] for result in self.analysis_results.values()]
        avg_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        # Find problematic modules