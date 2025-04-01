#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Quantum Knowledge System Test
=============================================

This script allows manual testing of the quantum knowledge system,
by sending queries and viewing how the system processes and responds to them.
It is a diagnostic and testing tool for the EVA & GUARANI system.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0
"""

import os
import json
import asyncio
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/quantum_knowledge_test.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_quantum_knowledge")

class QuantumKnowledgeTester:
    """
    Class to test the EVA & GUARANI Quantum Knowledge System.
    Allows sending queries, viewing results, and testing different configurations.
    """
    
    def __init__(self):
        """
        Initializes the quantum knowledge system tester.
        """
        self.logger = logger
        self.logger.info("Initializing Quantum Knowledge System Tester")
        
        # Check if necessary files exist
        self.check_files()
        
        # Internal state
        self.hub = None
        self.integrator = None
        self.conversation_history = []
        self.initialized = False
        
        self.logger.info("Tester initialized")
        
    def check_files(self) -> bool:
        """
        Checks if the necessary files exist.
        
        Returns:
            True if all files exist, False otherwise
        """
        required_files = [
            "quantum_knowledge_hub.py",
            "quantum_knowledge_integrator.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
                
        if missing_files:
            self.logger.error(f"Necessary files not found: {', '.join(missing_files)}")
            return False
            
        return True
        
    async def initialize(self) -> bool:
        """
        Initializes the components of the quantum knowledge system.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            # Create necessary directories
            os.makedirs("logs", exist_ok=True)
            
            # Import QuantumKnowledgeHub
            from quantum_knowledge_hub import QuantumKnowledgeHub
            
            # Initialize hub
            self.hub = QuantumKnowledgeHub()
            
            # Import QuantumKnowledgeIntegrator
            from quantum_knowledge_integrator import QuantumKnowledgeIntegrator
            
            # Initialize integrator
            self.integrator = QuantumKnowledgeIntegrator()
            
            # Initialize hub in the integrator
            await self.integrator.initialize_hub()
            
            self.initialized = True
            self.logger.info("Quantum knowledge system successfully initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing system: {e}")
            return False
            
    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processes a query using the quantum knowledge system.
        
        Args:
            query: Query to be processed
            
        Returns:
            Processing result
        """
        if not self.initialized:
            await self.initialize()
            
        if not self.initialized:
            return {"error": "System not initialized"}
            
        try:
            # Context data
            context_data = {
                "user_id": "tester",
                "conversation_id": "test_session",
                "platform": "test",
                "timestamp": datetime.now().isoformat()
            }
            
            # Process query
            result = await self.integrator.process_message(
                message=query,
                conversation_history=self.conversation_history,
                context_data=context_data
            )
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": query})
            if "response" in result and result["response"]:
                self.conversation_history.append({"role": "assistant", "content": result["response"]})
                
            # Limit history size
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
                
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {"error": str(e)}
            
    def display_result(self, result: Dict[str, Any]) -> None:
        """
        Displays the processing result in a user-friendly way on the console.
        
        Args:
            result: Processing result
        """
        if "error" in result:
            print("\n❌ Error:")
            print(f"  {result['error']}")
            return
            
        # Display response
        if "response" in result and result["response"]:
            print("\n✨ Response:")
            print(f"{result['response']}")
            
        # Display additional information
        print("\n📊 Additional Information:")
        
        if "model_used" in result:
            print(f"  Model used: {result['model_used']}")
            
        if "complexity" in result:
            print(f"  Query complexity: {result['complexity']:.2f}")
            
        if "knowledge_used" in result:
            print(f"  Knowledge used: {'Yes' if result['knowledge_used'] else 'No'}")
            
        # Display relevant knowledge if available
        if "knowledge_package" in result and "relevant_knowledge" in result["knowledge_package"]:
            relevant = result["knowledge_package"]["relevant_knowledge"]
            if relevant:
                print("\n📚 Relevant Knowledge Found:")
                for i, item in enumerate(relevant[:3], 1):
                    print(f"  {i}. {item.get('text', '')[:100]}...")
            else:
                print("\n📚 No specific knowledge found for this query.")
                
        print("\n" + "-" * 80)
            
    async def run_interactive(self) -> None:
        """
        Runs the tester in interactive mode.
        """
        # Initialize system
        if not self.initialized:
            await self.initialize()
            
        if not self.initialized:
            print("❌ Failed to initialize the system. Check the logs.")
            return
            
        # Print header
        print("\n" + "=" * 80)
        print("     ✧༺❀༻∞ EVA & GUARANI Quantum Knowledge System Tester ∞༺❀༻✧")
        print("=" * 80)
        print("\nEnter your queries to test the system (Type 'exit' to quit).")
        print("Special commands:")
        print("  !clear    - Clears the conversation history")
        print("  !info     - Displays information about the system")
        print("  !reindex  - Reindex knowledge")
        print("-" * 80)
        
        # Main loop
        while True:
            try:
                # Request user input
                query = input("\n📝 Enter your query: ")
                
                # Check special commands
                if query.lower() == "exit":
                    print("\n✨ Exiting the tester. Goodbye!")
                    break
                elif query.lower() == "!clear":
                    self.conversation_history = []
                    print("\n🧹 Conversation history cleared.")
                    continue
                elif query.lower() == "!info":
                    print("\n📋 System Information:")
                    print(f"  Initialization state: {'✓' if self.initialized else '✗'}")
                    print(f"  Messages in history: {len(self.conversation_history)}")
                    
                    # Display configurations
                    if hasattr(self.integrator, 'config'):
                        print("  Integrator configurations:")
                        for key, value in self.integrator.config.items():
                            if key in ["economic_model", "premium_model", "complexity_threshold"]:
                                print(f"    {key}: {value}")
                    continue
                elif query.lower() == "!reindex":
                    if self.hub:
                        count = await self.hub.index_quantum_prompts()
                        print(f"\n🔄 Reindexed {count} quantum prompts.")
                    else:
                        print("\n❌ Hub not initialized.")
                    continue
                    
                # Process query
                print("\n⏳ Processing query...")
                result = await self.process_query(query)
                
                # Display result
                self.display_result(result)
                
            except KeyboardInterrupt:
                print("\n\n✨ Exiting the tester. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    def close(self) -> None:
        """
        Closes the tester and releases resources.
        """
        try:
            if self.integrator:
                self.integrator.close()
                
            self.logger.info("Tester closed")
            
        except Exception as e:
            self.logger.error(f"Error closing tester: {e}")

# Function to run a single test
async def run_single_test(query: str) -> None:
    """
    Runs a single test with the provided query.
    
    Args:
        query: Query to be tested
    """
    tester = QuantumKnowledgeTester()
    await tester.initialize()
    
    print(f"\n📝 Query: {query}")
    print("\n⏳ Processing query...")
    
    result = await tester.process_query(query)
    tester.display_result(result)
    
    tester.close()

# Main function
async def main():
    """
    Main function of the tester.
    """
    # Configure argument parser
    parser = argparse.ArgumentParser(description="EVA & GUARANI Quantum Knowledge System Tester")
    parser.add_argument("--query", "-q", type=str, help="Query to be tested (non-interactive mode)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check execution mode
    if args.query:
        # Non-interactive mode
        await run_single_test(args.query)
    else:
        # Interactive mode
        tester = QuantumKnowledgeTester()
        await tester.run_interactive()
        tester.close()

if __name__ == "__main__":
    # Check if we are in an asynchronous environment or not
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already in a loop, create a task
            asyncio.create_task(main())
        else:
            # If not in a loop, run directly
            loop.run_until_complete(main())
    except RuntimeError:
        # If no loop, create a new one
        asyncio.run(main())