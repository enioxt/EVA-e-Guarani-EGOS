#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Quantum Knowledge Integration Script
====================================================

This script integrates the Quantum Knowledge system with the unified bot EVA & GUARANI.
It sets up and connects the QuantumKnowledgeHub and QuantumKnowledgeIntegrator,
allowing the bot to access the system's internal knowledge before using
external AI models, optimizing cost and maintaining the system's identity.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0
"""

import os
import sys
import json
import logging
import asyncio
import importlib
from pathlib import Path
from typing import Dict, Any, Optional

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/quantum_integration.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("integrate_quantum_knowledge")

class QuantumKnowledgeIntegrationManager:
    """
    Manager for integrating the quantum knowledge system into the unified bot.
    """
    
    def __init__(self, bot_path: str = "unified_eva_guarani_bot.py", config_path: str = "config/integration_manager.json"):
        """
        Initializes the integration manager.
        
        Args:
            bot_path: Path to the unified bot file
            config_path: Path to the configuration file
        """
        self.logger = logger
        self.logger.info("Initializing Quantum Knowledge Integration Manager")
        
        # Paths
        self.bot_path = Path(bot_path)
        self.config_path = Path(config_path)
        
        # Internal state
        self.config = self._load_config()
        self.bot_module = None
        self.bot_instance = None
        self.knowledge_hub = None
        self.knowledge_integrator = None
        
        # Check environments
        self._ensure_directories()
        
        self.logger.info("Quantum Knowledge Integration Manager initialized")
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the integration manager configuration.
        
        Returns:
            Dictionary with the configurations
        """
        # Default configuration
        default_config = {
            "version": "1.0",
            "auto_start_bot": False,
            "auto_index_on_start": True,
            "create_template_directories": True,
            "backup_bot_before_integration": True,
            "use_quantum_knowledge": True,
            "directories_to_create": [
                "EGOS/quantum_prompts",
                "EGOS/ethical_system",
                "EGOS/personas",
                "EGOS/stories",
                "EGOS/blockchain",
                "EGOS/game_elements",
                "templates",
                "data/quantum_knowledge",
                "data/quantum_knowledge/cache",
                "logs/quantum_integrator"
            ]
        }
        
        # Try to load custom configuration
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default configuration
                    merged_config = {**default_config, **config}
                    self.logger.info(f"Configuration loaded from {self.config_path}")
                    return merged_config
            else:
                # Create default configuration file
                os.makedirs(self.config_path.parent, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Default configuration created at {self.config_path}")
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return default_config
            
    def _ensure_directories(self) -> None:
        """
        Creates the necessary directories for the quantum knowledge system.
        """
        if not self.config.get("create_template_directories", True):
            self.logger.info("Directory creation disabled")
            return
            
        try:
            for directory in self.config.get("directories_to_create", []):
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"Directory created/verified: {directory}")
                
        except Exception as e:
            self.logger.error(f"Error creating directories: {e}")
            
    def _backup_bot(self) -> bool:
        """
        Creates a backup copy of the unified bot before integration.
        
        Returns:
            True if the backup was successful, False otherwise
        """
        if not self.config.get("backup_bot_before_integration", True):
            self.logger.info("Bot backup disabled")
            return True
            
        try:
            # Check if the bot file exists
            if not self.bot_path.exists():
                self.logger.error(f"Bot file not found: {self.bot_path}")
                return False
                
            # Create backup file
            backup_path = self.bot_path.with_suffix(".py.bak")
            with open(self.bot_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                    
            self.logger.info(f"Bot backup created at {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error backing up bot: {e}")
            return False
            
    async def initialize_components(self) -> bool:
        """
        Initializes the components of the quantum knowledge system.
        
        Returns:
            True if all components were successfully initialized, False otherwise
        """
        try:
            # 1. Initialize QuantumKnowledgeHub
            from quantum_knowledge_hub import QuantumKnowledgeHub, create_default_config as create_hub_config
            
            # Create default hub configuration
            create_hub_config()
            
            # Initialize hub
            self.knowledge_hub = QuantumKnowledgeHub()
            if not self.knowledge_hub.initialized:
                self.logger.error("Failed to initialize QuantumKnowledgeHub")
                return False
                
            self.logger.info("QuantumKnowledgeHub initialized successfully")
            
            # 2. Initialize QuantumKnowledgeIntegrator
            from quantum_knowledge_integrator import QuantumKnowledgeIntegrator, create_default_config as create_integrator_config
            
            # Create default integrator configuration
            create_integrator_config()
            
            # Initialize integrator
            self.knowledge_integrator = QuantumKnowledgeIntegrator()
            if not self.knowledge_integrator.initialized:
                self.logger.error("Failed to initialize QuantumKnowledgeIntegrator")
                return False
                
            self.logger.info("QuantumKnowledgeIntegrator initialized successfully")
            
            # 3. Connect hub to integrator
            await self.knowledge_integrator.initialize_hub()
            
            # 4. Index knowledge if configured
            if self.config.get("auto_index_on_start", True):
                await self.knowledge_integrator.index_quantum_knowledge()
                
            self.logger.info("Quantum knowledge system components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            return False
            
    async def load_bot(self) -> bool:
        """
        Loads the unified bot module.
        
        Returns:
            True if the bot was successfully loaded, False otherwise
        """
        try:
            # Check if the bot file exists
            if not self.bot_path.exists():
                self.logger.error(f"Bot file not found: {self.bot_path}")
                return False
                
            # Get module name without extension
            module_name = self.bot_path.stem
            
            # If the module has already been imported, reload it
            if module_name in sys.modules:
                self.bot_module = importlib.reload(sys.modules[module_name])
            else:
                # Import module
                spec = importlib.util.spec_from_file_location(module_name, self.bot_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.bot_module = module
                
            # Check if the module contains the bot class
            bot_class_name = "EVAGuaraniBot"
            if not hasattr(self.bot_module, bot_class_name):
                self.logger.error(f"Class '{bot_class_name}' not found in module")
                return False
                
            # Do not create bot instance yet, just ensure the module is loaded
            self.logger.info(f"Bot module '{module_name}' loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading bot module: {e}")
            return False
            
    async def integrate_knowledge_system(self) -> bool:
        """
        Integrates the quantum knowledge system into the unified bot.
        
        Returns:
            True if the integration was successful, False otherwise
        """
        try:
            # 1. Backup the bot if configured
            if not self._backup_bot():
                self.logger.warning("Continuing without backup")
                
            # 2. Load bot
            if not await self.load_bot():
                return False
                
            # 3. Initialize components
            if not await self.initialize_components():
                return False
                
            # 4. Check if there is a bot instance available
            if hasattr(self.bot_module, "bot_instance") and self.bot_module.bot_instance is not None:
                self.bot_instance = self.bot_module.bot_instance
                
                # 5. Integrate knowledge system into the bot
                result = await self.knowledge_integrator.integrate_with_bot(self.bot_instance)
                if result:
                    self.logger.info("Quantum knowledge system successfully integrated into the bot")
                else:
                    self.logger.warning("Integration with existing bot failed")
                    
                return result
            else:
                # Bot not yet initialized, modify file for automatic integration
                self.logger.info("Bot not initialized, preparing for integration at startup")
                return await self._prepare_bot_for_integration()
                
        except Exception as e:
            self.logger.error(f"Error integrating quantum knowledge system: {e}")
            return False
            
    async def _prepare_bot_for_integration(self) -> bool:
        """
        Prepares the bot for automatic integration during startup.
        This involves modifying the bot file to add the integration code.
        
        Returns:
            True if the preparation was successful, False otherwise
        """
        try:
            # Read bot file
            with open(self.bot_path, 'r', encoding='utf-8') as f:
                bot_code = f.read()
                
            # Check if integration has already been added
            if "quantum_knowledge_integrator" in bot_code and "quantum_knowledge_hub" in bot_code:
                self.logger.info("Integration code already exists in the bot file")
                return True
                
            # Code to add imports
            import_code = """
# Imports for quantum knowledge integration
import asyncio
try:
    from quantum_knowledge_integrator import QuantumKnowledgeIntegrator
    from quantum_knowledge_hub import QuantumKnowledgeHub
    QUANTUM_KNOWLEDGE_AVAILABLE = True
except ImportError:
    QUANTUM_KNOWLEDGE_AVAILABLE = False
    print("Quantum knowledge modules not available. Some features will be limited.")
"""
            
            # Code to add in the bot class initialization
            init_code = """
        # Initialize quantum knowledge system if available
        self.quantum_knowledge_integrator = None
        if QUANTUM_KNOWLEDGE_AVAILABLE:
            self.logger.info("Initializing quantum knowledge system...")
            try:
                asyncio.run(self._setup_quantum_knowledge())
                self.logger.info("Quantum knowledge system initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing quantum knowledge system: {e}")
"""
            
            # Code to add setup method
            method_code = """
    async def _setup_quantum_knowledge(self):
        """
        Sets up and initializes the quantum knowledge system.
        """
        try:
            # Initialize knowledge integrator
            integrator = QuantumKnowledgeIntegrator()
            
            # Initialize knowledge hub
            await integrator.initialize_hub()
            
            # Connect to existing quantum integration
            if hasattr(self, 'quantum_integration') and self.quantum_integration is not None:
                await integrator.connect_quantum_integration(self.quantum_integration)
                
            # Index existing knowledge
            await integrator.index_quantum_knowledge()
            
            # Store reference
            self.quantum_knowledge_integrator = integrator
            
            self.logger.info("Quantum knowledge system configured successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up quantum knowledge system: {e}")
            return False
            
    async def process_message_with_knowledge(self, message, user_id=None, conversation_id=None):
        """
        Processes a message using the quantum knowledge system.
        
        Args:
            message: Message to be processed
            user_id: ID of the user who sent the message
            conversation_id: ID of the conversation
            
        Returns:
            Response processed using quantum knowledge or None if not available
        """
        try:
            if not hasattr(self, 'quantum_knowledge_integrator') or self.quantum_knowledge_integrator is None:
                self.logger.warning("Quantum knowledge system not available")
                return None
                
            # Conversation context
            conversation_history = self.get_conversation_history(conversation_id) if hasattr(self, 'get_conversation_history') else []
            
            # Contextual data
            context_data = {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "platform": "telegram",
                "bot_name": "EVA & GUARANI"
            }
            
            # Process message using quantum knowledge
            result = await self.quantum_knowledge_integrator.process_message(
                message=message,
                conversation_history=conversation_history,
                context_data=context_data
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing message with quantum knowledge: {e}")
            return None
"""
            
            # Modify code to add imports
            if "# Imports for quantum knowledge integration" not in bot_code:
                # Find last import
                import_index = 0
                lines = bot_code.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        import_index = i
                        
                # Add after the last import
                modified_lines = lines[:import_index+1] + import_code.split("\n") + lines[import_index+1:]
                bot_code = "\n".join(modified_lines)
                
            # Add initialization code in the bot class
            if "# Initialize quantum knowledge system if available" not in bot_code:
                # Find __init__ method of EVAGuaraniBot class
                init_index = bot_code.find("def __init__(self")
                if init_index == -1:
                    self.logger.error("Method __init__ not found in EVAGuaraniBot class")
                    return False
                    
                # Find end of initialization (probably after self.logger = ...)
                init_end_index = bot_code.find("self.logger =", init_index)
                if init_end_index == -1:
                    # Try to find the end of __init__ another way
                    lines = bot_code.split("\n")
                    for i, line in enumerate(lines):
                        if "def __init__" in line:
                            # Look for the next method
                            for j in range(i + 1, len(lines)):
                                if "    def " in lines[j]:
                                    init_end_index = bot_code.find(lines[j])
                                    break
                            break
                            
                if init_end_index == -1:
                    self.logger.error("Could not find location to insert initialization code")
                    return False
                    
                # Find where the initialization block ends (next line with same indentation)
                init_end_line = bot_code[init_end_index:].split("\n")[0]
                indent = len(init_end_line) - len(init_end_line.lstrip())
                
                # Look for the next line with the same indentation or before a new method
                lines = bot_code[init_end_index:].split("\n")
                insertion_index = 0
                for i, line in enumerate(lines):
                    if (line.strip() and len(line) - len(line.lstrip()) == indent) or "    def " in line:
                        insertion_index = init_end_index + sum(len(line) + 1 for line in lines[:i])
                        break
                        
                if insertion_index == 0:
                    insertion_index = init_end_index + bot_code[init_end_index:].find("\n\n")
                    
                # Add initialization code
                bot_code = bot_code[:insertion_index] + init_code + bot_code[insertion_index:]
                
            # Add methods if they do not exist
            if "async def _setup_quantum_knowledge" not in bot_code:
                # Find last method of the class
                last_method_index = 0
                class_end_index = 0
                lines = bot_code.split("\n")
                class_found = False
                for i, line in enumerate(lines):
                    if "class EVAGuaraniBot" in line:
                        class_found = True
                    elif class_found and line.strip() and not line.startswith((" ", "\t")):
                        # Found line outside the class
                        class_end_index = sum(len(line) + 1 for line in lines[:i])
                        break
                    elif class_found and line.startswith("    def "):
                        last_method_index = sum(len(line) + 1 for line in lines[:i])
                        
                if last_method_index == 0 or class_end_index == 0:
                    self.logger.error("Could not find location to insert new methods")
                    return False
                    
                # Find the end of the last method
                method_end_index = 0
                current_indent = 4
                lines = bot_code[last_method_index:class_end_index].split("\n")
                for i, line in enumerate(lines):
                    if line.strip() and len(line) - len(line.lstrip()) <= current_indent and (line.startswith("    def ") or i > 10):
                        method_end_index = last_method_index + sum(len(line) + 1 for line in lines[:i])
                        break
                        
                if method_end_index == 0:
                    method_end_index = class_end_index
                    
                # Add new methods
                bot_code = bot_code[:method_end_index] + "\n" + method_code + bot_code[method_end_index:]
                
            # Save modified code
            with open(self.bot_path, 'w', encoding='utf-8') as f:
                f.write(bot_code)
                
            self.logger.info("Bot prepared for automatic integration of the quantum knowledge system")
            return True
            
        except Exception as e:
            self.logger.error(f"Error preparing bot for integration: {e}")
            return False
            
    async def run(self) -> bool:
        """
        Executes the integration of the quantum knowledge system.
        
        Returns:
            True if the integration was successful, False otherwise
        """
        try:
            # 1. Integrate knowledge system
            if not await self.integrate_knowledge_system():
                return False
                
            # 2. Start bot automatically if configured
            if self.config.get("auto_start_bot", False) and self.bot_module is not None: