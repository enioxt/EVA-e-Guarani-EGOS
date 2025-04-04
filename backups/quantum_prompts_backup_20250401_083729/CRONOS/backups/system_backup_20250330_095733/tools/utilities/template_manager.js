---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: tools
  changelog: []
  dependencies:
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
  subsystem: MASTER
  test_coverage: 0.9
  translation_status: completed
  type: javascript
  version: '8.0'
  windows_compatibility: true
---
/**
METADATA:
  type: utility
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
 */

javascript
/**
 * EVA & GUARANI - Template Manager
 * ========================================
 *
 * This module manages the templates used for creating new files
 * and inserting quantum context, following the EVA & GUARANI principles
 * and facilitating code creation with integrated ethical awareness.
 *
 * Incorporated principles:
 * - Ethics: Templates that promote good practices and adequate documentation
 * - Love: Supportive and encouraging messages in comments
 * - Economy: Optimized templates without redundant code
 * - Art: Elegant and visually harmonious structure
 *
 * @context EVA_GUARANI_QUANTUM_TEMPLATES
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Default templates for different file types
 * Organized modularly to facilitate extension and modification.
 * @private
 */
const DEFAULT_TEMPLATES = {
    // Template for JavaScript
    javascript: {
        header: (filename, author = 'EVA & GUARANI Team') => `/**
 * ${path.basename(filename)}
 * ${Array(path.basename(filename).length + 1).join('=')}
 *
 * @context EVA_GUARANI
 * @created ${new Date().toISOString().split('T')[0]}
 * @author ${author}
 *
 * This file was created with ethical awareness and love for code.
 * EVA & GUARANI: Development with purpose and responsibility.
 */\n\n`,

        class: (className) => `/**
 * Class ${className}
 * Implementation with ethical and modular awareness.
 */
class ${className} {
    /**
     * Class constructor
     * @param {Object} config - Initial configuration
     */
    constructor(config = {}) {
        this.config = config;
        this._initialize();
    }

    /**
     * Initializes the class with economic awareness
     * @private
     */
    _initialize() {
        // Implement initialization here
        console.log('${className} initialized with love and awareness');
    }

    // Public methods with clear documentation
}

module.exports = ${className};\n`,

        function: (funcName) => `/**
 * ${funcName}
 * Function implemented with ethical and economic awareness.
 *
 * @param {Object} params - Function parameters
 * @returns {Promise<Object>} Operation result
 */
async function ${funcName}(params = {}) {
    // Conscious and economic implementation
    return {
        success: true,
        message: 'Operation performed with love and ethics'
    };
}

module.exports = ${funcName};\n`,

        module: (moduleName) => `/**
 * Module ${moduleName}
 * Implementation with ethical awareness and modular functionalities.
 */

// Conscious and economic imports

/**
 * Module functions and methods
 */

// Export functions with clear documentation
module.exports = {
    // Exported functions
};\n`
    },

    // Template for TypeScript
    typescript: {
        header: (filename, author = 'EVA & GUARANI Team') => `/**
 * ${path.basename(filename)}
 * ${Array(path.basename(filename).length + 1).join('=')}
 *
 * @context EVA_GUARANI
 * @created ${new Date().toISOString().split('T')[0]}
 * @author ${author}
 *
 * This file was created with ethical awareness and love for code.
 * EVA & GUARANI: Development with purpose and responsibility.
 */\n\n`,

        interface: (interfaceName) => `/**
 * Interface ${interfaceName}
 * Contract definition with ethical awareness and responsibility.
 */
export interface ${interfaceName} {
    // Properties with clear documentation
    name: string;
    description?: string;

    // Methods with clear documentation
    initialize(): Promise<void>;
};\n`,

        class: (className, interfaceName = null) => {
            const implementsInterface = interfaceName ? ` implements ${interfaceName}` : '';
            return `/**
 * Class ${className}
 * Implementation with ethical and modular awareness.
 */
export class ${className}${implementsInterface} {
    // Private properties with well-defined purpose
    private config: Record<string, any>;

    /**
     * Class constructor
     * @param config - Initial configuration
     */
    constructor(config: Record<string, any> = {}) {
        this.config = config;
        this._initialize();
    }

    /**
     * Initializes the class with economic awareness
     * @private
     */
    private _initialize(): void {
        // Implement initialization here
        console.log('${className} initialized with love and awareness');
    }

    /**
     * Initializes the component
     */
    public async initialize(): Promise<void> {
        // Ethical and economic implementation
    }

    // Public methods with clear documentation
};\n`;
        },

        type: (typeName) => `/**
 * Type ${typeName}
 * Definition with ethical awareness and intentional clarity.
 */
export type ${typeName} = {
    // Properties with clear documentation
    id: string;
    name: string;
    description?: string;

    // Additional properties with clear purpose
};\n`
    },

    // Template for Python
    python: {
        header: (filename, author = 'EVA & GUARANI Team') => `"""
${path.basename(filename)}
${Array(path.basename(filename).length + 1).join('=')}

@context EVA_GUARANI
@created ${new Date().toISOString().split('T')[0]}
@author ${author}

This file was created with ethical awareness and love for code.
EVA & GUARANI: Development with purpose and responsibility.
"""

import logging
from typing import Dict, List, Optional, Union, Any

# Logging configuration with awareness
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)\n\n`,

        class: (className) => `class ${className}:
    """
    Class ${className}
    Implementation with ethical and modular awareness.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initializes the class with love and awareness.

        Args:
            config: Initial configuration
        """
        self.config = config or {}
        self._initialize()

    def _initialize(self) -> None:
        """
        Initializes the class with economic awareness.
        Private method for internal configuration.
        """
        # Implement initialization here
        logger.info("${className} initialized with love and awareness")

    # Public methods with clear documentation\n`,

        function: (funcName) => `def ${funcName}(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    ${funcName}
    Function implemented with ethical and economic awareness.

    Args:
        params: Function parameters

    Returns:
        Dict with operation result
    """
    params = params or {}

    // Conscious and economic implementation
    return {
        "success": True,
        "message": "Operation performed with love and ethics"
    }\n`
    },

    // Template for Markdown
    markdown: {
        header: (filename, author = 'EVA & GUARANI Team') => `# ${path.basename(filename, '.md')}

> *Created with ethical awareness by ${author} on ${new Date().toISOString().split('T')[0]}*
> *Context: EVA_GUARANI*

## 🌌 Overview

Description of the purpose of this document with ethical awareness.

## 📋 Content

1. [Introduction](#introduction)
2. [Principles](#principles)
3. [Implementation](#implementation)
4. [Ethical Considerations](#ethical-considerations)

## Introduction

Introduce the topic with clarity and purpose.

## Principles

List the relevant principles:

- **Integrated Ethics**: Principle description
- **Love for Code**: Principle description
- **Resource Economy**: Principle description
- **Art in Structure**: Principle description

## Implementation

Implementation details with awareness and clarity.

## Ethical Considerations

Reflections on relevant ethical aspects.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n\n`
    },

    // Template for HTML
    html: {
        header: (filename, author = 'EVA & GUARANI Team') => `<!DOCTYPE html>
<!--
    ${path.basename(filename)}
    @context EVA_GUARANI
    @created ${new Date().toISOString().split('T')[0]}
    @author ${author}

    This file was created with ethical awareness and love for code.
    EVA & GUARANI: Development with purpose and responsibility.
-->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${path.basename(filename, '.html')}</title>
    <meta name="description" content="Page created with ethical awareness and love.">
    <!-- Styles with aesthetic awareness -->
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            background-color: #f9f9f9;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            color: #8e44ad;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            color: #888;
        }
    </style>
</head>
<body>
    <header>
        <h1>${path.basename(filename, '.html')}</h1>
        <p>Created with ethical awareness and love</p>
    </header>

    <div class="container">
        <!-- Main content here -->
        <p>Content developed with ethics and purpose.</p>
    </div>

    <footer>
        <p>✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧</p>
    </footer>
</body>
</html>\n`
    }
};

