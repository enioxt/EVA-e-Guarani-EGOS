#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Portuguese to English File Translator

This script provides comprehensive translation of Portuguese files to English
throughout the system. It can handle files, directory names, and supports batch
processing with detailed logging.

Usage:
    python translate_portuguese_files.py [options]

Options:
    --directory/-d: Directory to process (default: current project root)
    --extensions/-e: File extensions to process (default: .txt,.md,.py,.js,.json)
    --dry-run: Simulate without making changes
    --rename-files: Rename files with Portuguese names
    --rename-dirs: Rename directories with Portuguese names
    --verbose: Show detailed logs
    --report: Generate detailed report
"""

import os
import sys
import re
import json
import argparse
import logging
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set, Optional
import difflib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("translation.log"), logging.StreamHandler()],
)

logger = logging.getLogger("TRANSLATOR")

# Enhanced Portuguese-English dictionary
TRANSLATION_DICTIONARY = {
    # System components and concepts
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
    "sistema": "system",
    "versao": "version",
    "próximos passos": "next steps",
    "concorrentes": "competitors",
    "plano de negocio": "business plan",
    "matriz": "matrix",
    "reorganizacao": "reorganization",
    "evolucao": "evolution",
    "consciencia": "consciousness",
    "etica": "ethics",
    "quantico": "quantum",
    "desenvolvimento": "development",
    "implementacao": "implementation",
    "memória": "memory",
    "aplicacao": "application",
    "automacao": "automation",
    "seguranca": "security",
    "analise": "analysis",
    "execucao": "execution",
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
    "Reorganizaçao do sistem": "System reorganization",
    "sistema validaçao etica": "ethical validation system",
    "viagem neural quantica": "quantum neural journey",
    "PLANO DE NEGOCIO EVA": "EVA BUSINESS PLAN",
    "BIOS-Q Cursor sistema EVA": "BIOS-Q Cursor EVA system",
    # Business terms
    "atendimento": "service",
    "vendas": "sales",
    "educação": "education",
    "saúde": "health",
    "gestão": "management",
    "preço": "price",
    "cliente": "client",
    "usuário": "user",
    "gratuito": "free",
    "pagamento": "payment",
    "receita": "revenue",
    "custo": "cost",
    "investimento": "investment",
    "retorno": "return",
    "mercado": "market",
    "pesquisa": "research",
    "desenvolvimento": "development",
    "estratégia": "strategy",
    "implementação": "implementation",
    "lançamento": "launch",
    "mensalidade": "monthly fee",
    "assinatura": "subscription",
    # Technical terms
    "banco de dados": "database",
    "conexão": "connection",
    "integração": "integration",
    "API": "API",
    "servidor": "server",
    "aplicativo": "application",
    "móvel": "mobile",
    "desktop": "desktop",
    "frontend": "frontend",
    "backend": "backend",
    "código": "code",
    "desenvolvimento": "development",
    "teste": "test",
    "depuração": "debugging",
    "implementação": "implementation",
    "lançamento": "release",
    "versão": "version",
    "atualização": "update",
    "backup": "backup",
    "restauração": "restoration",
    "configuração": "configuration",
    "instalação": "installation",
}


class PortugueseDetector:
    """Detects Portuguese content in files and text"""

    def __init__(self):
        self.portuguese_patterns = [
            r"\bção\b",
            r"\bções\b",
            r"\bção\s",
            r"\bções\s",
            r"\bcao\b",
            r"\bcao\s",
            r"\bcoes\b",
            r"\bcoes\s",
            r"\baçao\b",
            r"\baçao\s",
            r"\baçoes\b",
            r"\baçoes\s",
            r"\bçao\b",
            r"\bçao\s",
            r"\bçoes\b",
            r"\bçoes\s",
            r"\bde\s+a\b",
            r"\bda\b",
            r"\bdo\b",
            r"\bdos\b",
            r"\bdas\b",
            r"\bpara\s+o\b",
            r"\bpara\s+a\b",
            r"\bpara\s+os\b",
            r"\bpara\s+as\b",
            r"\bcomo\s+usar\b",
            r"\bcomo\s+fazer\b",
            r"\bcomo\s+implementar\b",
            r"\bpróximo\b",
            r"\bpróxima\b",
            r"\bpróximos\b",
            r"\bpróximas\b",
            r"\bfunção\b",
            r"\bfunções\b",
            r"\baplicação\b",
            r"\baplicações\b",
            r"\bpadrão\b",
            r"\bpadrões\b",
            r"\bautomatização\b",
            r"\bintegração\b",
            r"\bimplementação\b",
            r"\bmanutenção\b",
            r"\batualização\b",
            r"\bcódigo\b",
            r"\btradução\b",
            r"\banotação\b",
            r"\bvariável\b",
            r"\bconfigurações\b",
            r"\butilizando\b",
            r"\bprocessamento\b",
            r"\bcomunicação\b",
            r"\bsistemas\b",
            r"\bestrutura\b",
            # Portuguese-specific words with accents
            r"\bé\b",
            r"\bestá\b",
            r"\bestão\b",
            r"\bnão\b",
            r"\bmás\b",
            r"\bportuguês\b",
            r"\binglês\b",
        ]
        self.portuguese_words = {
            "não",
            "sim",
            "como",
            "porque",
            "quando",
            "onde",
            "quem",
            "qual",
            "quais",
            "para",
            "por",
            "pelo",
            "pela",
            "pelos",
            "pelas",
            "com",
            "sem",
            "entre",
            "sobre",
            "sob",
            "desde",
            "até",
            "durante",
            "após",
            "antes",
            "mas",
            "porém",
            "contudo",
            "todavia",
            "entretanto",
            "então",
            "portanto",
            "assim",
            "embora",
            "apesar",
            "conforme",
            "segundo",
            "consoante",
            "este",
            "esta",
            "estes",
            "estas",
            "esse",
            "essa",
            "esses",
            "essas",
            "isto",
            "isso",
            "aquele",
            "aquela",
            "aqueles",
            "aquelas",
            "aquilo",
        }
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.portuguese_patterns
        ]

    def contains_portuguese(self, text: str) -> bool:
        """Check if text contains Portuguese patterns"""
        if not text or len(text) < 10:
            return False

        # Check for compiled patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True

        # Count Portuguese words
        words = re.findall(r"\b\w+\b", text.lower())
        portuguese_word_count = sum(1 for word in words if word in self.portuguese_words)

        # If more than 5% of words are Portuguese, consider it Portuguese content
        if words and portuguese_word_count / len(words) > 0.05:
            return True

        return False

    def get_portuguese_ratio(self, text: str) -> float:
        """Get ratio of Portuguese content in text"""
        if not text or len(text) < 10:
            return 0.0

        # Count pattern matches
        pattern_matches = sum(1 for pattern in self.compiled_patterns if pattern.search(text))

        # Count Portuguese words
        words = re.findall(r"\b\w+\b", text.lower())
        if not words:
            return 0.0

        portuguese_word_count = sum(1 for word in words if word in self.portuguese_words)

        # Combine metrics (weight patterns more heavily)
        total_score = pattern_matches * 2 + portuguese_word_count
        max_score = len(self.compiled_patterns) * 2 + len(words)

        return total_score / max_score if max_score > 0 else 0.0


class PortugueseToEnglishTranslator:
    """Main translator class for Portuguese to English translation"""

    def __init__(self, base_path: str = None, dry_run: bool = False):
        """Initialize the translator"""
        # Determine base path
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path.cwd()
            # Try to find project root if not already there
            potential_markers = [".git", "requirements.txt", "setup.py", "README.md"]
            if not any((self.base_path / marker).exists() for marker in potential_markers):
                # Try parent directory
                if any((self.base_path.parent / marker).exists() for marker in potential_markers):
                    self.base_path = self.base_path.parent

        self.dry_run = dry_run
        self.dictionary = TRANSLATION_DICTIONARY
        self.translation_memory = {}
        self.detector = PortugueseDetector()

        # Statistics tracking
        self.stats = {
            "files_scanned": 0,
            "files_with_portuguese": 0,
            "files_translated": 0,
            "files_renamed": 0,
            "dirs_renamed": 0,
            "translation_errors": 0,
            "portuguese_words_found": 0,
            "portuguese_patterns_found": 0,
            "words_translated": 0,
        }

        # Load translation memory
        self._load_translation_memory()

        logger.info(f"Translator initialized with base path: {self.base_path}")
        logger.info(f"Dry run: {dry_run}")

    def _load_translation_memory(self):
        """Load translation memory from file if available"""
        memory_path = self.base_path / "tools/language/translation_memory.json"
        if memory_path.exists():
            try:
                with open(memory_path, "r", encoding="utf-8") as f:
                    self.translation_memory = json.load(f)
                logger.info(
                    f"Loaded {len(self.translation_memory)} entries from translation memory"
                )
            except Exception as e:
                logger.warning(f"Error loading translation memory: {e}")

    def save_translation_memory(self):
        """Save translation memory to file"""
        memory_path = self.base_path / "tools/language/translation_memory.json"
        try:
            # Ensure directory exists
            os.makedirs(memory_path.parent, exist_ok=True)

            with open(memory_path, "w", encoding="utf-8") as f:
                json.dump(self.translation_memory, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved {len(self.translation_memory)} entries to translation memory")
            return True
        except Exception as e:
            logger.error(f"Error saving translation memory: {e}")
            return False

    def translate_text(self, text: str) -> str:
        """
        Translate Portuguese text to English using dictionary and translation memory

        Args:
            text: Text to translate

        Returns:
            Translated text
        """
        if not text:
            return text

        # Check translation memory first
        if text in self.translation_memory:
            return self.translation_memory[text]

        translated = text

        # Apply dictionary replacements
        for pt, en in self.dictionary.items():
            # Use word boundaries for whole-word replacements
            pattern = r"\b" + re.escape(pt) + r"\b"
            translated = re.sub(pattern, en, translated, flags=re.IGNORECASE)

        # If the translation changed, store in memory
        if translated != text:
            self.translation_memory[text] = translated
            self.stats["words_translated"] += len(re.findall(r"\b\w+\b", text))

        return translated

    def is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary"""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                return b"\0" in chunk  # Binary files typically contain null bytes
        except Exception:
            return False

    def should_process_file(self, file_path: Path, extensions: List[str]) -> bool:
        """Check if a file should be processed based on extension and content"""
        # Skip if extension doesn't match
        if extensions and file_path.suffix.lower() not in extensions:
            return False

        # Skip binary files
        if self.is_binary_file(file_path):
            return False

        # Skip large files
        if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
            logger.info(f"Skipping large file: {file_path}")
            return False

        # Skip hidden files and directories
        if file_path.name.startswith("."):
            return False

        # Skip files in specific directories
        excluded_dirs = ["venv", "node_modules", ".git", ".pytest_cache", "__pycache__"]
        if any(excluded in file_path.parts for excluded in excluded_dirs):
            return False

        return True

    def translate_file(self, file_path: Path) -> bool:
        """
        Translate a file from Portuguese to English

        Args:
            file_path: Path to the file

        Returns:
            True if file was translated, False otherwise
        """
        try:
            self.stats["files_scanned"] += 1

            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                logger.warning(f"Error reading file {file_path}: {e}")
                return False

            # Check if file contains Portuguese
            if not self.detector.contains_portuguese(content):
                return False

            self.stats["files_with_portuguese"] += 1
            logger.info(f"Found Portuguese content in {file_path}")

            # Translate content
            translated_content = self.translate_text(content)

            # If no changes were made, return
            if translated_content == content:
                return False

            # If dry run, just log
            if self.dry_run:
                logger.info(f"[DRY RUN] Would translate file: {file_path}")
                return True

            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            shutil.copy2(file_path, backup_path)

            # Write translated content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated_content)

            self.stats["files_translated"] += 1
            logger.info(f"Translated file: {file_path}")
            return True

        except Exception as e:
            self.stats["translation_errors"] += 1
            logger.error(f"Error translating file {file_path}: {e}")
            return False

    def translate_file_name(self, file_path: Path) -> Optional[Path]:
        """
        Translate a Portuguese file name to English

        Args:
            file_path: Path to the file

        Returns:
            New path if renamed, original path if not renamed, None on error
        """
        try:
            # Translate file name
            original_name = file_path.name
            translated_name = self.translate_text(original_name)

            # If no changes, return original path
            if translated_name == original_name:
                return file_path

            # Create new path
            new_path = file_path.parent / translated_name

            # If dry run, just log
            if self.dry_run:
                logger.info(f"[DRY RUN] Would rename file: {file_path} -> {new_path}")
                return new_path

            # Rename file
            file_path.rename(new_path)

            self.stats["files_renamed"] += 1
            logger.info(f"Renamed file: {file_path} -> {new_path}")
            return new_path

        except Exception as e:
            logger.error(f"Error renaming file {file_path}: {e}")
            return None

    def translate_directory_name(self, dir_path: Path) -> Optional[Path]:
        """
        Translate a Portuguese directory name to English

        Args:
            dir_path: Path to the directory

        Returns:
            New path if renamed, original path if not renamed, None on error
        """
        try:
            # Translate directory name
            original_name = dir_path.name
            translated_name = self.translate_text(original_name)

            # If no changes, return original path
            if translated_name == original_name:
                return dir_path

            # Create new path
            new_path = dir_path.parent / translated_name

            # If dry run, just log
            if self.dry_run:
                logger.info(f"[DRY RUN] Would rename directory: {dir_path} -> {new_path}")
                return new_path

            # Rename directory
            dir_path.rename(new_path)

            self.stats["dirs_renamed"] += 1
            logger.info(f"Renamed directory: {dir_path} -> {new_path}")
            return new_path

        except Exception as e:
            logger.error(f"Error renaming directory {dir_path}: {e}")
            return None

    def process_directory(
        self,
        dir_path: Path,
        extensions: List[str],
        rename_files: bool = False,
        rename_dirs: bool = False,
    ) -> Dict[str, int]:
        """
        Process all files in a directory, translating Portuguese content to English

        Args:
            dir_path: Directory to process
            extensions: File extensions to process
            rename_files: Whether to rename files with Portuguese names
            rename_dirs: Whether to rename directories with Portuguese names

        Returns:
            Dictionary with processing statistics
        """
        logger.info(f"Processing directory: {dir_path}")

        # Get all files in directory and subdirectories
        all_files = []
        all_dirs = []

        for root, dirs, files in os.walk(dir_path):
            root_path = Path(root)

            # Add files to list
            for file in files:
                file_path = root_path / file
                if self.should_process_file(file_path, extensions):
                    all_files.append(file_path)

            # Add directories to list
            for directory in dirs:
                dir_path = root_path / directory
                all_dirs.append(dir_path)

        # Process files
        logger.info(f"Found {len(all_files)} files to scan")
        for file_path in all_files:
            self.translate_file(file_path)

        # Rename files if requested
        if rename_files:
            logger.info("Renaming files with Portuguese names...")
            for file_path in all_files:
                self.translate_file_name(file_path)

        # Rename directories if requested (bottom-up to avoid path issues)
        if rename_dirs:
            logger.info("Renaming directories with Portuguese names...")
            all_dirs.sort(key=lambda x: len(str(x).split(os.sep)), reverse=True)
            for dir_path in all_dirs:
                self.translate_directory_name(dir_path)

        # Save translation memory
        self.save_translation_memory()

        return self.stats

    def generate_report(self, output_file: Optional[str] = None) -> str:
        """
        Generate a detailed report of the translation process

        Args:
            output_file: Optional file to write the report to

        Returns:
            Report text
        """
        report = [
            "# EVA & GUARANI EGOS - Translation Report",
            f"## Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Statistics",
            f"- Files scanned: {self.stats['files_scanned']}",
            f"- Files with Portuguese content: {self.stats['files_with_portuguese']}",
            f"- Files translated: {self.stats['files_translated']}",
            f"- Files renamed: {self.stats['files_renamed']}",
            f"- Directories renamed: {self.stats['dirs_renamed']}",
            f"- Translation errors: {self.stats['translation_errors']}",
            f"- Words translated: {self.stats['words_translated']}",
            "",
            "## Translation Memory",
            f"- Entries: {len(self.translation_memory)}",
            "",
            "## Dictionary",
            f"- Entries: {len(self.dictionary)}",
            "",
            "## Examples of Translations",
            "",
        ]

        # Add examples
        examples = list(self.translation_memory.items())[:10]
        for source, target in examples:
            if len(source) > 50:
                source = source[:50] + "..."
            if len(target) > 50:
                target = target[:50] + "..."
            report.append(f'- "{source}" → "{target}"')

        report.append("")
        report.append("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

        # Write to file if requested
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(report))
                logger.info(f"Report written to {output_file}")
            except Exception as e:
                logger.error(f"Error writing report: {e}")

        return "\n".join(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="EVA & GUARANI EGOS - Portuguese to English File Translator"
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=None,
        help="Directory to process (default: current project root)",
    )

    parser.add_argument(
        "-e",
        "--extensions",
        type=str,
        default=".txt,.md,.py,.js,.json",
        help="Comma-separated list of file extensions to process (default: .txt,.md,.py,.js,.json)",
    )

    parser.add_argument("--dry-run", action="store_true", help="Simulate without making changes")

    parser.add_argument(
        "--rename-files", action="store_true", help="Rename files with Portuguese names"
    )

    parser.add_argument(
        "--rename-dirs", action="store_true", help="Rename directories with Portuguese names"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed logs")

    parser.add_argument("-r", "--report", action="store_true", help="Generate detailed report")

    parser.add_argument("-o", "--output", type=str, default=None, help="Output file for the report")

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    # Process extensions
    extensions = [
        ext.strip() if ext.strip().startswith(".") else "." + ext.strip()
        for ext in args.extensions.split(",")
    ]

    # Initialize translator
    translator = PortugueseToEnglishTranslator(args.directory, args.dry_run)

    # Process directory
    stats = translator.process_directory(
        Path(args.directory) if args.directory else translator.base_path,
        extensions,
        args.rename_files,
        args.rename_dirs,
    )

    # Print summary
    print("\nTranslation summary:")
    print(f"- Files scanned: {stats['files_scanned']}")
    print(f"- Files with Portuguese content: {stats['files_with_portuguese']}")
    print(f"- Files translated: {stats['files_translated']}")
    print(f"- Files renamed: {stats['files_renamed']}")
    print(f"- Directories renamed: {stats['dirs_renamed']}")
    print(f"- Translation errors: {stats['translation_errors']}")
    print(f"- Words translated: {stats['words_translated']}")

    # Generate report if requested
    if args.report or args.output:
        output_file = args.output or "translation_report.md"
        report = translator.generate_report(output_file)
        if args.verbose:
            print("\nReport:")
            print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
