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
  type: configuration
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
 * EVA & GUARANI - Configuration Module
 * ======================================
 * 
 * This module manages all the settings for the EVA & GUARANI extension
 * for VSCode, allowing customization and adaptation to the user's needs
 * with respect to their autonomy and privacy.
 * 
 * Incorporated principles:
 * - Ethics: Respect for user choices and transparency in settings
 * - Love: Default settings designed for the developer's well-being
 * - Economy: Efficient storage of settings and conscious use of resources
 * - Art: Harmonious and intuitive configuration interface
 * 
 * @context EVA_GUARANI_QUANTUM_CONFIG
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Default values for extension settings.
 * Defined with ethical awareness and love for the developer.
 * @private
 */
const DEFAULT_CONFIG = {
    // System settings
    enabled: true,
    syncEnabled: false,
    syncOnSave: false,
    cloudSyncUrl: '',
    
    // Analysis settings
    analyzeJavaScript: true,
    analyzeTypeScript: true,
    analyzePython: true,
    analyzeMarkdown: true,
    analysisDepth: 2, // 1-Superficial, 2-Normal, 3-Deep
    
    // Terminology settings
    enforceTerminology: true,
    terminologyViolationSeverity: 'Warning', // 'Hint', 'Information', 'Warning', 'Error'
    
    // Interface settings
    showWelcomeOnStartup: true,
    themeDarkMode: true,
    alwaysShowWelcome: false,
    statusBarPosition: 'right',
    
    // Template settings
    addHeaderToNewFiles: true,
    defaultTemplateLanguage: 'auto', // 'auto', 'js', 'ts', 'py', 'md'
    
    // Mapping settings
    systemMapAutoBuild: true,
    systemMapUpdateOnSave: true,
    
    // AI settings
    aiRecommendationsEnabled: true,
    aiPrivacySetting: 'local', // 'local', 'anonymous', 'full'
    
    // Ethical settings
    ethicalAnalysisEnabled: true,
    privacyPreservation: 'maximum', // 'balanced', 'maximum'
};

/**
 * File extensions for analysis and their types
 * @private
 */
const FILE_TYPES = {
    // JavaScript
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    
    // TypeScript
    '.ts': 'typescript',
    '.tsx': 'typescript',
    
    // Python
    '.py': 'python',
    '.pyw': 'python',
    '.pyi': 'python',
    
    // Documentation
    '.md': 'markdown',
    '.markdown': 'markdown',
    
    // Data
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    
    // Web
    '.html': 'html',
    '.css': 'css',
    '.scss': 'css',
    '.sass': 'css',
};

/**
 * Main class for ethical management of EVA & GUARANI settings
 */
class EVAGuaraniConfig {
    /**
     * Initializes the configuration with default values and loads
     * user settings ethically and consciously.
     */
    constructor() {
        this.config = {...DEFAULT_CONFIG};
        this.projectRoot = '';
        this.configWatcher = null;
        this.localConfigPath = '';
        
        // Load VSCode settings
        this._loadVSCodeConfig();
        
        // Set up change watcher (with economic awareness)
        this._setupConfigWatcher();
    }
    
    /**
     * Loads VSCode settings ethically and transparently
     * @private
     */
    _loadVSCodeConfig() {
        const vsConfig = vscode.workspace.getConfiguration('evaguarani');
        
        // Load each setting respecting user choices
        for (const key in this.config) {
            if (vsConfig.has(key)) {
                this.config[key] = vsConfig.get(key);
            }
        }
        
        console.log('EVA & GUARANI: VSCode settings loaded with love and respect');
    }
    
    /**
     * Sets up watcher for configuration changes
     * with economic resource implementation
     * @private
     */
    _setupConfigWatcher() {
        // Disable previous watcher if exists (resource economy)
        if (this.configWatcher) {
            this.configWatcher.dispose();
        }
        
        // Watch for configuration changes for real-time updates
        this.configWatcher = vscode.workspace.onDidChangeConfiguration(event => {
            if (event.affectsConfiguration('evaguarani')) {
                this._loadVSCodeConfig();
                console.log('EVA & GUARANI: Settings updated in real-time');
            }
        });
    }
    
    /**
     * Checks if the extension is enabled
     * @returns {boolean} Extension activation status
     */
    isEnabled() {
        return this.config.enabled;
    }
    
    /**
     * Sets the root directory of the EVA & GUARANI project
     * @param {string} rootPath - Root directory path
     */
    setProjectRoot(rootPath) {
        this.projectRoot = rootPath;
        
        // Check and load local project configuration ethically
        this.localConfigPath = path.join(rootPath, '.evaguarani', 'config.json');
        this._loadLocalConfig();
        
        console.log(`EVA & GUARANI: Root directory set: ${rootPath}`);
    }
    
    /**
     * Returns the root directory of the EVA & GUARANI project
     * @returns {string} Root directory path
     */
    getProjectRoot() {
        return this.projectRoot;
    }
    
    /**
     * Loads local project settings, respecting
     * the project's sovereignty and specific needs.
     * @private
     */
    _loadLocalConfig() {
        if (fs.existsSync(this.localConfigPath)) {
            try {
                const localConfig = JSON.parse(fs.readFileSync(this.localConfigPath, 'utf8'));
                
                // Merge with current settings, respecting local configuration
                this.config = {...this.config, ...localConfig};
                
                console.log('EVA & GUARANI: Local project settings loaded');
            } catch (error) {
                console.log(`EVA & GUARANI: Error loading local settings: ${error.message}`);
            }
        }
    }
    
    /**
     * Saves local project settings, preserving
     * the project's autonomy and particularities.
     * @private
     */
    _saveLocalConfig() {
        if (this.projectRoot) {
            try {
                const evaguaraniDir = path.join(this.projectRoot, '.evaguarani');
                
                // Create directory if it doesn't exist
                if (!fs.existsSync(evaguaraniDir)) {
                    fs.mkdirSync(evaguaraniDir, {recursive: true});
                }
                
                // Save local configuration
                fs.writeFileSync(
                    this.localConfigPath, 
                    JSON.stringify(this.config, null, 2), 
                    'utf8'
                );
                
                console.log('EVA & GUARANI: Local settings saved successfully');
                return true;
            } catch (error) {
                console.log(`EVA & GUARANI: Error saving local settings: ${error.message}`);
                return false;
            }
        }
        return false;
    }
    
    /**
     * Determines if a file should be analyzed based on
     * its characteristics and analysis settings.
     * @param {string} filePath - File path
     * @returns {boolean} If the file should be analyzed
     */
    shouldAnalyzeFile(filePath) {
        if (!this.isEnabled()) {
            return false;
        }
        
        // Check file extension
        const ext = path.extname(filePath).toLowerCase();
        const fileType = FILE_TYPES[ext];
        
        if (!fileType) {
            return false; // Unsupported file type
        }
        
        // Check specific setting for file type
        switch (fileType) {
            case 'javascript':
                return this.config.analyzeJavaScript;
            case 'typescript':
                return this.config.analyzeTypeScript;
            case 'python':
                return this.config.analyzePython;
            case 'markdown':
                return this.config.analyzeMarkdown;
            default:
                return false;
        }
    }
    
    /**
     * Determines if it should sync on save
     * @returns {boolean} If it should sync automatically
     */
    shouldSyncOnSave() {
        return this.isEnabled() && this.config.syncEnabled && this.config.syncOnSave;
    }
    
    /**
     * Determines if it should always show the welcome message
     * @returns {boolean} Configuration status
     */
    shouldAlwaysShowWelcome() {
        return this.config.alwaysShowWelcome;
    }
    
    /**
     * Gets the value of a specific setting
     * @param {string} key - Setting name
     * @param {any} defaultValue - Default value if not exists
     * @returns {any} Setting value
     */
    get(key, defaultValue) {
        return key in this.config ? this.config[key] : defaultValue;
    }
    
    /**
     * Sets the value of a specific setting,
     * updating both locally and in VSCode
     * @param {string} key - Setting name
     * @param {any} value - New value
     * @param {boolean} global - If it should save globally
     * @returns {boolean} Operation success
     */
    set(key, value, global = false) {
        if (key in this.config) {
            // Update local setting
            this.config[key] = value;
            
            // Update VSCode setting
            if (global) {
                const vsConfig = vscode.workspace.getConfiguration('evaguarani');
                vsConfig.update(key, value, true);
            }
            
            // Save local setting
            this._saveLocalConfig();
            
            return true;
        }
        return false;
    }
    
    /**
     * Returns configured analysis depth
     * @returns {number} Depth (1-3)
     */
    getAnalysisDepth() {
        return this.config.analysisDepth;
    }
    
    /**
     * Checks if AI recommendations are enabled
     * @returns {boolean} Configuration status
     */
    isAIRecommendationsEnabled() {
        return this.isEnabled() && this.config.aiRecommendationsEnabled;
    }
    
