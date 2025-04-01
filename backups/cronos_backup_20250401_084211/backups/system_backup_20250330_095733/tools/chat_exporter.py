#!/usr/bin/env python3
"""
# ========================================================================
# CHAT EXPORTER - Comprehensive Chat Export Tool for EVA & GUARANI
# ========================================================================
#
# This tool helps extract and save ALL chat conversations from Cursor or 
# other sources to ensure no information is lost during development.
#
# Features:
# 1. Export all conversations to a dedicated CHATS directory
# 2. Extract context from previous conversation summaries
# 3. Format conversations with timestamps and metadata
# 4. Integrates with BIOS-Q for context preservation
# 
# ========================================================================
"""

import os
import sys
import re
import json
import datetime
import argparse
from pathlib import Path

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import conversation exporter
try:
    from tools.conversation_exporter import export_conversation
    CONVERSATION_EXPORTER_AVAILABLE = True
except ImportError:
    CONVERSATION_EXPORTER_AVAILABLE = False

# Try to import quantum utils for BIOS-Q integration
try:
    from core.quantum_utils import (
        trigger_context_preservation,
        extract_context_from_conversation,
        detect_language
    )
    QUANTUM_UTILS_AVAILABLE = True
except ImportError:
    QUANTUM_UTILS_AVAILABLE = False

# ========================================================================
# CONFIGURATION
# ========================================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHATS_DIR = os.path.join(PROJECT_ROOT, "CHATS")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs", "conversations")
CHAT_INDEX_FILE = os.path.join(CHATS_DIR, "chat_index.json")
CHAT_METADATA_DIR = os.path.join(CHATS_DIR, "metadata")
QUANTUM_SIGNATURE = "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(CHATS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(CHAT_METADATA_DIR, exist_ok=True)
    return True

def clean_text(text):
    """Clean up text for saving"""
    # Remove any special control characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

def extract_conversation_from_summary(summary_text):
    """Extract conversation details from a summary section"""
    title_match = re.search(r'Conversation Title: (.+?)\n', summary_text)
    title = title_match.group(1) if title_match else "Unknown Title"
    
    # Extract the summary content
    summary_content = re.search(r'<summary>\s*([\s\S]*?)\s*</summary>', summary_text)
    summary = summary_content.group(1).strip() if summary_content else "No summary available"
    
    return {
        "title": title,
        "summary": summary,
        "extracted_from": "summary",
        "timestamp": datetime.datetime.now().isoformat()
    }

def extract_conversation_from_user_query(query_text):
    """Extract content from user query section"""
    # Clean up the text
    clean_query = query_text.strip()
    
    # Create summary based on first sentence or first 100 chars
    first_sentence = re.split(r'[.!?]', clean_query)[0]
    summary = (first_sentence[:100] + '...') if len(first_sentence) > 100 else first_sentence
    
    return {
        "content": clean_query,
        "summary": summary,
        "extracted_from": "user_query",
        "timestamp": datetime.datetime.now().isoformat()
    }

