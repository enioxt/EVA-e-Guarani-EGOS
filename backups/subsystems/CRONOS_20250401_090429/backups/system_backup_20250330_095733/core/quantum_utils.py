#!/usr/bin/env python3
"""
# ========================================================================
# QUANTUM UTILS - Utility Functions for EVA & GUARANI Core Modules
# ========================================================================
#
# This module provides utility functions that help connect and integrate
# various components of the EVA & GUARANI system.
#
# Features:
# 1. BIOS-Q integration helpers
# 2. Conversation preservation utilities
# 3. Common formatting and processing functions
# 4. Language management
#
# ========================================================================
"""

import os
import sys
import datetime
import json
import re
from pathlib import Path

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import conversation exporter
try:
    from tools.conversation_exporter import export_conversation

    CONVERSATION_EXPORTER_AVAILABLE = True
except ImportError:
    CONVERSATION_EXPORTER_AVAILABLE = False

# ========================================================================
# CONFIGURATION
# ========================================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUANTUM_SIGNATURE = "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
CONTEXT_STORAGE_DIR = os.path.join(PROJECT_ROOT, "logs", "context")
DEFAULT_LANGUAGE = "en"  # English as default
LANGUAGE_CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "language_settings.json")

# ========================================================================
# LANGUAGE MANAGEMENT
# ========================================================================


