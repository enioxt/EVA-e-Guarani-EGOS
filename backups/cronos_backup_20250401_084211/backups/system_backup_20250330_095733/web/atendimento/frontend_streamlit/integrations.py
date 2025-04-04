#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Integration Module
Responsible for connecting the Streamlit frontend with the system core.

Date: 2025-03-20
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ATLASInterface:
    """Interface for the ATLAS module."""

    def __init__(self, atlas_core):
        """Initializes the ATLAS interface."""
        self.atlas_core = atlas_core
        self.logger = logging.getLogger(__name__)

    def create_node(
        self,
        name: str,
        node_type: str,
        metadata: Dict[str, Any],
        love_quotient: float = 0.95,
        consciousness_level: float = 0.90,
    ) -> Optional[str]:
        """Creates a new node in the system."""
        try:
            node = self.atlas_core.SystemNode(
                id=f"node_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=name,
                type=node_type,
                metadata=metadata,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                love_quotient=love_quotient,
                consciousness_level=consciousness_level,
            )

            if self.atlas_core.add_node(node):
                self.logger.info(f"Node '{name}' created successfully")
                return node.id
            return None
        except Exception as e:
            self.logger.error(f"Error creating node: {str(e)}")
            return None

    def create_connection(
        self,
        source_id: str,
        target_id: str,
        conn_type: str,
        strength: float,
        metadata: Dict[str, Any],
    ) -> Optional[str]:
        """Creates a new connection between nodes."""
        try:
            connection = self.atlas_core.SystemConnection(
                id=f"conn_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id=source_id,
                target_id=target_id,
                type=conn_type,
                strength=strength,
                metadata=metadata,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            if self.atlas_core.add_connection(connection):
                self.logger.info(f"Connection created successfully")
                return connection.id
            return None
        except Exception as e:
            self.logger.error(f"Error creating connection: {str(e)}")
            return None

    def analyze_system(self) -> Dict[str, Any]:
        """Analyzes the current system."""
        try:
            return self.atlas_core.analyze_topology()
        except Exception as e:
            self.logger.error(f"Error analyzing system: {str(e)}")
            return {}


class NEXUSInterface:
    """Interface for the NEXUS module."""

    def __init__(self, nexus_core):
        """Initializes the NEXUS interface."""
        self.nexus_core = nexus_core
        self.logger = logging.getLogger(__name__)

    def analyze_component(
        self,
        component_id: str,
        analysis_level: str,
        include_metrics: bool = True,
        include_dependencies: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Analyzes a system component."""
        try:
            return self.nexus_core.analyze_component(
                component_id=component_id,
                level=analysis_level,
                include_metrics=include_metrics,
                include_dependencies=include_dependencies,
            )
        except Exception as e:
            self.logger.error(f"Error analyzing component: {str(e)}")
            return None

    def optimize_component(
        self,
        component_id: str,
        target: str,
        love_threshold: float = 0.95,
        consciousness_threshold: float = 0.90,
        create_backup: bool = True,
    ) -> bool:
        """Optimizes a system component."""
        try:
            return self.nexus_core.optimize_component(
                component_id=component_id,
                target=target,
                love_threshold=love_threshold,
                consciousness_threshold=consciousness_threshold,
                create_backup=create_backup,
            )
        except Exception as e:
            self.logger.error(f"Error optimizing component: {str(e)}")
            return False


class CRONOSInterface:
    """Interface for the CRONOS module."""

    def __init__(self, cronos_core):
        """Initializes the CRONOS interface."""
        self.cronos_core = cronos_core
        self.logger = logging.getLogger(__name__)

    def create_backup(self, name: str, backup_type: str, metadata: Dict[str, Any]) -> Optional[str]:
        """Creates a new system backup."""
        try:
            return self.cronos_core.create_backup(
                name=name, backup_type=backup_type, metadata=metadata
            )
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            return None

    def restore_backup(
        self, backup_id: str, verify_integrity: bool = True, create_restore_point: bool = True
    ) -> bool:
        """Restores a system backup."""
        try:
            return self.cronos_core.restore_backup(
                backup_id=backup_id,
                verify_integrity=verify_integrity,
                create_restore_point=create_restore_point,
            )
        except Exception as e:
            self.logger.error(f"Error restoring backup: {str(e)}")
            return False


class ETHIKInterface:
    """Interface for the ETHIK module."""

    def __init__(self, ethik_core):
        """Initializes the ETHIK interface."""
        self.ethik_core = ethik_core
        self.logger = logging.getLogger(__name__)

    def validate_action(
        self, action: str, context: Dict[str, Any], love_quotient: float = 0.95
    ) -> bool:
        """Validates a system action."""
        try:
            return self.ethik_core.validate_action(
                action=action, context=context, love_quotient=love_quotient
            )
        except Exception as e:
            self.logger.error(f"Error validating action: {str(e)}")
            return False

    def get_ethical_metrics(self) -> Dict[str, Any]:
        """Obtains ethical metrics from the system."""
        try:
            return self.ethik_core.get_metrics()
        except Exception as e:
            self.logger.error(f"Error obtaining ethical metrics: {str(e)}")
            return {}


class EVASystem:
    """Main interface for the EVA & GUARANI system."""

    def __init__(self, core_path: str):
        """Initializes the EVA & GUARANI system."""
        self.core_path = Path(core_path)
        self.logger = logging.getLogger(__name__)

        # Add core to the system path
        sys.path.append(str(self.core_path))

        # Module interfaces
        self.atlas = None
        self.nexus = None
        self.cronos = None
        self.ethik = None

    def initialize(self) -> bool:
        """Initializes all system modules."""
        try:
            # Import core modules
            from atlas.src.atlas_core import ATLASCore
            from nexus.src.nexus_core import NEXUSCore
            from cronos.src.cronos_core import CRONOSCore
            from ethik.src.ethik_core import ETHIKCore

            # Initialize cores
            atlas_core = ATLASCore()
            nexus_core = NEXUSCore()
            cronos_core = CRONOSCore()
            ethik_core = ETHIKCore()

            # Create interfaces
            self.atlas = ATLASInterface(atlas_core)
            self.nexus = NEXUSInterface(nexus_core)
            self.cronos = CRONOSInterface(cronos_core)
            self.ethik = ETHIKInterface(ethik_core)

            self.logger.info("EVA & GUARANI system initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error initializing system: {str(e)}")
            return False

    def get_system_status(self) -> Dict[str, Any]:
        """Obtains the current system status."""
        try:
            status = {
                "initialized": all(
                    [
                        self.atlas is not None,
                        self.nexus is not None,
                        self.cronos is not None,
                        self.ethik is not None,
                    ]
                ),
                "timestamp": datetime.now().isoformat(),
                "modules": {
                    "atlas": self.atlas is not None,
                    "nexus": self.nexus is not None,
                    "cronos": self.cronos is not None,
                    "ethik": self.ethik is not None,
                },
            }

            # Add metrics if available
            if self.ethik:
                status["ethics"] = self.ethik.get_ethical_metrics()

            if self.atlas:
                status["topology"] = self.atlas.analyze_system()

            return status

        except Exception as e:
            self.logger.error(f"Error obtaining system status: {str(e)}")
            return {"initialized": False, "error": str(e)}