/**
 * Class responsible for template management
 * Implements functionalities for inserting code with ethical
 * awareness and respect for each language's style.
 */
class TemplateManager {
    /**
     * Initializes the template manager
     * @param {vscode.ExtensionContext} context - Extension context
     * @param {Object} config - EVA & GUARANI configuration
     */
    constructor(context, config) {
        this.context = context;
        this.config = config;
        this.templates = {...DEFAULT_TEMPLATES};

        // Load customized templates from the project
        this._loadCustomTemplates();
    }

    /**
     * Loads customized templates from the current project
     * respecting autonomy and specific needs.
     * @private
     */
    _loadCustomTemplates() {
        const projectRoot = this.config.getProjectRoot();
        if (!projectRoot) return;

        const customTemplatesPath = path.join(projectRoot, '.evaguarani', 'templates');

        if (fs.existsSync(customTemplatesPath)) {
            try {
                // Look for customized templates by language
                const languages = fs.readdirSync(customTemplatesPath);

                for (const language of languages) {
                    const languagePath = path.join(customTemplatesPath, language);
                    if (fs.statSync(languagePath).isDirectory()) {
                        // Register language if it doesn't exist
                        if (!this.templates[language]) {
                            this.templates[language] = {};
                        }

                        // Load templates for this language
                        const templateFiles = fs.readdirSync(languagePath)
                            .filter(file => file.endsWith('.js') || file.endsWith('.mjs'));

                        for (const templateFile of templateFiles) {
                            const templateName = path.basename(templateFile, path.extname(templateFile));
                            const templatePath = path.join(languagePath, templateFile);

                            try {
                                // Dynamically load the template
                                const template = require(templatePath);
                                if (typeof template === 'function') {
                                    this.templates[language][templateName] = template;
                                    console.log(`EVA & GUARANI: Template '${templateName}' for ${language} loaded successfully`);
                                }
                            } catch (err) {
                                console.log(`EVA & GUARANI: Error loading template '${templateFile}': ${err.message}`);
                            }
                        }
                    }
                }

                console.log('EVA & GUARANI: Customized templates loaded with love and respect');
            } catch (error) {
                console.log(`EVA & GUARANI: Error loading customized templates: ${error.message}`);
            }
        }
    }

