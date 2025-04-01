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
 * EVA & GUARANI - VSCode Extension
 * =====================================
 * 
 * This extension implements the integration of the EVA & GUARANI system with VSCode,
 * allowing full use of the quantum knowledge base, modular analysis, and
 * systemic mapping in any project.
 * 
 * Incorporated principles:
 * - Ethics: Respect for the original intention and preservation of code integrity
 * - Love: Compassionate interface and supportive messages to the developer
 * - Economy: Efficient use of resources, minimizing unnecessary processing
 * - Art: Aesthetic visualizations and templates that integrate beauty and functionality
 * 
 * @context EVA_GUARANI_QUANTUM
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

// Standard VSCode dependencies
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

// Internal modules of the extension
const CONFIG = require('./config');
const TemplateManager = require('./template_manager');
const TerminologyGuard = require('./terminology_guard');
const ModularAnalyzer = require('./modular_analyzer');
const SystemMapper = require('./system_mapper');
const ArtisticVisualizer = require('./artistic_visualizer');
const EthicalAdvisor = require('./ethical_advisor');
const CloudSynchronizer = require('./cloud_synchronizer');
const AIRecommender = require('./ai_recommender');

/**
 * Main class of the VSCode extension for EVA & GUARANI
 * Implements the modular design pattern keeping each component
 * with a single responsibility.
 */
class EVAGuaraniVSCode {
    /**
     * Initializes the EVA & GUARANI extension for VSCode
     * @param {vscode.ExtensionContext} context - Extension context
     */
    constructor(context) {
        this.context = context;
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('evaguarani');
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        this.statusBarItem.text = "✧ EVA & GUARANI ✧";
        this.statusBarItem.tooltip = "EVA & GUARANI Quantum System active";
        this.statusBarItem.command = "evaguarani.showInfo";
        this.statusBarItem.show();
        
        this.config = new CONFIG.EVAGuaraniConfig();
        this.templateManager = new TemplateManager(context, this.config);
        this.terminologyGuard = new TerminologyGuard(this.diagnosticCollection, this.config);
        this.modularAnalyzer = new ModularAnalyzer(this.diagnosticCollection, this.config);
        this.systemMapper = new SystemMapper(context, this.config);
        this.artisticVisualizer = new ArtisticVisualizer(context, this.config);
        this.ethicalAdvisor = new EthicalAdvisor(this.config);
        this.cloudSynchronizer = new CloudSynchronizer(context, this.config);
        this.aiRecommender = new AIRecommender(context, this.config);
        
        // Initialize the system with love and ethics
        this._initialize();
        
        // Welcome message with love
        this._showWelcomeMessage();
    }
    
    /**
     * Initializes the components of the extension, setting up observers
     * and commands necessary for integration with VSCode.
     * @private
     */
    _initialize() {
        // Detect EVA & GUARANI project root directory
        this._detectProjectRoot();
        
        // Register observers
        this._registerEventListeners();
        
        // Register commands
        this._registerCommands();
        
        // Set up cloud synchronization (ethical and economical implementation)
        this.cloudSynchronizer.initialize();
        
        // Initial configuration of metrics (with economic awareness)
        this.modularAnalyzer.initializeMetrics();
        
        // Notify complete initialization
        console.log('EVA & GUARANI VSCode - System initialized with love and awareness');
    }
    