    /**
     * Shows interface for extension configuration,
     * with artistic and intuitive design for the user.
     */
    showConfigurationUI() {
        // Configuration interface implementation using WebView
        const panel = vscode.window.createWebviewPanel(
            'evaguaraniConfig',
            '✧ EVA & GUARANI Configuration ✧',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );
        
        // Generate HTML for configuration interface with art and love
        panel.webview.html = this._generateConfigHTML();
        
        // Process messages from the interface ethically and compassionately
        panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'saveConfig':
                        // Update settings respecting user choices
                        for (const key in message.config) {
                            this.set(key, message.config[key], message.global);
                        }
                        
                        // Confirm save with love and gratitude
                        vscode.window.showInformationMessage(
                            '✧ EVA & GUARANI settings updated with love and awareness ✧'
                        );
                        break;
                        
                    case 'resetConfig':
                        // Restore default settings with universal redemption
                        this.config = {...DEFAULT_CONFIG};
                        this._saveLocalConfig();
                        
                        // Update interface
                        panel.webview.postMessage({ 
                            command: 'updateInterface', 
                            config: this.config 
                        });
                        
                        // Confirm reset with love and possibility of evolution
                        vscode.window.showInformationMessage(
                            '✧ EVA & GUARANI settings restored to original values ✧'
                        );
                        break;
                }
            },
            undefined
        );
    }
    
    /**
     * Generates artistic HTML for the configuration interface
     * @private
     * @returns {string} Interface HTML
     */
    _generateConfigHTML() {
        // Serialize settings safely
        const configJSON = JSON.stringify(this.config);
        
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EVA & GUARANI Configuration</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: #e0e0e0;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
                    padding: 2rem;
                    line-height: 1.6;
                }
                
                .header {
                    text-align: center;
                    margin-bottom: 2rem;
                }
                
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                    background: linear-gradient(45deg, #f5b041, #e74c3c, #8e44ad, #3498db);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                
                .subtitle {
                    font-style: italic;
                    color: #aaa;
                    margin-bottom: 2rem;
                }
                
                .tab-container {
                    margin: 2rem 0;
                }
                
                .tab-buttons {
                    display: flex;
                    overflow: auto;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }
                
                .tab-button {
                    background: none;
                    color: #aaa;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .tab-button:hover {
                    color: #fff;
                }
                
                .tab-button.active {
                    color: #e74c3c;
                    border-bottom: 2px solid #e74c3c;
                }
                
                .tab-content {
                    display: none;
                    padding: 1.5rem;
                    background-color: rgba(255, 255, 255, 0.05);
                    border-radius: 0 0 8px 8px;
                }
                
                .tab-content.active {
                    display: block;
                }
                
                .form-group {
                    margin-bottom: 1.5rem;
                }
                
                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    color: #9b59b6;
                }
                
                input[type="text"],
                input[type="number"],
                select {
                    width: 100%;
                    padding: 0.75rem;
                    background-color: rgba(0, 0, 0, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                    color: #e0e0e0;
                    font-size: 1rem;
                }
                
                input[type="checkbox"] {
                    margin-right: 0.5rem;
                }
                
                .checkbox-label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                }
                
                .actions {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 2rem;
                }
                
                button {
                    background-color: #8e44ad;
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }
                
                button:hover {
                    background-color: #9b59b6;
                    transform: translateY(-2px);
                }
                
                button.reset {
                    background-color: #e74c3c;
                }
                
                button.reset:hover {
                    background-color: #c0392b;
                }
                
                .scope-toggle {
                    display: flex;
                    justify-content: center;
                    margin: 1rem 0;
                    background-color: rgba(0, 0, 0, 0.2);
                    padding: 0.5rem;
                    border-radius: 4px;
                }
                
                .scope-button {
                    background: none;
                    border: none;
                    color: #aaa;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                }
                
                .scope-button.active {
                    background-color: #3498db;
                    color: white;
                }
                
                .signature {
                    font-family: 'Brush Script MT', cursive;
                    font-size: 1.5rem;
                    text-align: center;
                    margin-top: 2rem;
                    color: #e74c3c;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧</h1>
                <div class="subtitle">Quantum System Configuration</div>
            </div>
            
            <div class="scope-toggle">
                <button id="localScope" class="scope-button active">Project Configuration</button>
                <button id="globalScope" class="scope-button">Global Configuration</button>
            </div>
            
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button active" data-tab="general">General</button>
                    <button class="tab-button" data-tab="analysis">Analysis</button>
                    <button class="tab-button" data-tab="templates">Templates</button>
                    <button class="tab-button" data-tab="ai">Artificial Intelligence</button>
                    <button class="tab-button" data-tab="ethics">Ethics</button>
                    <button class="tab-button" data-tab="sync">Synchronization</button>
                </div>
                
                <div id="general" class="tab-content active">
                    <div class="form-group">
                        <div class="checkbox-label">
                            <input type="checkbox" id="enabled">
                            <label for="enabled">Enable EVA & GUARANI</label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <div class="checkbox-label">
                            <input type="checkbox" id="showWelcomeOnStartup">
                            <label for="showWelcomeOnStartup">Show welcome message on startup