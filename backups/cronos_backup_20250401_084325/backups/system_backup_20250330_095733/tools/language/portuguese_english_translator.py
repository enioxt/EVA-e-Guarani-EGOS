#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Portuguese to English Translator

This utility helps convert Portuguese content to English throughout the system.
It can translate file content, directory names, and provide batch processing for
large-scale translation tasks.
"""

import os
import re
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, Tuple
import shutil
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [TRANSLATOR] %(message)s",
    handlers=[logging.FileHandler("translator.log"), logging.StreamHandler()],
)

logger = logging.getLogger("TRANSLATOR")

# Dictionary of common Portuguese terms in the codebase and their English equivalents
TRANSLATION_DICTIONARY = {
    # System components
    "atualizacao": "update",
    "inicializacao": "initialization",
    "configuracao": "configuration",
    "traducao": "translation",
    "apresentacao": "presentation",
    "integracao": "integration",
    "validacao": "validation",
    "preservacao": "preservation",
    "conversao": "conversion",
    "arquivo": "file",
    "pasta": "folder",
    "diretorio": "directory",
    # File/folder names
    "Eva e Guarani changelogs": "Eva and Guarani changelogs",
    "conversa anterior": "previous conversation",
    "A FAZER": "TODO",
    "apresentaçao e concorrentes": "presentation and competitors",
    "atualizacao bot unificado": "unified bot update",
    "atualização botava": "bot update",
    "BACKUP quantico": "quantum BACKUP",
    "Benchmark do Sistema": "System Benchmark",
    "Como usar e atualizacao": "How to use and update",
    "Integraçao Cursor e Eva": "Cursor and Eva Integration",
    "Integraçao Eliza": "Eliza Integration",
    "Integraçao sistema quantico": "Quantum system integration",
    "MATRIZ quantica": "Quantum MATRIX",
    "próximos passo": "next steps",
    "Reorganizaçao do sistema": "System reorganization",
    "sistema validaçao etica": "ethical validation system",
    "viagem neural quantica": "quantum neural journey",
    # Common phrases
    "versão": "version",
    "sistema": "system",
    "quantum": "quantum",
    "próximos passos": "next steps",
    "concorrentes": "competitors",
    # Technical terms
    "aprendizado de máquina": "machine learning",
    "inteligência artificial": "artificial intelligence",
    "processamento de linguagem natural": "natural language processing",
    "rede neural": "neural network",
    "aprendizado profundo": "deep learning",
    "visão computacional": "computer vision",
    "ciência de dados": "data science",
    "base de dados": "database",
    "análise de dados": "data analysis",
    "mineração de dados": "data mining",
    "algoritmo": "algorithm",
    "programação orientada a objetos": "object-oriented programming",
    "interface de usuário": "user interface",
    "experiência do usuário": "user experience",
    "desenvolvimento web": "web development",
    "desenvolvimento de software": "software development",
    "arquitetura de software": "software architecture",
    "engenharia de software": "software engineering",
    "controle de versão": "version control",
    "código-fonte": "source code",
    "depuração": "debugging",
    "otimização": "optimization",
    "implantação": "deployment",
    # ATLAS-specific terms
    "cartografia sistêmica": "systemic cartography",
    "mapeamento de conexões": "connection mapping",
    "visualização de sistemas": "system visualization",
    "análise topológica": "topological analysis",
    "identificação de padrões": "pattern identification",
    # NEXUS-specific terms
    "análise modular": "modular analysis",
    "avaliação de componentes": "component evaluation",
    "coesão": "cohesion",
    "acoplamento": "coupling",
    "otimização de sistemas": "system optimization",
    # CRONOS-specific terms
    "preservação evolutiva": "evolutionary preservation",
    "persistência de contexto": "context persistence",
    "gerenciamento de backup": "backup management",
    "continuidade de estado": "state continuity",
    "rastreamento de versão": "version tracking",
    # ETHIK-specific terms
    "estrutura ética": "ethical framework",
    "orientação ética": "ethical guidance",
    "avaliação ética": "ethical evaluation",
    "princípios universais": "universal principles",
    "assinatura ética": "ethical signature",
    # BIOS-Q-specific terms
    "gerenciamento de contexto": "context management",
    "preservação de estado": "state preservation",
    "base lógica de firmware": "logical firmware foundation",
    "carregador de inicialização": "bootloader",
    "sequência de inicialização": "boot sequence",
    # Philosophical terms
    "amor incondicional": "unconditional love",
    "possibilidade universal de redenção": "universal possibility of redemption",
    "temporalidade compassiva": "compassionate temporality",
    "privacidade sagrada": "sacred privacy",
    "acessibilidade universal": "universal accessibility",
    "confiança recíproca": "reciprocal trust",
    "ética integrada": "integrated ethics",
    "modularidade consciente": "conscious modularity",
    "cartografia sistêmica": "systemic cartography",
    "preservação evolutiva": "evolutionary preservation",
    "harmonia multiplataforma": "cross-platform harmony",
    # Grammar structures
    "é necessário": "it is necessary",
    "é importante": "it is important",
    "é preciso": "it is required",
    "deve-se": "one should",
    "pode-se": "one can",
}

# Load translation memory if exists
TRANSLATION_MEMORY_FILE = "tools/language/translation_memory.json"
translation_memory = {}

if os.path.exists(TRANSLATION_MEMORY_FILE):
    try:
        with open(TRANSLATION_MEMORY_FILE, "r", encoding="utf-8") as f:
            translation_memory = json.load(f)
    except Exception as e:
        logger.warning(f"Could not load translation memory: {e}")
        translation_memory = {}

# Context-aware translation configuration
CONTEXT_PATTERNS = {
    # Python file context
    r"\.py$": {
        "code_blocks": [
            (r"def ([a-zA-Z0-9_]+)\(([^)]*)\):", "function"),
            (r"class ([a-zA-Z0-9_]+)(\([^)]*\))?:", "class"),
            (r"# (.*)", "comment"),
            (r'"""(.*?)"""', "docstring", re.DOTALL),
            (r"'''(.*?)'''", "docstring", re.DOTALL),
        ],
        "preserve": [r"import .*", r"from .* import .*", r"@.*", r'if __name__ == "__main__":'],
        "technical_terms": True,
    },
    # Markdown file context
    r"\.md$": {
        "code_blocks": [
            (r"```[a-z]*\n(.*?)\n```", "code_block", re.DOTALL),
            (r"`(.*?)`", "inline_code"),
            (r"#{1,6} (.*)", "heading"),
        ],
        "preserve": [
            r"!\[.*?\]\(.*?\)",
            r"\[.*?\]\(.*?\)",
            r"<.*?>",
        ],
        "technical_terms": True,
    },
    # JSON file context
    r"\.json$": {
        "preserve": [
            r'"[^"]*"\s*:',
            r"\{",
            r"\}",
            r"\[",
            r"\]",
        ],
        "technical_terms": False,
    },
}


def get_file_context(file_path: str) -> dict:
    """Determine the context (file type, etc.) for more accurate translation."""
    context = {"file_type": "unknown", "patterns": None}

    for pattern, config in CONTEXT_PATTERNS.items():
        if re.search(pattern, file_path, re.IGNORECASE):
            file_type = pattern.replace("\\", "").replace("$", "").replace(".", "")
            context["file_type"] = file_type
            context["patterns"] = config
            break

    return context


def translate_text(text: str, context: dict = None) -> str:
    """
    Translate Portuguese text to English with context awareness.

    Args:
        text: The text to translate
        context: Optional context information for better translation

    Returns:
        Translated text
    """
    if not text:
        return text

    # Check translation memory first
    if text in translation_memory:
        return translation_memory[text]

    # Check if we should preserve this text based on context
    if context and context["patterns"] and "preserve" in context["patterns"]:
        for pattern in context["patterns"]["preserve"]:
            if re.match(pattern, text):
                return text

    # Handle code blocks if in context
    if context and context["patterns"] and "code_blocks" in context["patterns"]:
        for pattern, block_type, *flags in context["patterns"]["code_blocks"]:
            flag = flags[0] if flags else 0
            match = re.match(pattern, text, flag)
            if match:
                if block_type == "function" or block_type == "class":
                    # Preserve function/class definitions but translate comments
                    return text
                elif block_type == "code_block":
                    # Preserve code within markdown code blocks
                    return text

    # Apply dictionary replacement for exact matches
    if text in TRANSLATION_DICTIONARY:
        translated = TRANSLATION_DICTIONARY[text]
        translation_memory[text] = translated
        return translated

    # Apply pattern-based translation for complex structures
    translated = text
    for pt, en in TRANSLATION_DICTIONARY.items():
        # Use word boundary markers to avoid partial replacements
        pattern = r"\b" + re.escape(pt) + r"\b"
        translated = re.sub(pattern, en, translated, flags=re.IGNORECASE)

    # Store in translation memory if different from original
    if translated != text:
        translation_memory[text] = translated

    return translated


def translate_file_content(file_path: str, dry_run: bool = False) -> Tuple[bool, str, str]:
    """
    Translate the content of a file from Portuguese to English with context awareness.

    Args:
        file_path: Path to the file to translate
        dry_run: If True, don't actually write changes

    Returns:
        Tuple of (success, original_content, translated_content)
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if not content.strip():
            return True, content, content

        context = get_file_context(file_path)

        # Process line by line for most file types
        lines = content.split("\n")
        translated_lines = []

        for line in lines:
            translated_line = translate_text(line, context)
            translated_lines.append(translated_line)

        translated_content = "\n".join(translated_lines)

        if not dry_run and translated_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            logger.info(f"Translated file: {file_path}")

        return True, content, translated_content
    except Exception as e:
        logger.error(f"Error translating file {file_path}: {e}")
        return False, "", ""


