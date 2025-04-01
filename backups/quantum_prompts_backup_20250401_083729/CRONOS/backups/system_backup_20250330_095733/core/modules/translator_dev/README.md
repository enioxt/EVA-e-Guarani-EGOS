---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: modules
  changelog: []
  dependencies:
  - TRANSLATOR
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: TRANSLATOR
  test_coverage: 0.9
  translation_status: completed
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

# EVA & GUARANI Translator

Advanced translation utility that converts Portuguese files to English while preserving formatting and structure.

## Features

### Automatic Detection of Portuguese Content

- Enhanced language detection using the `py3langid` library for accurate identification
- Smart confidence scoring to minimize false positives
- Supports scanning entire directories for files containing Portuguese text

### Multiple Translation Engines

- HuggingFace (offline): Local machine translation without API costs
- OpenAI (online): Higher quality translation with usage monitoring

### Smart Caching

- Caches translations to avoid redundant processing
- Significantly speeds up repeated translations
- Preserves resources by avoiding unnecessary API calls

### Format-Specific Handling

- **Markdown**: Preserves formatting while translating content
- **HTML/XML**: Translates text while preserving tags and structure
- **JSON/YAML**: Intelligently handles data structures
- **Source Code**: Translates comments while preserving code functionality

### Technical Terminology Management

- Dictionary of technical terms to ensure consistent translation
- Ability to add custom terminology for your specific domain
- Pre/post-processing rules for technical content

### Concurrent Batch Processing

- Translates multiple files simultaneously
- Optimizes performance with multi-threading
- Progress tracking with detailed statistics

### Command-Line Interface

- Intuitive terminal UI with progress bars and status indicators
- Detailed progress reporting and translation statistics
- Session management to pause and resume translations

## Installation

### Windows

1. Ensure you have Python 3.8 or newer installed:

   ```
   python --version
   ```

2. Clone the repository or navigate to the EVA & GUARANI directory:

   ```
   cd path\to\eva-guarani-egos
   ```

3. Install the required dependencies:

   ```
   pip install -r modules/translator_dev/requirements.txt
   ```

4. For optional components (recommended):

   ```
   pip install py3langid beautifulsoup4
   ```

## Usage

### Scanning for Portuguese Files

```
python modules/translator_dev/translator.py --scan path/to/directory
```

### Translating Files

```
python modules/translator_dev/translator.py --translate path/to/directory --output path/to/output
```

### Additional Options

```
python modules/translator_dev/translator.py --help
```

## Development Status

### Completed

- Core translation functionality
- Multiple engine support
- Caching system
- Concurrent processing
- Format-specific handlers for Markdown and code files
- Language detection with py3langid
- Technical terminology dictionary

### In Progress

- Enhanced HTML/XML handling
- Improved JSON/YAML support
- OpenAI engine integration
- Cost monitoring

### Planned

- Additional format-specific handlers
- Support for RTL languages
- Terminology management UI
- Training custom models

## VSCode Integration

For the best experience using the translator with VSCode:

1. **Open the project folder in VSCode**:

   ```bash
   code .
   ```

2. **Install recommended extensions**:
   - Python extension by Microsoft
   - YAML extension for better YAML file editing
   - Markdown All in One for better Markdown preview

3. **Configure Python Interpreter**:
   - Press `Ctrl+Shift+P` to open the command palette
   - Type "Python: Select Interpreter" and select your virtual environment

4. **Create VSCode Tasks** (optional):

   Create a `.vscode/tasks.json` file with the following content:

   ```json
   {
       "version": "2.0.0",
       "tasks": [
           {
               "label": "Scan for Portuguese",
               "type": "shell",
               "command": "${command:python.interpreterPath}",
               "args": [
                   "modules/translator_dev/translator.py",
                   "--scan",
                   "${input:folderPath}"
               ],
               "group": "test",
               "presentation": {
                   "reveal": "always",
                   "panel": "new"
               }
           },
           {
               "label": "Translate Files",
               "type": "shell",
               "command": "${command:python.interpreterPath}",
               "args": [
                   "modules/translator_dev/translator.py",
                   "--translate",
                   "${input:folderPath}"
               ],
               "group": "test",
               "presentation": {
                   "reveal": "always",
                   "panel": "new"
               }
           }
       ],
       "inputs": [
           {
               "id": "folderPath",
               "type": "promptString",
               "description": "Path to scan or translate",
               "default": "."
           }
       ]
   }
   ```

   With this configuration, you can run the scanner or translator directly from VSCode's Tasks menu.

## Troubleshooting

### Common Issues on Windows

1. **File Path Issues**:
   - Windows uses backslashes (`\`) for file paths, but the translator accepts both forward slashes (`/`) and backslashes.
   - For paths with spaces, use quotes: `"C:\My Documents\project"`

2. **Permission Issues**:
   - Run Command Prompt or PowerShell as Administrator if you encounter permission errors.

3. **Encoding Issues**:
   - If you see encoding errors, make sure your files are saved with UTF-8 encoding.
   - In VSCode, you can change the encoding in the bottom right corner.

4. **Library Installation Errors**:
   - If `pip install` fails, try upgrading pip first: `python -m pip install --upgrade pip`
   - For binary packages that fail to install, look for pre-compiled wheels on [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

### Getting Help

If you encounter issues not covered here, please:

1. Check the logs in the `logs` directory
2. Open an issue on GitHub
3. Contact the development team

## Development Documentation

For developers looking to extend or modify the translator, please refer to the [Developer Guide](./docs/DEVELOPMENT.md).

## Recent Updates

- Added py3langid for improved language detection
- Enhanced format preservation for Markdown and HTML
- Implemented technical term dictionary
- Added concurrent processing for batch translations

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

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

```bash
# Set a monthly budget of $10
python translator.py --budget 10.00 --translate path/to/directory
```

## Development Status

### Completed

- ✅ Configuration system with YAML support
- ✅ Translation cache implementation
- ✅ File scanner with Portuguese detection
- ✅ Multiple translation engines (HuggingFace, OpenAI)
- ✅ Translation processor with statistics
- ✅ Format-specific handlers for various file types
- ✅ Technical terminology management
- ✅ Cost monitoring and budget controls
- ✅ Enhanced CLI with progress reporting
- ✅ Session management for batch translations
- ✅ Concurrent processing support

### In Progress

- 🔄 Improved file type detection accuracy
- 🔄 Additional format-specific handlers
- 🔄 Enhanced technical terminology recognition

### Planned

- ⏳ GUI interface
- ⏳ API server mode
- ⏳ Integration with version control systems
- ⏳ Additional translation engines

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