    /**
     * Detects the root directory of the EVA & GUARANI project
     * using an ethical and conscious search algorithm.
     * @private
     */
    _detectProjectRoot() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            console.log('No workspace open, using default configuration');
            return;
        }
        
        // Search for EVA & GUARANI project markers in directories
        for (const folder of workspaceFolders) {
            const folderPath = folder.uri.fsPath;
            
            // Check for marker files
            const documentationPath = path.join(folderPath, 'docs', 'DOCUMENTACAO_UNIFICADA.md');
            const readmePath = path.join(folderPath, 'README.md');
            
            if (fs.existsSync(documentationPath)) {
                this.config.setProjectRoot(folderPath);
                console.log(`EVA & GUARANI project found at ${folderPath} (via unified documentation)`);
                return;
            }
            
            if (fs.existsSync(readmePath)) {
                try {
                    const readmeContent = fs.readFileSync(readmePath, 'utf8');
                    if (readmeContent.includes('EVA & GUARANI')) {
                        this.config.setProjectRoot(folderPath);
                        console.log(`EVA & GUARANI project found at ${folderPath} (via README)`);
                        return;
                    }
                } catch (error) {
                    console.log(`Error reading README: ${error.message}`);
                }
            }
        }
        
        // Use the first workspace as fallback
        this.config.setProjectRoot(workspaceFolders[0].uri.fsPath);
        console.log(`Using ${workspaceFolders[0].uri.fsPath} as root directory (default)`);
    }
    
    /**
     * Registers event listeners to offer automatic functionalities
     * like template insertion and terminological verification.
     * @private
     */
    _registerEventListeners() {
        // Active text change observer (using resource-efficient approach)
        this.context.subscriptions.push(
            vscode.window.onDidChangeActiveTextEditor(editor => {
                if (editor && this.config.isEnabled()) {
                    // Check empty file to insert template
                    if (editor.document.getText().trim() === '') {
                        this.templateManager.checkAndInsertTemplate(editor);
                    }
                    
                    // Analyze terminology and modularity only when necessary (economy)
                    if (this.config.shouldAnalyzeFile(editor.document.uri.fsPath)) {
                        this.terminologyGuard.checkTerminology(editor.document);
                        this.modularAnalyzer.analyzeModularity(editor.document);
                    }
                }
            })
        );
        
        // Document change observer (optimized for economical resource use)
        let changeTimeout = null;
        this.context.subscriptions.push(
            vscode.workspace.onDidChangeTextDocument(event => {
                if (this.config.isEnabled()) {
                    // Use debounce to save resources
                    if (changeTimeout) {
                        clearTimeout(changeTimeout);
                    }
                    
                    changeTimeout = setTimeout(() => {
                        this.terminologyGuard.checkTerminology(event.document);
                        
                        // Update AI recommendations only when there are significant changes
                        if (event.contentChanges.length > 0 && 
                            event.contentChanges.some(change => change.text.length > 10)) {
                            this.aiRecommender.updateRecommendations(event.document);
                        }
                    }, 500); // Wait 500ms to save resources
                }
            })
        );
        
        // File save observer (for more intensive analyses)
        this.context.subscriptions.push(
            vscode.workspace.onDidSaveTextDocument(document => {
                if (this.config.isEnabled()) {
                    // Full analysis on save (saves resources by not doing it constantly)
                    this.modularAnalyzer.analyzeModularity(document);
                    
                    // Update system map after saving
                    this.systemMapper.updateFileInSystemMap(document);
                    
                    // Synchronize if necessary (with economic awareness)
                    if (this.config.shouldSyncOnSave()) {
                        this.cloudSynchronizer.syncFile(document.uri.fsPath);
                    }
                }
            })
        );
    }
    
    /**
     * Registers extension commands in VSCode to allow conscious interaction
     * with all functionalities of EVA & GUARANI.
     * @private
     */
    _registerCommands() {
        // Command to show system information
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.showInfo', () => {
                this._showSystemInfo();
            })
        );
        
        // Command to add quantum context to the current file
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.addQuantumContext', () => {
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    this.templateManager.addQuantumContextToFile(editor);
                }
            })
        );
        
        // Command to generate system map (cartography with artistic awareness)
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.generateSystemMap', () => {
                this.systemMapper.generateSystemMap();
                this.artisticVisualizer.visualizeSystemMap(this.systemMapper.getSystemMap());
            })
        );
        
        // Command for ethical code analysis
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.ethicalAnalysis', () => {
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    this.ethicalAdvisor.analyzeFile(editor.document);
                }
            })
        );
        
        // Command to configure the extension
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.configure', () => {
                this.config.showConfigurationUI();
            })
        );
        
        // Command to show AI recommendations
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.showRecommendations', () => {
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    this.aiRecommender.showRecommendations(editor.document);
                }
            })
        );
        
        // Command for cloud synchronization (with ethical security)
        this.context.subscriptions.push(
            vscode.commands.registerCommand('evaguarani.syncWithCloud', () => {
                this.cloudSynchronizer.syncAll();
            })
        );
    }
    
    /**
     * Shows a welcome message with love and ethical awareness.
     * @private
     */
    _showWelcomeMessage() {
        // Check if it's the first time the user opens the extension
        const hasShownWelcome = this.context.globalState.get('evaguarani.hasShownWelcome', false);
        
        if (!hasShownWelcome || this.config.shouldAlwaysShowWelcome()) {
            vscode.window.showInformationMessage(
                '✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n' +
                'Quantum System initialized with love and awareness.\n' +
                'Use the command "EVA & GUARANI: Show Information" to get started.',
                'Configure', 'View Documentation'
            ).then(selection => {
                if (selection === 'Configure') {
                    vscode.commands.executeCommand('evaguarani.configure');
                } else if (selection === 'View Documentation') {
                    // Open documentation with love and ethics
                    const docPath = path.join(this.config.getProjectRoot(), 'docs', 'DOCUMENTACAO_UNIFICADA.md');
                    if (fs.existsSync(docPath)) {
                        vscode.workspace.openTextDocument(docPath).then(doc => {
                            vscode.window.showTextDocument(doc);
                        });
                    } else {
                        vscode.window.showInformationMessage('Unified documentation not found in the current project.');
                    }
                }
            });
            
            // Register that the message has been shown
            this.context.globalState.update('evaguarani.hasShownWelcome', true);
        }
    }
    
    /**
     * Displays information about the EVA & GUARANI system in an artistic panel.
     * @private
     */
    _showSystemInfo() {
        // Create informative panel with art and love
        const panel = vscode.window.createWebviewPanel(
            'evaguaraniInfo',
            '✧ EVA & GUARANI ✧',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [
                    vscode.Uri.file(path.join(this.context.extensionPath, 'media'))
                ]
            }
        );
        
        // Generate artistic content with system information
        panel.webview.html = this._generateSystemInfoHTML();
        
        // Handle messages from the webview (with ethics and love)
        panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'openDocumentation':
                        const docPath = path.join(this.config.getProjectRoot(), 'docs', 'DOCUMENTACAO_UNIFICADA.md');
                        if (fs.existsSync(docPath)) {
                            vscode.workspace.openTextDocument(docPath).then(doc => {
                                vscode.window.showTextDocument(doc);
                            });
                        }
                        break;
                    case 'generateSystemMap':
                        vscode.commands.executeCommand('evaguarani.generateSystemMap');
                        break;
                    case 'showRecommendations':
                        vscode.commands.executeCommand('evaguarani.showRecommendations');
                        break;
                }
            },
            undefined,
            this.context.subscriptions
        );
    }
    
    /**
     * Generates artistic HTML for the system information panel.
     * @private
     * @returns {string} HTML of the information panel
     */
    _generateSystemInfoHTML() {
        // Include statistics and artistic visualizations
        return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EVA & GUARANI</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: #e0e0e0;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
                    padding: 2rem;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 0 auto;
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
                    background-size: 300% 300%;
                    animation: gradient-text 8s ease infinite;
                }
                
                @keyframes gradient-text {
                    0% { background-position: 0% 50% }
                    50% { background-position: 100% 50% }
                    100% { background-position: 0% 50% }
                }
                
                .subtitle {
                    font-style: italic;
                    color: #aaa;
                    margin-bottom: 2rem;
                }
                
                .section {
                    background-color: rgba(255, 255, 255, 0.05);
                    padding: 1.5rem;
                    border-radius: 8px;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    border-left: 4px solid #8e44ad;
                }
                
                h2 {
                    color: #9b59b6;
                    margin-top: 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    padding-bottom: 0.5rem;
                }
                
                .stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                    gap: 1rem;
                    margin-top: 1rem;
                }
                
                .stat-card {
                    background-color: rgba(0, 0, 0, 0.2);
                    padding: 1rem;
                    border-radius: 6px;
                    text-align: center;
                }
                
                .stat-value {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #3498db;
                    margin: 0.5rem 0;
                }
                
                .actions {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 1rem;
                    margin-top: 1.5rem;
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
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                
                .principles {
                    columns: 2;
                    column-gap: 2rem;
                    margin-top: 1rem;
                }
                
                .principle {
                    break-inside: avoid;
                    margin-bottom: 1rem;
                }
                
                .principle h3 {
                    color: #e74c3c;
                    margin-bottom: 0.25rem;
                }
                
                footer {
                    text-align: center;
                    margin-top: 2rem;
                    padding-top: 1rem;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    color: #aaa;
                }
                
                .signature {
                    font-family: 'Brush Script MT', cursive;
                    font-size: 1.5rem;
                    margin-top: 1rem;
                    color: #e74c3c;
                }
                
                .matrix {
                    background-color: rgba(0, 0, 0, 0.3);
                    padding: 1rem;
                    border-radius: 6px;
                    font-family: monospace;
                    margin-top: 1rem;
                    color: #2ecc71;
                    white-space: pre;
                }
                
                .progress-bar {
                    height: 6px;
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 3px;
                    overflow: hidden;
                    margin: 8px 0;
                }
                
                .progress-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #3498db, #9b59b6);
                    transition: width 0.5s ease;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧</h1>
                <div class="subtitle">Ethical Development Quantum System - VSCode Extension</div>
            </div>
            
            <div class="section">
                <h2>🌌 Quantum Consciousness Matrix</h2>