def process_file(args):
    """Process a single file for parallel execution."""
    file_path, dry_run = args
    return translate_file_content(file_path, dry_run)


def translate_directory(
    directory: str,
    extensions: List[str] = None,
    rename_files: bool = False,
    rename_dirs: bool = False,
    dry_run: bool = False,
    max_workers: int = None,
) -> Dict[str, Any]:
    """
    Recursively translate all files in a directory from Portuguese to English.

    Args:
        directory: Directory to translate
        extensions: List of file extensions to translate (e.g. ['.py', '.md'])
        rename_files: If True, rename files from Portuguese to English
        rename_dirs: If True, rename directories from Portuguese to English
        dry_run: If True, don't actually make changes
        max_workers: Maximum number of parallel workers (defaults to CPU count)

    Returns:
        Dictionary with stats about the translation
    """
    if not os.path.exists(directory):
        logger.error(f"Directory not found: {directory}")
        return {
            "success": False,
            "files_processed": 0,
            "files_translated": 0,
            "files_renamed": 0,
            "dirs_renamed": 0,
            "errors": [f"Directory not found: {directory}"],
        }

    stats = {
        "success": True,
        "files_processed": 0,
        "files_translated": 0,
        "files_renamed": 0,
        "dirs_renamed": 0,
        "errors": [],
    }

    # Get list of all files to process
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue

            file_path = os.path.join(root, file)
            all_files.append((file_path, dry_run))

    # Determine number of workers
    if max_workers is None:
        max_workers = max(1, multiprocessing.cpu_count() - 1)

    # Process files in parallel
    translated_files = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, args): args[0] for args in all_files}

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                success, original, translated = future.result()
                stats["files_processed"] += 1

                if success and original != translated:
                    stats["files_translated"] += 1
                    translated_files += 1

            except Exception as e:
                stats["errors"].append(f"Error processing {file_path}: {e}")
                logger.error(f"Error processing {file_path}: {e}")

    # Handle directory and file renaming - we do this sequentially as it can cause conflicts
    if rename_dirs:
        # Start from deepest directories to avoid path conflicts
        all_dirs = []
        for root, dirs, _ in os.walk(directory):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                all_dirs.append(dir_path)

        # Sort by depth (deepest first)
        all_dirs.sort(key=lambda x: x.count(os.sep), reverse=True)

        for dir_path in all_dirs:
            dir_name = os.path.basename(dir_path)
            parent_dir = os.path.dirname(dir_path)
            translated_name = translate_text(dir_name)

            if translated_name != dir_name:
                new_dir_path = os.path.join(parent_dir, translated_name)

                if not dry_run:
                    try:
                        # Check if destination already exists
                        if os.path.exists(new_dir_path):
                            logger.warning(
                                f"Cannot rename directory {dir_path} to {new_dir_path} - destination exists"
                            )
                            stats["errors"].append(
                                f"Rename conflict: {new_dir_path} already exists"
                            )
                            continue

                        os.rename(dir_path, new_dir_path)
                        stats["dirs_renamed"] += 1
                        logger.info(f"Renamed directory: {dir_path} -> {new_dir_path}")
                    except Exception as e:
                        stats["errors"].append(f"Error renaming directory {dir_path}: {e}")
                        logger.error(f"Error renaming directory {dir_path}: {e}")
                else:
                    logger.info(f"[DRY RUN] Would rename directory: {dir_path} -> {new_dir_path}")
                    stats["dirs_renamed"] += 1

    if rename_files:
        for root, _, files in os.walk(directory):
            for file_name in files:
                if extensions and not any(file_name.endswith(ext) for ext in extensions):
                    continue

                file_path = os.path.join(root, file_name)
                file_base, file_ext = os.path.splitext(file_name)
                translated_base = translate_text(file_base)

                if translated_base != file_base:
                    new_file_name = translated_base + file_ext
                    new_file_path = os.path.join(root, new_file_name)

                    if not dry_run:
                        try:
                            # Check if destination already exists
                            if os.path.exists(new_file_path):
                                logger.warning(
                                    f"Cannot rename file {file_path} to {new_file_path} - destination exists"
                                )
                                stats["errors"].append(
                                    f"Rename conflict: {new_file_path} already exists"
                                )
                                continue

                            os.rename(file_path, new_file_path)
                            stats["files_renamed"] += 1
                            logger.info(f"Renamed file: {file_path} -> {new_file_path}")
                        except Exception as e:
                            stats["errors"].append(f"Error renaming file {file_path}: {e}")
                            logger.error(f"Error renaming file {file_path}: {e}")
                    else:
                        logger.info(f"[DRY RUN] Would rename file: {file_path} -> {new_file_path}")
                        stats["files_renamed"] += 1

    # Save updated translation memory
    if translated_files > 0 and not dry_run:
        try:
            os.makedirs(os.path.dirname(TRANSLATION_MEMORY_FILE), exist_ok=True)
            with open(TRANSLATION_MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(translation_memory, f, ensure_ascii=False, indent=2)
            logger.info(f"Updated translation memory with {len(translation_memory)} entries")
        except Exception as e:
            logger.error(f"Error saving translation memory: {e}")
            stats["errors"].append(f"Error saving translation memory: {e}")

    return stats


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="EVA & GUARANI EGOS - Portuguese to English Translator"
    )
    parser.add_argument("--base-path", help="Base path for the EVA & GUARANI EGOS system")
    parser.add_argument("--file", help="Path to a specific file to translate")
    parser.add_argument("--dir", help="Path to a directory to translate all files")
    parser.add_argument(
        "--rename-files", action="store_true", help="Rename files from Portuguese to English"
    )
    parser.add_argument(
        "--rename-dirs", action="store_true", help="Rename directories from Portuguese to English"
    )
    parser.add_argument(
        "--extensions",
        help="Comma-separated list of file extensions to translate (default: .md,.txt,.py,.js,.json)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate translation without making changes"
    )

    args = parser.parse_args()

    # Initialize the translator
    translator = PortugueseEnglishTranslator(args.base_path, args.dry_run)

    if args.file:
        # Translate a single file
        translator.translate_file_content(args.file)

    if args.dir:
        # Translate all files in a directory
        extensions = args.extensions.split(",") if args.extensions else None
        translator.translate_directory_contents(args.dir, extensions)

    if args.rename_files:
        # Rename files from Portuguese to English
        if args.file:
            translator.translate_file_name(args.file)
        elif args.dir:
            for file_path in Path(args.dir).glob("**/*"):
                if file_path.is_file():
                    translator.translate_file_name(file_path)

    if args.rename_dirs:
        # Rename directories from Portuguese to English
        if args.dir:
            translator.translate_directory_names(args.dir)

    # Save the translation memory
    translator.save_translation_memory()

    logger.info("Translation process completed")
    return 0


if __name__ == "__main__":
    main()
