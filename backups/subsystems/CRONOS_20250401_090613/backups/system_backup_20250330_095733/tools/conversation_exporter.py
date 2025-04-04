#!/usr/bin/env python3
"""
# ========================================================================
# CONVERSATION EXPORTER - Content Export Tool for EVA & GUARANI
# ========================================================================
#
# This tool helps extract and save conversation history from Cursor or
# other sources to ensure no information is lost during development.
#
# Features:
# 1. Export current conversation to a text file
# 2. Format conversations with timestamps and roles
# 3. Save in both plain text and markdown formats
#
# ========================================================================
"""

import os
import sys
import argparse
import datetime
import json
import re
from pathlib import Path

# Try to import pyperclip for clipboard functionality, but make it optional
try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Note: pyperclip not available, clipboard functionality will be disabled.")

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ========================================================================
# CONFIGURATION
# ========================================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS_DIR = os.path.join(PROJECT_ROOT, "logs", "conversations")
DEFAULT_FILENAME = f"cursor_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================


def ensure_export_directory():
    """Create export directory if it doesn't exist"""
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    return EXPORTS_DIR


def clean_text(text):
    """Clean up text for saving"""
    # Remove any special control characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)
    return text


def parse_conversation_from_clipboard():
    """Parse conversation text from clipboard"""
    if not CLIPBOARD_AVAILABLE:
        print("⚠️ Clipboard functionality not available. Please install pyperclip.")
        return None

    try:
        text = pyperclip.paste()
        if not text:
            print("⚠️ Clipboard is empty. Please copy conversation text first.")
            return None

        print(f"✅ Retrieved {len(text)} characters from clipboard")
        return text
    except Exception as e:
        print(f"⚠️ Error accessing clipboard: {str(e)}")
        return None


def extract_conversation_structure(text):
    """Try to extract conversation structure (roles and messages)"""
    # Simple heuristic: look for patterns like "Human:" and "Assistant:"
    # This is a simplistic approach and may need refinement
    messages = []

    # Try to identify message patterns
    human_pattern = re.compile(r"(?:Human|User):(.*?)(?=(?:Assistant|Human|User):|$)", re.DOTALL)
    assistant_pattern = re.compile(r"Assistant:(.*?)(?=(?:Human|User|Assistant):|$)", re.DOTALL)

    # Extract human messages
    for match in human_pattern.finditer(text):
        content = match.group(1).strip()
        if content:
            messages.append(
                {
                    "role": "human",
                    "content": content,
                    "timestamp": datetime.datetime.now().isoformat(),  # Approximate
                }
            )

    # Extract assistant messages
    for match in assistant_pattern.finditer(text):
        content = match.group(1).strip()
        if content:
            messages.append(
                {
                    "role": "assistant",
                    "content": content,
                    "timestamp": datetime.datetime.now().isoformat(),  # Approximate
                }
            )

    # If we couldn't extract structured messages, treat as a single blob
    if not messages:
        messages.append(
            {"role": "unknown", "content": text, "timestamp": datetime.datetime.now().isoformat()}
        )

    return messages


def format_as_markdown(messages):
    """Format conversation as Markdown"""
    md_content = "# Cursor Conversation Export\n\n"
    md_content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md_content += "---\n\n"

    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        timestamp = msg.get("timestamp", "")

        if timestamp:
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

        md_content += f"## {role}"
        if timestamp:
            md_content += f" ({timestamp})"
        md_content += "\n\n"

        # Format code blocks properly
        content = re.sub(r"```(.*?)```", r"```\1```", content, flags=re.DOTALL)

        md_content += f"{content}\n\n"

    md_content += "---\n\n"
    md_content += "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n"

    return md_content


def format_as_plain_text(messages):
    """Format conversation as plain text"""
    text_content = "CURSOR CONVERSATION EXPORT\n"
    text_content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    text_content += "=" * 50 + "\n\n"

    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        timestamp = msg.get("timestamp", "")

        if timestamp:
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

        text_content += f"[{role}]"
        if timestamp:
            text_content += f" ({timestamp})"
        text_content += "\n"

        # Indent content
        content_lines = content.split("\n")
        indented_content = "\n".join(f"  {line}" for line in content_lines)
        text_content += f"{indented_content}\n\n"

    text_content += "=" * 50 + "\n"
    text_content += "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n"

    return text_content


def save_conversation(messages, output_path=None, format_type="both"):
    """Save conversation to file"""
    if not output_path:
        output_path = os.path.join(ensure_export_directory(), DEFAULT_FILENAME)

    # Make sure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if format_type in ["markdown", "both"]:
        md_content = format_as_markdown(messages)
        md_path = output_path if output_path.endswith(".md") else f"{output_path}.md"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ Markdown conversation saved to: {md_path}")

    if format_type in ["text", "both"]:
        text_content = format_as_plain_text(messages)
        text_path = (
            output_path.replace(".md", ".txt")
            if output_path.endswith(".md")
            else f"{output_path}.txt"
        )

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(f"✅ Plain text conversation saved to: {text_path}")

    return True


# ========================================================================
# MAIN EXPORT FUNCTION
# ========================================================================


def export_conversation(clipboard_text=None, output_path=None, format_type="both"):
    """Export conversation to file"""
    print("\n✧༺❀༻∞ EVA & GUARANI - Conversation Exporter ∞༺❀༻✧\n")

    # Get conversation text
    if not clipboard_text:
        print("📋 Reading from clipboard...")
        clipboard_text = parse_conversation_from_clipboard()

        if not clipboard_text and not CLIPBOARD_AVAILABLE:
            print("💡 Clipboard functionality not available. Please provide text via file input.")
            print("   Example: python conversation_exporter.py -i input_file.txt")

    if not clipboard_text:
        print("⚠️ No conversation text provided. Exiting.")
        return False

    # Clean and parse conversation
    print("🔄 Processing conversation structure...")
    cleaned_text = clean_text(clipboard_text)
    messages = extract_conversation_structure(cleaned_text)

    if not messages:
        print("⚠️ Failed to extract conversation structure.")
        print("💡 Treating entire text as a single message.")
        messages = [
            {
                "role": "unknown",
                "content": cleaned_text,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        ]

    # Save conversation
    print(f"💾 Saving conversation with {len(messages)} messages...")
    success = save_conversation(messages, output_path, format_type)

    if success:
        print("\n✅ Conversation exported successfully!")
        print(f"📂 Files saved to: {ensure_export_directory()}")
    else:
        print("\n⚠️ Failed to export conversation.")

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
    return success


# ========================================================================
# COMMAND LINE INTERFACE
# ========================================================================


def main():
    """Command line interface for the conversation exporter"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI Conversation Exporter")
    parser.add_argument("-o", "--output", help="Output file path", default=None)
    parser.add_argument(
        "-f",
        "--format",
        choices=["markdown", "text", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument("-i", "--input", help="Input file (instead of clipboard)", default=None)
    parser.add_argument("-t", "--text", help="Text to process directly", default=None)

    args = parser.parse_args()

    # Get text from input sources (priority: direct text > input file > clipboard)
    text = None

    # 1. Check for direct text input
    if args.text:
        text = args.text
        print("📝 Using provided text parameter")

    # 2. Check for input file
    elif args.input and os.path.exists(args.input):
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"📄 Read input from file: {args.input}")
        except Exception as e:
            print(f"⚠️ Error reading input file: {str(e)}")

    # 3. Clipboard will be tried in the export_conversation function if text is still None

    # Export the conversation
    export_conversation(clipboard_text=text, output_path=args.output, format_type=args.format)


if __name__ == "__main__":
    main()