def parse_conversation_data(text):
    """Parse conversation data from the provided text"""
    conversations = []
    
    # Extract previous conversation summaries
    summary_sections = re.findall(r'<conversation_summary>([\s\S]*?)</conversation_summary>', text)
    for summary in summary_sections:
        conversations.append(extract_conversation_from_summary(summary))
    
    # Extract user queries
    query_sections = re.findall(r'<user_query>([\s\S]*?)</user_query>', text)
    for query in query_sections:
        conversations.append(extract_conversation_from_user_query(query))
    
    # If no structured data found, treat as raw conversation
    if not conversations:
        # Try to identify Human/Assistant patterns
        human_sections = re.findall(r'Human:([\s\S]*?)(?=Assistant:|$)', text)
        assistant_sections = re.findall(r'Assistant:([\s\S]*?)(?=Human:|$)', text)
        
        if human_sections or assistant_sections:
            # Reconstruct conversation
            raw_conversation = ""
            for i in range(max(len(human_sections), len(assistant_sections))):
                if i < len(human_sections):
                    raw_conversation += f"Human: {human_sections[i].strip()}\n\n"
                if i < len(assistant_sections):
                    raw_conversation += f"Assistant: {assistant_sections[i].strip()}\n\n"
            
            conversations.append({
                "content": raw_conversation,
                "summary": "Reconstructed conversation",
                "extracted_from": "raw_text",
                "timestamp": datetime.datetime.now().isoformat()
            })
        else:
            # Just use the raw text
            conversations.append({
                "content": text,
                "summary": text[:100] + "..." if len(text) > 100 else text,
                "extracted_from": "raw_text",
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    return conversations

def generate_chat_id(content, prefix="chat"):
    """Generate a unique ID for a chat based on content hash and timestamp"""
    import hashlib
    
    # Create hash from content
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
    
    # Get timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{prefix}_{timestamp}_{content_hash}"

def save_chat(chat_data, chat_id=None):
    """Save a chat to the CHATS directory"""
    ensure_directories()
    
    # Generate ID if not provided
    if not chat_id:
        content = chat_data.get("content", chat_data.get("summary", ""))
        chat_id = generate_chat_id(content)
    
    # Create chat file path
    chat_file = os.path.join(CHATS_DIR, f"{chat_id}.md")
    
    # Format chat content
    title = chat_data.get("title", "Chat Export")
    summary = chat_data.get("summary", "No summary available")
    content = chat_data.get("content", "")
    timestamp = chat_data.get("timestamp", datetime.datetime.now().isoformat())
    
    # Format as markdown
    md_content = f"# {title}\n\n"
    md_content += f"**Date**: {timestamp}\n\n"
    md_content += f"**Summary**: {summary}\n\n"
    md_content += "---\n\n"
    md_content += content
    md_content += "\n\n---\n\n"
    md_content += f"{QUANTUM_SIGNATURE}\n"
    
    # Save the file
    with open(chat_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Save metadata
    metadata = {
        "chat_id": chat_id,
        "title": title,
        "summary": summary,
        "timestamp": timestamp,
        "file_path": chat_file,
        "extracted_from": chat_data.get("extracted_from", "unknown"),
        "language": detect_language(content) if QUANTUM_UTILS_AVAILABLE else "unknown"
    }
    
    metadata_file = os.path.join(CHAT_METADATA_DIR, f"{chat_id}_metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Update chat index
    update_chat_index(chat_id, metadata)
    
    return chat_file

def update_chat_index(chat_id, metadata):
    """Update the chat index file with new chat information"""
    # Load existing index
    chat_index = {}
    if os.path.exists(CHAT_INDEX_FILE):
        try:
            with open(CHAT_INDEX_FILE, 'r', encoding='utf-8') as f:
                chat_index = json.load(f)
        except:
            chat_index = {"chats": {}}
    else:
        chat_index = {"chats": {}}
    
    # Add/update this chat
    chat_index["chats"][chat_id] = {
        "title": metadata.get("title", "Untitled"),
        "summary": metadata.get("summary", "No summary"),
        "timestamp": metadata.get("timestamp", datetime.datetime.now().isoformat()),
        "file_path": metadata.get("file_path", ""),
        "language": metadata.get("language", "unknown")
    }
    
    # Update last_updated timestamp
    chat_index["last_updated"] = datetime.datetime.now().isoformat()
    
    # Save the index
    with open(CHAT_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(chat_index, f, indent=2)
    
    return True

def detect_language(text):
    """Detect language of text if quantum_utils not available"""
    if QUANTUM_UTILS_AVAILABLE:
        from core.quantum_utils import detect_language
        return detect_language(text)
    
    # Simple fallback detection
    english_words = ["the", "is", "and", "in", "to", "of", "that", "for"]
    portuguese_words = ["o", "a", "e", "de", "que", "para", "em", "com"]
    
    english_count = sum(1 for word in english_words if f" {word} " in f" {text.lower()} ")
    portuguese_count = sum(1 for word in portuguese_words if f" {word} " in f" {text.lower()} ")
    
    return "pt" if portuguese_count > english_count else "en"

# ========================================================================
# MAIN EXPORT FUNCTIONS
# ========================================================================

def export_all_conversations(text_input=None):
    """Export all conversations that can be accessed"""
    print(f"\n{QUANTUM_SIGNATURE}")
    print("CHAT EXPORTER - Saving All Conversations")
    print("=========================================\n")
    
    ensure_directories()
    
    # Save current conversation if provided
    if text_input:
        print("📋 Processing current conversation...")
        conversations = parse_conversation_data(text_input)
        
        for i, conv in enumerate(conversations):
            chat_id = generate_chat_id(conv.get("content", conv.get("summary", "")), f"current_{i+1}")
            file_path = save_chat(conv, chat_id)
            print(f"✅ Saved conversation {i+1} to: {os.path.basename(file_path)}")
            
            # Integrate with BIOS-Q if available
            if QUANTUM_UTILS_AVAILABLE:
                trigger_context_preservation(conv.get("content", ""), source_name="chat_exporter")
    
    # Process conversation summaries if available
    print("\n📚 Checking for previous conversation summaries...")
    if text_input:
        summary_count = len(re.findall(r'<conversation_summary>', text_input))
        if summary_count > 0:
            print(f"✓ Found {summary_count} conversation summaries")
        else:
            print("⚠️ No structured conversation summaries found")
    
    # Look for chat logs in the logs directory
    print("\n🔍 Looking for conversation logs...")
    log_files = list(Path(LOGS_DIR).glob("*.md")) + list(Path(LOGS_DIR).glob("*.txt"))
    
    if log_files:
        print(f"✓ Found {len(log_files)} conversation log files")
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                chat_id = generate_chat_id(log_content, f"log_{log_file.stem}")
                
                # Extract basic info
                title_match = re.search(r'# (.+?)(?:\n|$)', log_content)
                title = title_match.group(1) if title_match else log_file.stem
                
                chat_data = {
                    "title": title,
                    "content": log_content,
                    "summary": f"Imported from log file: {log_file.name}",
                    "timestamp": datetime.datetime.fromtimestamp(log_file.stat().st_mtime).isoformat(),
                    "extracted_from": "log_file"
                }
                
                file_path = save_chat(chat_data, chat_id)
                print(f"✅ Imported log: {os.path.basename(file_path)}")
                
            except Exception as e:
                print(f"⚠️ Error processing log file {log_file.name}: {str(e)}")
    else:
        print("⚠️ No conversation log files found")
    
    # Generate report
    chat_count = 0
    if os.path.exists(CHAT_INDEX_FILE):
        try:
            with open(CHAT_INDEX_FILE, 'r', encoding='utf-8') as f:
                chat_index = json.load(f)
                chat_count = len(chat_index.get("chats", {}))
        except:
            pass
    
    print("\n📊 Export Summary:")
    print(f"- Total conversations saved: {chat_count}")
    print(f"- Chat directory: {CHATS_DIR}")
    print(f"- Chat index file: {CHAT_INDEX_FILE}")
    
    print(f"\n{QUANTUM_SIGNATURE}")
    return chat_count

def generate_chat_report():
    """Generate a report of all saved chats"""
    if not os.path.exists(CHAT_INDEX_FILE):
        print("⚠️ No chat index found. Please run export_all_conversations first.")
        return None
    
    try:
        with open(CHAT_INDEX_FILE, 'r', encoding='utf-8') as f:
            chat_index = json.load(f)
        
        chats = chat_index.get("chats", {})
        report_file = os.path.join(CHATS_DIR, "chat_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# EVA & GUARANI - Chat Archive Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total chats: {len(chats)}\n\n")
            
            # Group by language
            languages = {}
            for chat_id, chat in chats.items():
                lang = chat.get("language", "unknown")
                if lang not in languages:
                    languages[lang] = []
                languages[lang].append(chat)
            
            f.write("## Language Distribution\n\n")
            for lang, lang_chats in languages.items():
                f.write(f"- {lang.upper()}: {len(lang_chats)} chats\n")
            
            f.write("\n## Chat Index\n\n")
            
            # Sort by timestamp
            sorted_chats = sorted(
                [(cid, c) for cid, c in chats.items()],
                key=lambda x: x[1].get("timestamp", ""),
                reverse=True
            )
            
            for chat_id, chat in sorted_chats:
                title = chat.get("title", "Untitled")
                timestamp = chat.get("timestamp", "")
                try:
                    dt = datetime.datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
                
                f.write(f"### {title}\n\n")
                f.write(f"- **ID**: {chat_id}\n")
                f.write(f"- **Date**: {formatted_time}\n")
                f.write(f"- **Language**: {chat.get('language', 'unknown').upper()}\n")
                f.write(f"- **File**: [{os.path.basename(chat.get('file_path', ''))}]({chat.get('file_path', '')})\n")
                f.write(f"- **Summary**: {chat.get('summary', 'No summary available')}\n\n")
            
            f.write(f"\n{QUANTUM_SIGNATURE}\n")
        
        print(f"✅ Chat report generated: {report_file}")
        return report_file
        
    except Exception as e:
        print(f"⚠️ Error generating chat report: {str(e)}")
        return None

# ========================================================================
# COMMAND LINE INTERFACE
# ========================================================================

def main():
    """Command line interface for the chat exporter"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI Chat Exporter")
    parser.add_argument('-i', '--input', help='Input file with conversation text', default=None)
    parser.add_argument('-r', '--report', help='Generate chat report', action='store_true')
    
    args = parser.parse_args()
    
    # Get text from input file if provided
    text = None
    if args.input and os.path.exists(args.input):
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"📄 Read input from file: {args.input}")
        except Exception as e:
            print(f"⚠️ Error reading input file: {str(e)}")
    
    # Export conversations
    export_all_conversations(text)
    
    # Generate report if requested
    if args.report:
        generate_chat_report()

if __name__ == "__main__":
    main() 