    /**
     * Checks if a template should be inserted and does so if necessary
     * @param {vscode.TextEditor} editor - Active editor
     * @returns {boolean} If a template was inserted
     */
    checkAndInsertTemplate(editor) {
        if (!editor || !this.config.get('addHeaderToNewFiles', true)) {
            return false;
        }

        // Check if the file is empty
        if (editor.document.getText().trim() !== '') {
            return false;
        }

        // Determine file type
        const filename = editor.document.fileName;
        const fileType = this._getFileType(filename);

        if (!fileType) {
            return false; // Unsupported file type
        }

        // Insert appropriate template with awareness and love
        return this._insertHeader(editor, fileType, filename);
    }

    /**
     * Adds EVA & GUARANI quantum context to the file
     * @param {vscode.TextEditor} editor - Active editor
     * @returns {boolean} If the context was added
     */
    addQuantumContextToFile(editor) {
        if (!editor) {
            return false;
        }

        // Determine file type
        const filename = editor.document.fileName;
        const fileType = this._getFileType(filename);

        if (!fileType) {
            vscode.window.showInformationMessage('Unsupported file type for quantum context addition.');
            return false;
        }

        // Check if quantum context already exists
        const documentText = editor.document.getText();
        if (documentText.includes('@context EVA_GUARANI')) {
            vscode.window.showInformationMessage('File already has EVA & GUARANI quantum context.');
            return false;
        }

        // Add header at the beginning of the file
        return this._insertHeader(editor, fileType, filename);
    }

    /**
     * Detects the file type based on the extension
     * @param {string} filename - File name
     * @returns {string|null} File type or null if unsupported
     * @private
     */
    _getFileType(filename) {
        const ext = path.extname(filename).toLowerCase();

        // Map extension to template type
        switch (ext) {
            case '.js':
            case '.jsx':
            case '.mjs':
            case '.cjs':
                return 'javascript';

            case '.ts':
            case '.tsx':
                return 'typescript';

            case '.py':
            case '.pyw':
                return 'python';

            case '.md':
            case '.markdown':
                return 'markdown';

            case '.html':
            case '.htm':
                return 'html';

            default:
                // Check if we have a custom template for this extension
                for (const language in this.templates) {
                    if (this.templates[language].extensions &&
                        this.templates[language].extensions.includes(ext)) {
                        return language;
                    }
                }

                return null; // Unsupported
        }
    }

    /**
     * Inserts a header at the beginning of the file
     * @param {vscode.TextEditor} editor - Active editor
     * @param {string} fileType - File type
     * @param {string} filename - File name
     * @returns {boolean} If the header was inserted
     * @private
     */
    _insertHeader(editor, fileType, filename) {
        // Check if we have a template for this type
        if (!this.templates[fileType] || !this.templates[fileType].header) {
            return false;
        }

        // Determine author name (use Git user name if available)
        let author = 'EVA & GUARANI Team';
        try {
            // Try to get user name from Git settings
            const gitConfig = path.join(require('os').homedir(), '.gitconfig');
            if (fs.existsSync(gitConfig)) {
                const content = fs.readFileSync(gitConfig, 'utf8');
                const match = /name\s*=\s*(.+)/.exec(content);
                if (match && match[1]) {
                    author = match[1].trim();
                }
            }
        } catch (err) {
            // Silently fail and use default author
        }

        // Generate header content
        const headerContent = this.templates[fileType].header(filename, author);

        // Insert at the beginning of the file
        editor.edit(editBuilder => {
            editBuilder.insert(new vscode.Position(0, 0), headerContent);
        }).then(success => {
            if (success) {
                vscode.window.showInformationMessage(
                    '✧ EVA & GUARANI quantum context added with love and awareness ✧'
                );
            }
        });

        return true;
    }

    /**
     * Inserts a class template
     * @param {vscode.TextEditor} editor - Active editor
     * @param {string} className - Class name
     * @returns {Promise<boolean>} If the template was inserted
     */
    async insertClassTemplate(editor, className) {
        if (!editor || !className) {
            return false;
        }

        const fileType = this._getFileType(editor.document.fileName);
        if (!fileType || !this.templates[fileType] || !this.templates[fileType].class) {
            vscode.window.showInformationMessage(
                'No class template available for this file type.'
            );
            return false;
        }

        // Generate class template
        let templateContent;

        // For TypeScript, check if you want to implement an interface
        if (fileType === 'typescript' && await this._askImplementInterface()) {
            const interfaceName = await vscode.window.showInputBox({
                prompt: 'Name of the interface to implement',
                placeHolder: 'IClassName'
            });

            if
