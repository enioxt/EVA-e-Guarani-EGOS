# EVA & GUARANI Translator

A modular and efficient tool for automatic file translation, focusing on code and technical documentation.

## Features

- Automatic detection of Portuguese content in files and directories
  - Enhanced language detection using langdetect library
  - Smart confidence scoring for accurate identification
- Multiple translation engines:
  - HuggingFace (offline, runs locally)
  - OpenAI (high quality, requires API key)
- Smart caching system to avoid retranslating the same content
- Format-specific content handling:
  - Markdown preservation with special handling of links, code blocks, and formatting
  - HTML/XML preservation with specialized tag and attribute handling
  - JSON/YAML structure preservation with translation of string values only
  - Code-aware translation that preserves syntax and structure
- Technical terminology management:
  - Dictionary of technical terms in multiple categories
  - Automatic preservation of technical terms during translation
  - Ability to add custom terminology
- Concurrent batch processing for faster translation of multiple files
- Command-line interface with progress reporting and statistics
- Detailed reporting of translation results
- File and directory batch processing
- Cost control and budget management for API-based engines
  - Monthly budget limits and usage tracking
  - Automatic fallback to offline engines when limits are reached
  - Detailed usage statistics and warnings

## Installation

```bash
# Navigate to the project directory
cd C:\Eva & Guarani - EGOS\modules\translator_dev

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Scanning for Portuguese Files

```bash
# Scan a directory for Portuguese files
python translator.py scan path/to/directory
```

### Translating Files

```bash
# Translate a single file
python translator.py file path/to/file.py

# Translate all Portuguese files in a directory (with scan)
python translator.py directory path/to/directory --scan

# Translate files from a batch file or report
python translator.py batch path/to/report.md
```

## Configuration

Edit `config/settings.yaml` to customize behavior:

```yaml
engine:
  name: huggingface  # or openai
  api_key: null      # required for OpenAI
  model: Helsinki-NLP/opus-mt-pt-en  # default model for HuggingFace
  max_tokens: 4096
  temperature: 0.3

scanner:
  ignore_dirs:
    - .git
    - __pycache__
  file_extensions:
    - .py
    - .md
    - .txt

cache:
  enabled: true
  directory: ./cache
  max_size: 1000000000  # 1GB
```

## Project Structure

```
translator_dev/
├── README.md               # This file
├── requirements.txt        # Project dependencies
├── translator.py           # Main entry point
├── config/                 # Configuration files
│   ├── settings.yaml       # Main configuration
│   └── config.py           # Configuration manager
├── engines/                # Translation engines
│   ├── openai/             # OpenAI engine
│   └── huggingface/        # HuggingFace engine
├── core/                   # Core functionality
│   ├── cache.py            # Translation cache
│   ├── scanner.py          # File scanner
│   └── processor.py        # Translation processor
├── ui/                     # User interfaces
│   └── cli.py              # Command-line interface
├── tests/                  # Test files
└── examples/               # Usage examples
```

## Translation Engines

### HuggingFace (Offline)

The HuggingFace engine uses the MarianMT model to translate text offline without requiring an API key. It's completely private and works without internet access, but the translation quality may be lower than online services.

```yaml
engine:
  name: huggingface
  model: Helsinki-NLP/opus-mt-pt-en
```

### OpenAI (Online)

The OpenAI engine provides high-quality translations using GPT models. It requires an API key and internet access, but delivers superior translation quality with better context understanding and format preservation.

```yaml
engine:
  name: openai
  api_key: your_api_key_here  # or set OPENAI_API_KEY environment variable
  model: gpt-4o
  temperature: 0.3
```

## Format-Specific Handling

The translator includes specialized handling for different file types:

### Markdown

- Preserves all Markdown formatting (headings, lists, emphasis)
- Protects links, images, and code blocks during translation
- Maintains document structure and whitespace

### HTML/XML

- Preserves all HTML tags and attributes
- Translates only text content between tags
- Keeps JavaScript and CSS code intact

### JSON/YAML

- Maintains data structure and formatting
- Translates only string values, not keys
- Preserves numbers, booleans, and null values

### Source Code

- Translates only comments and string literals
- Preserves all code logic, variables, and syntax
- Maintains indentation and formatting

## Technical Terminology Management

The translator includes a comprehensive technical terms dictionary to ensure consistent translation of specialized terms:

- Programming terms (functions, classes, variables, etc.)
- Translation-specific terminology
- EVA & GUARANI specific terms
- File type and structure terms
- AI/ML terminology

You can add custom terms through the term manager interface or by directly editing the `config/technical_terms.json` file.

## Development Status

Currently in Phase 1: Stabilization and Foundation

### Completed

- [x] Basic project structure
- [x] Configuration system with YAML support
- [x] Cache implementation for translation efficiency
- [x] HuggingFace engine for offline translation
- [x] OpenAI engine for high-quality translation
- [x] Language detection with enhanced accuracy
- [x] Format-specific translation handlers
- [x] Technical terminology management
- [x] Concurrent batch processing
- [x] CLI interface with progress reporting
- [x] Enhanced visual interface with clean output
- [x] Pause/resume translation functionality
- [x] Session management system
- [x] Safe file protection mechanism
- [x] Detailed statistics and reporting

### In Progress

- [ ] Improved file type detection
- [ ] Additional format-specific handlers
- [ ] TUI interface with more interactive features
- [ ] Quarantine system for unused/sensitive files

### Planned

- [ ] GUI interface
- [ ] VS Code extension
- [ ] Git integration hooks
- [ ] REST API for service integration
- [ ] Custom technical terms editor

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for your changes
5. Make sure all tests pass
6. Submit a pull request

## License

This project is part of EVA & GUARANI and follows its licensing terms.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

## Cost Management

The translator includes a cost management system to help control expenses when using paid API-based translation services like OpenAI:

### Features

- **Monthly Budget Setting**: Set a maximum monthly budget for API usage.
- **Usage Tracking**: Automatically tracks and records API usage costs.
- **Budget Warnings**: Provides warnings when approaching your budget limit.
- **Automatic Fallback**: Falls back to free offline engines when budget limits are reached.
- **Usage Reports**: View detailed usage statistics by month.

### Configuration

Configure cost controls in your `settings.yaml` file:

```yaml
engine:
  name: huggingface  # Default to offline engine to save costs
  cost_control:
    enabled: true
    monthly_budget: 5.00  # Maximum monthly budget in USD
    warn_at_percent: 80   # Warn when reaching 80% of budget
```

### Optimizing for Cost Efficiency

To minimize translation costs:

1. **Use HuggingFace By Default**: The offline engine has no API costs but slightly lower quality.
2. **Enable Caching**: Avoid retranslating the same content multiple times.
3. **Use Selective Translation**: Only translate files that actually contain Portuguese.
4. **Smaller Token Limits**: Set lower `max_tokens` values for the OpenAI engine.
5. **Economy Model**: Use `gpt-3.5-turbo` instead of the more expensive `gpt-4` models.
