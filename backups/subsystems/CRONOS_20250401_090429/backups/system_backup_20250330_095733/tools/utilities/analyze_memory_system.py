#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Memory System Analyzer
This script analyzes how the system stores memories and generates a detailed report.
"""

import os
import json
import logging
import datetime
import glob
import time
from typing import Dict, List, Any, Optional, Tuple

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/memory_analysis.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Constants
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DATA_DIR = "data"
MEMORY_DIRS = [
    "data/memories",
    "data/consciousness",
    "data/conversations",
    "data/quantum_memory",
    "data/ethik",
]
PAYMENTS_DIR = "data/payments"

class MemoryAnalyzer:
    """Memory system analyzer for EVA & GUARANI."""
    
    def __init__(self, data_dir: str = DATA_DIR, output_dir: str = "reports"):
        """
        Initializes the memory analyzer.
        
        Args:
            data_dir: Data directory to be analyzed
            output_dir: Directory to save reports
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.results: Dict[str, Any] = {
            "timestamp": TIMESTAMP,
            "memory_subsystems": {},
            "payments": {},
            "conversations": {},
            "summary": {}
        }
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Memory analyzer initialized: data_dir={data_dir}")
    
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """
        Analyzes a memory directory.
        
        Args:
            directory: Path of the directory to be analyzed
            
        Returns:
            Dictionary with information about the directory
        """
        if not os.path.exists(directory):
            logger.warning(f"Directory not found: {directory}")
            return {
                "exists": False,
                "files_count": 0,
                "total_size_bytes": 0,
                "files": []
            }
        
        dir_info = {
            "exists": True,
            "files_count": 0,
            "total_size_bytes": 0,
            "files": []
        }
        
        # List all files recursively
        all_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        
        # Analyze each file
        for file_path in all_files:
            file_size = os.path.getsize(file_path)
            file_info = {
                "path": file_path,
                "size_bytes": file_size,
                "last_modified": time.ctime(os.path.getmtime(file_path))
            }
            
            # Try to read JSON file contents
            if file_path.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Determine file type
                    file_type = "unknown"
                    if "users" in data and "transactions" in data:
                        file_type = "payment_data"
                    elif "user_id" in data and "messages" in data:
                        file_type = "conversation"
                    elif "working_memory" in data or "long_term_memory" in data:
                        file_type = "quantum_memory"
                    
                    file_info["type"] = file_type
                    file_info["item_count"] = len(data) if isinstance(data, list) else len(data.keys())
                except Exception as e:
                    file_info["error"] = str(e)
            
            dir_info["files"].append(file_info)
            dir_info["total_size_bytes"] += file_size
        
        dir_info["files_count"] = len(dir_info["files"])
        logger.info(f"Directory analyzed: {directory} ({dir_info['files_count']} files)")
        return dir_info
    
    def analyze_payments(self) -> Dict[str, Any]:
        """
        Analyzes the payment system.
        
        Returns:
            Dictionary with information about the payment system
        """
        payments_path = os.path.join(PAYMENTS_DIR, "payments.json")
        payments_info = {
            "file_exists": os.path.exists(payments_path),
            "size_bytes": 0,
            "users_count": 0,
            "transactions_count": 0,
            "file_path": payments_path
        }
        
        if payments_info["file_exists"]:
            payments_info["size_bytes"] = os.path.getsize(payments_path)
            
            try:
                with open(payments_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "users" in data:
                    payments_info["users_count"] = len(data["users"])
                
                if "transactions" in data:
                    payments_info["transactions_count"] = len(data["transactions"])
                    
                    # Analyze user tiers
                    tier_stats = {"free_tier": 0, "supporter_tier": 0, "premium_tier": 0}
                    for user_id, user_data in data.get("users", {}).items():
                        tier = user_data.get("tier", "free_tier")
                        if tier in tier_stats:
                            tier_stats[tier] += 1
                    
                    payments_info["tier_stats"] = tier_stats
                    
                    # Analyze credits statistics
                    credits_stats = {
                        "total_special_calls": 0,
                        "total_internet_calls": 0,
                        "avg_special_calls": 0,
                        "avg_internet_calls": 0
                    }
                    
                    for user_id, user_data in data.get("users", {}).items():
                        if "credits" in user_data:
                            credits_stats["total_special_calls"] += user_data["credits"].get("special_calls", 0)
                            credits_stats["total_internet_calls"] += user_data["credits"].get("internet_calls", 0)
                    
                    if payments_info["users_count"] > 0:
                        credits_stats["avg_special_calls"] = credits_stats["total_special_calls"] / payments_info["users_count"]
                        credits_stats["avg_internet_calls"] = credits_stats["total_internet_calls"] / payments_info["users_count"]
                    
                    payments_info["credits_stats"] = credits_stats
            except Exception as e:
                payments_info["error"] = str(e)
        
        logger.info(f"Payment system analyzed: {payments_info['users_count']} users")
        return payments_info
    
    def analyze_conversations(self) -> Dict[str, Any]:
        """
        Analyzes the conversation system.
        
        Returns:
            Dictionary with information about the conversation system
        """
        conversations_dir = os.path.join(DATA_DIR, "conversations")
        conversation_files = glob.glob(os.path.join(conversations_dir, "conversation_*.json"))
        
        conversations_info = {
            "directory_exists": os.path.exists(conversations_dir),
            "total_conversations": len(conversation_files),
            "total_size_bytes": 0,
            "total_messages": 0,
            "conversations": []
        }
        
        for conv_file in conversation_files:
            conv_info = {
                "file_path": conv_file,
                "size_bytes": os.path.getsize(conv_file),
                "messages_count": 0,
                "last_updated": time.ctime(os.path.getmtime(conv_file))
            }
            
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract user information
                conv_info["user_id"] = data.get("user_id")
                conv_info["username"] = data.get("username")
                
                if "messages" in data:
                    conv_info["messages_count"] = len(data["messages"])
                    conversations_info["total_messages"] += conv_info["messages_count"]
                
                # Extract creation and update dates
                conv_info["created_at"] = data.get("created_at")
                conv_info["updated_at"] = data.get("updated_at")
            except Exception as e:
                conv_info["error"] = str(e)
            
            conversations_info["conversations"].append(conv_info)
            conversations_info["total_size_bytes"] += conv_info["size_bytes"]
        
        # Calculate statistics
        if conversations_info["total_conversations"] > 0:
            conversations_info["avg_messages_per_conversation"] = (
                conversations_info["total_messages"] / conversations_info["total_conversations"]
            )
            conversations_info["avg_size_per_conversation"] = (
                conversations_info["total_size_bytes"] / conversations_info["total_conversations"]
            )
        
        logger.info(f"Conversation system analyzed: {conversations_info['total_conversations']} conversations")
        return conversations_info
    
    def analyze_memory_subsystems(self) -> None:
        """
        Analyzes all memory subsystems.
        """
        for memory_dir in MEMORY_DIRS:
            dir_name = os.path.basename(memory_dir)
            self.results["memory_subsystems"][dir_name] = self.analyze_directory(memory_dir)
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generates a summary of the analysis.
        
        Returns:
            Dictionary with the analysis summary
        """
        summary = {
            "total_memory_subsystems": len(self.results["memory_subsystems"]),
            "active_memory_subsystems": sum(
                1 for info in self.results["memory_subsystems"].values() 
                if info.get("exists", False) and info.get("files_count", 0) > 0
            ),
            "total_files": sum(
                info.get("files_count", 0) 
                for info in self.results["memory_subsystems"].values()
            ),
            "total_size_bytes": sum(
                info.get("total_size_bytes", 0) 
                for info in self.results["memory_subsystems"].values()
            ),
            "storage_method": "File system",
            "users_count": self.results["payments"].get("users_count", 0),
            "conversations_count": self.results["conversations"].get("total_conversations", 0),
            "messages_count": self.results["conversations"].get("total_messages", 0)
        }
        
        # Determine primary storage format
        if summary["total_files"] > 0:
            json_files = sum(
                len([f for f in info.get("files", []) if f.get("path", "").endswith(".json")])
                for info in self.results["memory_subsystems"].values()
            )
            
            if json_files / summary["total_files"] > 0.8:
                summary["primary_format"] = "JSON"
            else:
                summary["primary_format"] = "Mixed"
        
        logger.info(f"Summary generated: {summary['active_memory_subsystems']} active subsystems")
        return summary
    
    def generate_report(self) -> str:
        """
        Generates a complete analysis report and saves it to a file.
        
        Returns:
            Path of the generated report file
        """
        # Analyze subsystems
        self.analyze_memory_subsystems()
        
        # Analyze payment system
        self.results["payments"] = self.analyze_payments()
        
        # Analyze conversation system
        self.results["conversations"] = self.analyze_conversations()
        
        # Generate summary
        self.results["summary"] = self.generate_summary()
        
        # Save report to JSON file
        report_path = os.path.join(self.output_dir, f"memory_analysis_{TIMESTAMP}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        
        # Generate text report
        report_txt_path = os.path.join(self.output_dir, f"memory_analysis_{TIMESTAMP}.txt")
        self._generate_text_report(report_txt_path)
        
        logger.info(f"Report generated: {report_path}")
        logger.info(f"Text report: {report_txt_path}")
        return report_txt_path
    
    def _generate_text_report(self, filepath: str) -> None:
        """
        Generates a text format report.
        
        Args:
            filepath: Path of the output file
        """
        summary = self.results["summary"]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write(f"EVA & GUARANI MEMORY SYSTEM ANALYSIS REPORT\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write("## GENERAL SUMMARY\n\n")
            f.write(f"• Storage method: {summary.get('storage_method', 'Unknown')}\n")
            f.write(f"• Primary format: {summary.get('primary_format', 'Unknown')}\n")
            f.write(f"• Active subsystems: {summary.get('active_memory_subsystems', 0)} of {summary.get('total_memory_subsystems', 0)}\n")
            f.write(f"• Total files: {summary.get('total_files', 0)}\n")
            f.write(f"• Total size: {summary.get('total_size_bytes', 0) / (1024*1024):.2f} MB\n")
            f.write(f"• Number of users: {summary.get('users_count', 0)}\n")
            f.write(f"• Number of conversations: {summary.get('conversations_count', 0)}\n")
            f.write(f"• Number of messages: {summary.get('messages_count', 0)}\n\n")
            
            f.write("## PAYMENT SYSTEM\n\n")
            payments = self.results["payments"]
            f.write(f"• File: {payments.get('file_path', 'N/A')}\n")
            f.write(f"• Exists: {payments.get('file_exists', False)}\n")
            f.write(f"• Size: {payments.get('size_bytes', 0) / 1024:.2f} KB\n")
            f.write(f"• Users: {payments.get('users_count', 0)}\n")
            f.write(f"• Transactions: {payments.get('transactions_count', 0)}\n")
            
            tier_stats = payments.get("tier_stats", {})
            if tier_stats:
                f.write(f"• Plan distribution:\n")
                f.write(f"  - Free: {tier_stats.get('free_tier', 0)}\n")
                f.write(f"  - Supporter: {tier_stats.get('supporter_tier', 0)}\n")
                f.write(f"  - Premium: {tier_stats.get('premium_tier', 0)}\n")
            
            f.write("\n## CONVERSATIONS\n\n")
            convs = self.results["conversations"]
            f.write(f"• Total conversations: {convs.get('total_conversations', 0)}\n")
            f.write(f"• Total messages: {convs.get('total_messages', 0)}\n")
            f.write(f"• Total size: {convs.get('total_size_bytes', 0) / (1024):.2f} KB\n")
            f.write(f"• Average messages per conversation: {convs.get('avg_messages_per_conversation', 0):.2f}\n\n")
            
            f.write("## MEMORY SUBSYSTEMS\n\n")
            for name, subsystem in self.results["memory_subsystems"].items():
                f.write(f"### {name.upper()}\n\n")
                f.write(f"• Exists: {subsystem.get('exists', False)}\n")
                f.write(f"• Files: {subsystem.get('files_count', 0)}\n")
                f.write(f"• Size: {subsystem.get('total_size_bytes', 0) / 1024:.2f} KB\n\n")
            
            f.write("="*80 + "\n")
            f.write("End of report\n")
            f.write("="*80 + "\n")

def main():
    """Main function."""
    print("="*80)
    print("EVA & GUARANI MEMORY SYSTEM ANALYZER")
    print("="*80)
    
    start_time = time.time()
    analyzer = MemoryAnalyzer()
    report_path = analyzer.generate_report()
    
    duration = time.time() - start_time
    print(f"\nAnalysis completed in {duration:.2f} seconds!")
    print(f"Report saved at: {report_path}")
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()