def get_system_language():
    """Get the current system language setting"""
    try:
        if os.path.exists(LANGUAGE_CONFIG_FILE):
            with open(LANGUAGE_CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("system_language", DEFAULT_LANGUAGE)
        return DEFAULT_LANGUAGE
    except Exception as e:
        print(f"Error loading language settings: {str(e)}")
        return DEFAULT_LANGUAGE


def set_system_language(language_code):
    """Set the system language"""
    try:
        os.makedirs(os.path.dirname(LANGUAGE_CONFIG_FILE), exist_ok=True)

        config = {}
        if os.path.exists(LANGUAGE_CONFIG_FILE):
            with open(LANGUAGE_CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)

        config["system_language"] = language_code
        config["last_updated"] = datetime.datetime.now().isoformat()

        with open(LANGUAGE_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        print(f"System language set to: {language_code}")
        return True
    except Exception as e:
        print(f"Error setting language: {str(e)}")
        return False


def detect_language(text):
    """Detect the language of the provided text"""
    try:
        # Try to use the language detection library
        try:
            from lingua import Language, LanguageDetectorBuilder

            languages = [Language.ENGLISH, Language.PORTUGUESE]
            detector = LanguageDetectorBuilder.from_languages(*languages).build()
            result = detector.detect_language_of(text)
            if result:
                if result == Language.ENGLISH:
                    return "en"
                elif result == Language.PORTUGUESE:
                    return "pt"
        except ImportError:
            pass

        # Fallback to simple heuristics
        portuguese_indicators = ["ção", "ões", "não", "está", "você", "como"]
        english_indicators = ["the", "and", "is", "are", "what", "with"]

        pt_count = sum(1 for word in portuguese_indicators if word in text.lower())
        en_count = sum(1 for word in english_indicators if word in text.lower())

        if pt_count > en_count:
            return "pt"
        return "en"
    except Exception:
        return DEFAULT_LANGUAGE


# ========================================================================
# BIOS-Q INTEGRATION FUNCTIONS
# ========================================================================


def register_conversation_with_biosq(conversation_path, metadata=None):
    """
    Registers a saved conversation with the BIOS-Q system for context preservation

    Args:
        conversation_path: Path to the saved conversation file
        metadata: Optional dictionary with additional metadata

    Returns:
        bool: Success status
    """
    try:
        # Try to import BIOS-Q dynamically to avoid circular imports
        from core.bios_quantum import BIOSQuantum

        # Initialize BIOS-Q
        biosq = BIOSQuantum()

        # Log conversation registration
        biosq.log(f"Registering conversation: {os.path.basename(conversation_path)}")

        # Create or update context file for BIOS-Q
        context_file = os.path.join(CONTEXT_STORAGE_DIR, "conversation_context.json")
        os.makedirs(os.path.dirname(context_file), exist_ok=True)

        # Extract metadata from conversation
        if metadata is None:
            metadata = {}

        # Try to read the conversation file to get context
        conversation_text = ""
        try:
            with open(conversation_path, "r", encoding="utf-8") as f:
                conversation_text = f.read()
        except Exception as e:
            biosq.log(f"Error reading conversation file: {str(e)}", level="WARNING")

        # Get context from the conversation
        if conversation_text:
            context_data = extract_context_from_conversation(conversation_text)
            metadata.update(context_data)

            # Detect language of the conversation
            detected_language = detect_language(conversation_text)
            metadata["detected_language"] = detected_language

        # Update the context file
        context_data = {
            "last_conversation": os.path.basename(conversation_path),
            "timestamp": datetime.datetime.now().isoformat(),
            "conversations": [],
        }

        if os.path.exists(context_file):
            try:
                with open(context_file, "r", encoding="utf-8") as f:
                    context_data = json.load(f)
            except:
                pass

        # Add the new conversation to the context
        context_data["conversations"].append(
            {
                "path": conversation_path,
                "timestamp": datetime.datetime.now().isoformat(),
                "metadata": metadata,
            }
        )

        # Keep only the last 10 conversations
        if len(context_data["conversations"]) > 10:
            context_data["conversations"] = context_data["conversations"][-10:]

        # Save updated context
        with open(context_file, "w", encoding="utf-8") as f:
            json.dump(context_data, f, indent=2)

        biosq.log(f"Context updated with conversation: {os.path.basename(conversation_path)}")
        return True

    except ImportError:
        print("⚠️ BIOS-Q module not available. Conversation not registered.")
        return False
    except Exception as e:
        print(f"⚠️ Error registering conversation with BIOS-Q: {str(e)}")
        return False


def get_conversation_context():
    """
    Retrieve the conversation context from BIOS-Q

    Returns:
        dict: The conversation context
    """
    context_file = os.path.join(CONTEXT_STORAGE_DIR, "conversation_context.json")

    if not os.path.exists(context_file):
        return {
            "last_conversation": None,
            "timestamp": datetime.datetime.now().isoformat(),
            "conversations": [],
        }

    try:
        with open(context_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading conversation context: {str(e)}")
        return {
            "last_conversation": None,
            "timestamp": datetime.datetime.now().isoformat(),
            "conversations": [],
        }


def load_past_conversations(limit=3):
    """
    Load the most recent conversations for context

    Args:
        limit: Maximum number of conversations to load

    Returns:
        list: List of conversation texts
    """
    context = get_conversation_context()
    conversations = []

    # Get the most recent conversations
    recent_conversations = sorted(
        context.get("conversations", []), key=lambda x: x.get("timestamp", ""), reverse=True
    )[:limit]

    for conv_info in recent_conversations:
        path = conv_info.get("path")
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    conversations.append(
                        {"text": f.read(), "metadata": conv_info.get("metadata", {})}
                    )
            except Exception as e:
                print(f"⚠️ Error loading conversation from {path}: {str(e)}")

    return conversations


# ========================================================================
# CONVERSATION PRESERVATION FUNCTIONS
# ========================================================================


def preserve_conversation(text, source_name="cursor", metadata=None):
    """
    Preserves a conversation by exporting it and registering with BIOS-Q

    Args:
        text: The conversation text
        source_name: Name of the conversation source
        metadata: Optional dictionary with additional metadata

    Returns:
        tuple: (success status, output file path)
    """
    # Default metadata
    if metadata is None:
        metadata = {}

    # Detect language of the conversation
    detected_language = detect_language(text)

    metadata.update(
        {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": source_name,
            "detected_language": detected_language,
        }
    )

    # Generate a unique output filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{source_name}_conversation_{timestamp}"

    # Export the conversation
    if CONVERSATION_EXPORTER_AVAILABLE:
        print(f"🔄 Exporting conversation from {source_name}...")

        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(PROJECT_ROOT, "logs", "conversations")
        os.makedirs(logs_dir, exist_ok=True)

        # Export using the conversation exporter tool
        output_path = os.path.join(logs_dir, output_filename)
        success = export_conversation(
            clipboard_text=text, output_path=output_path, format_type="both"
        )

        # Register with BIOS-Q if successful
        if success:
            md_path = f"{output_path}.md"
            register_conversation_with_biosq(md_path, metadata)

            print(f"✅ Conversation preserved successfully")
            print(f"📂 Exported to: {md_path}")
            print(f"🔍 Detected language: {detected_language}")
            return True, md_path
        else:
            print("⚠️ Failed to export conversation")
            return False, None
    else:
        print("⚠️ Conversation exporter not available")
        print("💡 You can save your conversation manually by copying to a text file")
        return False, None


def extract_context_from_conversation(text, keywords=None):
    """
    Extracts important context from conversation based on keywords

    Args:
        text: The conversation text
        keywords: List of keywords to search for

    Returns:
        dict: Extracted context
    """
    if keywords is None:
        keywords = ["EVA & GUARANI", "BIOS-Q", "Quantum", "EGOS"]

    context = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": "",
        "key_points": [],
        "related_files": [],
    }

    # Extract code blocks that might contain file references
    code_blocks = re.findall(r"```(?:\w+)?\s*\n(.*?)\n```", text, re.DOTALL)

    # Find file references
    file_pattern = re.compile(r"[\w/\-\.]+\.(py|md|js|html|css|json|yaml|yml)")
    for block in code_blocks:
        matches = file_pattern.findall(block)
        for match in matches:
            if os.path.exists(os.path.join(PROJECT_ROOT, match)):
                context["related_files"].append(match)

    # Extract key points (sentences containing keywords)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sentence in sentences:
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            context["key_points"].append(sentence.strip())

    # Generate simple summary
    if context["key_points"]:
        context["summary"] = (
            f"Conversation contains {len(context['key_points'])} key points related to {', '.join(keywords)}"
        )
    else:
        context["summary"] = "No significant context found in this conversation"

    return context


def load_conversation_context_for_bios_q():
    """
    Load and format conversation context for BIOS-Q integration

    Returns:
        str: Formatted context for BIOS-Q
    """
    conversations = load_past_conversations(limit=3)
    if not conversations:
        return "No previous conversation context available."

    context_text = "### Previous Conversation Context\n\n"

    for i, conv in enumerate(conversations):
        metadata = conv.get("metadata", {})
        summary = metadata.get("summary", "No summary available.")
        timestamp = metadata.get("timestamp", "")

        if timestamp:
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

        context_text += f"**Conversation {i+1}** ({timestamp}):\n"
        context_text += f"- Summary: {summary}\n"

        key_points = metadata.get("key_points", [])
        if key_points:
            context_text += "- Key points:\n"
            for point in key_points[:3]:  # Limit to first 3 points
                context_text += f"  - {point}\n"

        context_text += "\n"

    return context_text


# ========================================================================
# FORMATTING UTILITY FUNCTIONS
# ========================================================================


def format_timestamp(timestamp=None, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Returns a formatted timestamp string

    Args:
        timestamp: Optional datetime or isoformat string
        format_str: Format string for the output

    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        dt = datetime.datetime.now()
    elif isinstance(timestamp, str):
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
        except ValueError:
            dt = datetime.datetime.now()
    else:
        dt = timestamp

    return dt.strftime(format_str)


def format_quantum_log_entry(message, level="INFO", source=None):
    """
    Creates a formatted log entry with quantum signature

    Args:
        message: The log message
        level: Log level
        source: Source module

    Returns:
        str: Formatted log entry
    """
    timestamp = format_timestamp()
    source_info = f" [{source}]" if source else ""

    return f"[{timestamp}] [{level}]{source_info} {message}"


# ========================================================================
# TRIGGER FUNCTIONS FOR CONVERSATION CONTEXT
# ========================================================================


def trigger_context_preservation(text, source="automatic"):
    """
    Trigger function to preserve conversation context

    This can be called automatically or manually to save the current
    conversation and make it available to BIOS-Q.

    Args:
        text: The conversation text
        source: Source of the trigger (automatic, manual, etc.)

    Returns:
        bool: Success status
    """
    print(f"\n🔄 Context preservation triggered ({source})...")
    success, path = preserve_conversation(text, source_name=source)

    if success:
        print(f"✅ Context preserved successfully")
        print(f"📂 Available for BIOS-Q integration")

    return success


def trigger_context_loading():
    """
    Trigger function to load conversation context

    This can be called at the beginning of a new conversation
    to load previous context.

    Returns:
        str: Formatted context
    """
    print("\n🔄 Loading conversation context...")
    context = load_conversation_context_for_bios_q()
    print(f"✅ Loaded context from {len(load_past_conversations())} previous conversations")

    return context


# ========================================================================
# MAIN FUNCTION FOR TESTING
# ========================================================================


def test_conversation_preservation():
    """Test the conversation preservation functionality"""
    print("\n✧༺❀༻∞ EVA & GUARANI - Testing Conversation Preservation ∞༺❀༻✧\n")

    test_conversation = """
    Human: How can I export conversations from Cursor?

    Assistant: You can use the new conversation_exporter.py tool:

    ```python
    from tools.conversation_exporter import export_conversation

    # Export directly from clipboard
    export_conversation()

    # Or from a text string
    text = "Your conversation here"
    export_conversation(clipboard_text=text)
    ```

    Human: Will this integrate with BIOS-Q?

    Assistant: Yes, it can be integrated with BIOS-Q for context preservation.
    """

    # Set up language for testing
    current_language = get_system_language()
    print(f"Current system language: {current_language}")

    # Test language detection
    detected_language = detect_language(test_conversation)
    print(f"Detected conversation language: {detected_language}")

    # Test context preservation
    success, output_path = preserve_conversation(
        test_conversation, source_name="test", metadata={"test": True}
    )

    if success:
        print("\n✅ Conversation preservation test completed successfully")

        # Test context loading
        context = trigger_context_loading()
        print("\nLoaded Context Sample:")
        print(context[:200] + "..." if len(context) > 200 else context)
    else:
        print("\n⚠️ Conversation preservation test failed")

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")


if __name__ == "__main__":
    test_conversation_preservation()
