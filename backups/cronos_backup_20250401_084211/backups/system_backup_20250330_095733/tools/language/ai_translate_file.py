#!/usr/bin/env python3
# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: 2025-03-22 08:37:43
# Combined files:
# - tools\language\ai_translate_file.py (kept)
# - sandbox\tools\ai_translate_file.py (moved to quarantine)
# ==================================================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - AI-Assisted File Translation Tool
This script uses OpenAI API to translate files from Portuguese to English.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    import openai
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ai_translation_log.txt", encoding="utf-8"),
    ],
)
logger = logging.getLogger("ai_translate_file")


class AITranslator:
    """AI-assisted translator for converting files from Portuguese to English"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the AI translator

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: OpenAI model to use for translation
        """
        # Default API key from project configuration
        default_api_key = "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"

        # Priority: 1. Explicit API key parameter, 2. Environment variable, 3. Default project key
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or default_api_key
        self.model = model
        self.client = None

        if not self.api_key:
            logger.warning(
                "No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass with --api-key"
            )

        self._init_client()

    def _init_client(self) -> None:
        """Initialize OpenAI client if available"""
        if not OPENAI_AVAILABLE:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            return

        if not self.api_key:
            logger.error("OpenAI API key not provided")
            return

        try:
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"OpenAI client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            self.client = None

    def translate_file(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        backup: bool = True,
        dry_run: bool = False,
    ) -> Optional[Path]:
        """
        Translate a file from Portuguese to English

        Args:
            input_path: Path to input file
            output_path: Path to output file (if None, will replace or append to original)
            backup: Whether to create a backup of the original file
            dry_run: If True, don't actually change the file

        Returns:
            Path to output file, or None if translation failed
        """
        # Check if file exists
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            return None

        # Default output path is the same as input (replace)
        if not output_path:
            output_path = input_path

        # Read input file
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading input file: {str(e)}")
            return None

        # Create backup if needed
        if backup and not dry_run and output_path == input_path:
            backup_path = input_path.with_suffix(input_path.suffix + ".backup")
            try:
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"Backup created: {backup_path}")
            except Exception as e:
                logger.error(f"Error creating backup: {str(e)}")
                return None

        # For dry runs, just simulate the process and return the output path
        if dry_run:
            logger.info(f"Dry run - not making any changes")
            logger.info(f"Would translate file {input_path} to {output_path}")
            return output_path

        # Check if OpenAI client is available for actual translation
        if not OPENAI_AVAILABLE or not self.client:
            logger.error("OpenAI client not available. Cannot perform translation.")
            return None

        # Get file type
        file_ext = input_path.suffix.lower()

        # Construct prompt based on file type
        file_type_desc = ""
        if file_ext == ".py":
            file_type_desc = "Python code"
        elif file_ext == ".md":
            file_type_desc = "Markdown documentation"
        elif file_ext == ".js":
            file_type_desc = "JavaScript code"
        elif file_ext == ".html":
            file_type_desc = "HTML"
        elif file_ext == ".css":
            file_type_desc = "CSS"
        elif file_ext in [".json", ".yaml", ".yml"]:
            file_type_desc = f"{file_ext[1:].upper()} configuration"
        else:
            file_type_desc = "text"

        prompt = f"""Translate the following {file_type_desc} from Portuguese to English.
Maintain the exact same structure, formatting, indentation and code functionality.
Translate only the text, comments, documentation strings, and variable/function/class names if they're in Portuguese.
DO NOT change any code logic, imports, or functionality.
Keep all symbols, punctuation, and code structure intact.
For variable/function/class names, use English equivalents that maintain the same meaning.

Here is the content to translate:

```
{content}
```"""

        logger.info(f"Translating file: {input_path}")

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator specializing in Portuguese to English technical translation, maintaining code integrity and functionality.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=4000,
            )

            # Extract translated content
            translated_content = response.choices[0].message.content

            # Remove markdown code block markers if present
            translated_content = translated_content.replace("```", "").strip()
            if file_ext in [".py", ".js", ".html", ".css"]:
                # Remove language identifier if present at the beginning
                translated_content = translated_content.replace(file_ext[1:] + "\n", "", 1)

            # Write output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(translated_content)

            logger.info(f"Translation complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            return None


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI AI-Assisted File Translation Tool")

    # Support both positional and --file argument for better script integration
    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument("--file", type=str, help="Input file to translate")
    file_group.add_argument("input_file", nargs="?", type=str, help="Input file to translate")

    parser.add_argument(
        "--output", type=str, help="Output file (if not specified, will replace original)"
    )
    parser.add_argument("--api-key", type=str, help="OpenAI API key")
    parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model to use")
    parser.add_argument(
        "--no-backup", action="store_true", help="Don't create a backup of the original file"
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't actually translate the file")

    args = parser.parse_args()

    # Initialize translator
    translator = AITranslator(api_key=args.api_key, model=args.model)

    # Get input file path (either from positional arg or --file)
    input_file = args.input_file or args.file

    # Get input and output paths
    input_path = Path(input_file).resolve()
    output_path = input_path
    if args.output:
        output_path = Path(args.output).resolve()

    # Translate file
    result = translator.translate_file(
        input_path=input_path,
        output_path=output_path,
        backup=not args.no_backup,
        dry_run=args.dry_run,
    )

    # Report results
    if result:
        print(f"\nTranslation successful!")
        print(f"Translated file: {result}")

        # If we created a backup, check if it exists and report
        backup_file = None
        if not args.no_backup and input_path == output_path:
            backup_file = input_path.with_suffix(input_path.suffix + ".backup")
            if backup_file and backup_file.exists():
                print(f"Backup created: {backup_file}")
        return 0
    else:
        print("\nTranslation failed. Check the logs for more information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
