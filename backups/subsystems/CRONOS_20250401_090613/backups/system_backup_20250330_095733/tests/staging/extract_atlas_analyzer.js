---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: staging
  changelog: []
  dependencies:
  - ATLAS
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
  subsystem: ATLAS
  test_coverage: 0.9
  translation_status: completed
  type: javascript
  version: '8.0'
  windows_compatibility: true
---
/**
METADATA:
  type: module
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

# Important content extracted from core\atlas_pre_merge_20250320_082617\atlas_analyzer.js
# Original file moved to quarantine
# Date: 2025-03-22 08:37:20

javascript
/**
 * EVA & GUARANI - Systemic Cartography (ATLAS)
 * ==========================================
 * 
 * This module implements the systemic cartography system (ATLAS) for the VSCode extension,
 * allowing visualization and analysis of dependencies, relationships, and code structures,
 * identifying connections and architectural patterns with an ethical and artistic perspective.
 * 
 * Incorporated principles:
 * - Ethics: Respectful visualization that preserves the original architectural intent
 * - Love: Harmonious representations focused on system cohesion and beauty
 * - Economy: Efficient processing and optimized visualizations
 * - Art: Aesthetic representations of complex code structures
 * 
 * @context EVA_GUARANI_ATLAS
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Constants for visualization types
 * Define the different types of available visualizations
 * @private
 */
const VISUALIZATION_TYPES = {
    // Dependency map between files/modules
    DEPENDENCY_GRAPH: 'dependency_graph',
    
    // Complexity heatmap
    COMPLEXITY_HEATMAP: 'complexity_heatmap',
    
    // Data flow with ethical perspective
    DATA_FLOW: 'data_flow',
    
    // Constellation of related modules
    MODULE_CONSTELLATION: 'module_constellation',
    
    // Code evolution timeline
    EVOLUTION_TIMELINE: 'evolution_timeline'
};

/**
 * Constants for cartography scope
 * Define the scope of cartographic analysis
 * @private
 */
const CARTOGRAPHY_SCOPE = {
    FILE: 'file',           // Single file analysis
    MODULE: 'module',       // Module (directory) analysis
    PROJECT: 'project',     // Entire project analysis
    WORKSPACE: 'workspace'  // VSCode workspace analysis
};

/**
 * Default configuration for visualizations
 * Define styles, colors, and visual parameters
 * @private
 */
const DEFAULT_VISUALIZATION_CONFIG = {
    theme: 'quantum',
    node_size: 10,
    edge_width: 1.5,
    font_size: 8,
    colors: {
        node_default: '#6a54c0',     // Primary EVA & GUARANI color
        edge_default: '#8075ff',     // Secondary color
        highlight: '#ff5733',        // Highlight color
        background: '#f9f8ff',       // Soft background
        ethical_concern: '#f44336',  // Red for ethical concerns
        ethical_positive: '#4caf50', // Green for positive ethical aspects
        technical_debt: '#ff9800',   // Orange for technical debt
        complexity: '#9c27b0'        // Purple for complexity
    },
    // Detail level of visualization (1-5)
    detail_level: 3,
    // Whether to include ethical metrics in visualizations
    include_ethical_metrics: true,
    // Whether to highlight improvement points
    highlight_improvements: true
};

/**
 * AtlasAnalyzer Class
 * Implements the ATLAS subsystem of systemic cartography with ethical awareness,
 * allowing visualization of structures, dependencies, and flows in the code.
 */
class AtlasAnalyzer {
    /**
     * Initializes the cartographic analyzer
     * @param {vscode.ExtensionContext} context - Extension context
     * @param {Object} config - EVA & GUARANI configuration
     */
    constructor(context, config) {
        this.context = context;
        this.config = config;
        
        // Configuration for visualizations
        this.visualizationConfig = { 
            ...DEFAULT_VISUALIZATION_CONFIG,
            ...this._loadCustomVisualizationConfig()
        };
        
        // Current status of cartographic analysis
        this.analyzing = false;
        this.progress = 0;
        this.lastAnalysisTime = null;
        
        // Storage of cartography results
        this.cartographyResults = new Map();
        
        // WebView panel for current visualization
        this.visualizationPanel = null;
        
        // Dependencies from other EVA & GUARANI modules
        this.nexusAnalyzer = null; // Will be defined after integration with NEXUS
    }
    
    /**
     * Loads custom configuration for visualizations
     * @private
     * @returns {Object} Custom configuration
     */
    _loadCustomVisualizationConfig() {
        try {
            // Attempt to load custom configuration from workspace
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders && workspaceFolders.length > 0) {
                const configPath = path.join(
                    workspaceFolders[0].uri.fsPath,
                    '.evaguarani',
                    'atlas_config.json'
                );
                
                if (fs.existsSync(configPath)) {
                    const configContent = fs.readFileSync(configPath, 'utf8');
                    const customConfig = JSON.parse(configContent);
                    return customConfig.visualization || {};
                }
            }
        } catch (error) {
            console.error('EVA & GUARANI: Error loading custom configuration:', error);
        }
        
        return {};
    }
    
    /**
     * Starts a cartographic analysis
     * @param {string} targetPath - Path of the file or directory to be analyzed
     * @param {Object} options - Analysis options
     * @param {string} options.visualizationType - Visualization type (default: VISUALIZATION_TYPES.DEPENDENCY_GRAPH)
     * @param {string} options.scope - Analysis scope (default: CARTOGRAPHY_SCOPE.FILE)
     * @param {boolean} options.includeNodeModules - Whether to include node_modules (default: false)
     * @param {Function} options.progressCallback - Callback for progress update
     * @returns {Promise<Object>} Result of the cartographic analysis
     */
    async startCartography(targetPath, options = {}) {
        // Check if there is already an ongoing analysis
        if (this.analyzing) {
            throw new Error('A cartographic analysis is already in progress. Please wait or cancel the current analysis.');
        }
        
        // Define default options
        const defaultOptions = {
            visualizationType: VISUALIZATION_TYPES.DEPENDENCY_GRAPH,
            scope: CARTOGRAPHY_SCOPE.FILE,
            includeNodeModules: false,
            progressCallback: null
        };
        
        // Merge options
        const cartographyOptions = {...defaultOptions, ...options};
        
        // Check if the target exists
        if (!fs.existsSync(targetPath)) {
            throw new Error(`Path not found: ${targetPath}`);
        }
        
        // Update status
        this.analyzing = true;
        this.progress = 0;
        
        // Record start time
        const startTime = Date.now();
        
        try {
            // Notify start of analysis
            vscode.window.showInformationMessage(
                `EVA & GUARANI: Starting systemic cartography with love and awareness.`
            );
            
            // Create initial result
            const result = {
                targetPath,
                visualizationType: cartographyOptions.visualizationType,
                scope: cartographyOptions.scope,
                timestamp: startTime,
                nodes: [],
                edges: [],
                metrics: {},
                ethicalFindings: []
            };
            
            // Execute analysis based on visualization type
            switch (cartographyOptions.visualizationType) {
                case VISUALIZATION_TYPES.DEPENDENCY_GRAPH:
                    await this._analyzeDependencies(targetPath, cartographyOptions, result);
                    break;
                    
                case VISUALIZATION_TYPES.COMPLEXITY_HEATMAP:
                    await this._analyzeComplexity(targetPath, cartographyOptions, result);
                    break;
                    
                case VISUALIZATION_TYPES.DATA_FLOW:
                    await this._analyzeDataFlow(targetPath, cartographyOptions, result);
                    break;
                    
                case VISUALIZATION_TYPES.MODULE_CONSTELLATION:
                    await this._analyzeModuleConstellation(targetPath, cartographyOptions, result);
                    break;
                    
                case VISUALIZATION_TYPES.EVOLUTION_TIMELINE:
                    await this._analyzeEvolution(targetPath, cartographyOptions, result);
                    break;
                    
                default:
                    throw new Error(`Invalid visualization type: ${cartographyOptions.visualizationType}`);
            }
            
            // Calculate ethical metrics
            await this._calculateEthicalMetrics(result);
            
            // Calculate duration
            const duration = Date.now() - startTime;
            result.duration = duration;
            
            // Store results
            const resultKey = `${targetPath}_${cartographyOptions.visualizationType}_${new Date().toISOString()}`;
            this.cartographyResults.set(resultKey, result);
            this.lastAnalysisTime = new Date();
            
            // Notify completion
            vscode.window.showInformationMessage(
                `EVA & GUARANI: Systemic cartography completed with love and awareness (${duration}ms).`
            );
            
            return result;
        } catch (error) {
            vscode.window.showErrorMessage(
                `EVA & GUARANI: Error during systemic cartography: ${error.message}`
            );
            
            throw error;
        } finally {
            // Update status
            this.analyzing = false;
            this.progress = 100;
        }
    }
    
    /**
     * Cancels the ongoing cartographic analysis
     * @returns {boolean} Whether the analysis was successfully canceled
     */
    cancelCartography() {
        if (!this.analyzing) {
            return false;
        }
        
        // Update status
        this.analyzing = false;
        
        // Notify cancellation
        vscode.window.showInformationMessage(
            `EVA & GUARANI: Systemic cartography canceled with respect.`
        );
        
        return true;
    }
    
    /**
     * Gets the most recent cartography result
     * @returns {Object|null} Most recent result or null if none available
     */
    getLatestCartographyResult() {
        if (this.cartographyResults.size === 0) {
            return null;
        }
        
        // Find the most recent result
        let latestResult = null;
        let latestTimestamp = 0;
        
        for (const [key, result] of this.cartographyResults) {
            const timestamp = result.timestamp;
            
            if (timestamp > latestTimestamp) {
                latestTimestamp = timestamp;
                latestResult = result;
            }
        }
        
        return latestResult;
    }
    
    /**
     * Collects files recursively from a directory
     * @private
     * @param {string} directory - Directory to collect files from
     * @param {string[]} filesList - List of files to populate
     * @param {number} depth - Maximum recursion depth (Infinity for unlimited)
     * @param {boolean} includeNodeModules - Whether to include node_modules
     * @returns {Promise<void>}
     */
    async _collectFiles(directory, filesList, depth = Infinity, includeNodeModules = false) {
        if (depth < 0) {
            return;
        }
        
        try {
            const files = fs.readdirSync(directory);
            
            for (const file of files) {
                const filePath = path.join(directory, file);
                
                // Skip node_modules unless explicitly included
                if (file === 'node_modules' && !includeNodeModules) {
                    continue;
                }
                
                // Skip hidden directories
                if (file.startsWith('.')) {
                    continue;
                }
                
                const stats = fs.statSync(filePath);
                
                if (stats.isDirectory()) {
                    // Recurse into subdirectories with reduced depth
                    await this._collectFiles(filePath, filesList, depth - 1, includeNodeModules);
                } else if (this._isCodeFile(filePath)) {
                    filesList.push(filePath);
                }
            }
        } catch (error) {
            console.error(`Error accessing directory ${directory}:`, error);
        }
    }
    
    /**
     * Completes the dependency analysis
     * @private
     * @param {string} targetPath - Target path of the analysis
     * @param {Object} options - Analysis options
     * @returns {Promise<Object>} Analysis result
     */
    async _analyzeDependencies(targetPath, options, result) {
        // Check if it's a file or directory
        const stats = fs.statSync(targetPath);
        
        // Identify files for analysis
        const filesToAnalyze = [];
        
        if (stats.isFile()) {
            filesToAnalyze.push(targetPath);
        } else if (stats.isDirectory()) {
            // Collect files recursively based on scope
            const depth = options.scope === CARTOGRAPHY_SCOPE.PROJECT ? Infinity : 
                        options.scope === CARTOGRAPHY_SCOPE.MODULE ? 2 : 1;
            
            await this._collectFiles(targetPath, filesToAnalyze, depth, options.includeNodeModules);
        }
        
        // Dependency map: file -> [dependencies]
        const dependencies = new Map();
        const fileNodes = new Map(); // file -> node id
        let nodeCounter = 0;
        
        // Analyze each file
        for (let i = 0; i < filesToAnalyze.length; i++) {
            const filePath = filesToAnalyze[i];
            
            // Update progress
            this._updateProgress(options, i, filesToAnalyze.length);
            
            // Read file content
            try {
                const content = fs.readFileSync(filePath, 'utf8');
                const fileImports = this._extractImports(filePath, content);
                
                dependencies.set(filePath, fileImports);
                
                // Create node for this file if it doesn't exist
                if (!fileNodes.has(filePath)) {
                    const nodeId = `node_${nodeCounter++}`;
                    fileNodes.set(filePath, nodeId);
                    result.nodes.push(this._createFileNode(filePath, nodeId));
                }
                
                // Create nodes for each import
                for (const importPath of fileImports) {
                    if (!fileNodes.has(importPath)) {
                        const nodeId = `node_${nodeCounter++}`;
                        fileNodes.set(importPath, nodeId);
                        result.nodes.push(this._createFileNode(importPath, nodeId));
                    }
                }
            } catch (error) {
                console.error(`Error analyzing file ${filePath}:`, error);
            }
        }
        
        // Create edges to represent dependencies
        for (const [file, imports] of dependencies) {
            const sourceId = fileNodes.get(file);
            
            for (const importPath of imports) {
                const targetId = fileNodes.get(importPath);
                
                if (sourceId && targetId) {
                    result.edges.push({
                        id: `edge_${sourceId}_${targetId}`,
                        source: sourceId,
                        target: targetId,
                        type: 'dependency'
                    });
                }
            }
        }
        
        // Calculate metrics for the dependency network
        this._calculateDependencyMetrics(dependencies, result);
        
        return result;
    }
    
    /**
     * Checks if a file is a code file
     * @private
     * @param {string} filePath - File path
     * @returns {boolean} Whether it is a code file
     */
    _isCodeFile(filePath) {
        const ext = path.extname(filePath).toLowerCase();
        const codeExtensions = [
            '.js', '.jsx', '.ts', '.tsx', '.py', 
            '.java', '.c', '.cpp', '.cs', '.go', 
            '.rb', '.php', '.html', '.css', '.vue',
            '.json', '.md', '.yaml', '.yml'
        ];
        
        return codeExtensions.includes(ext);
    }
    
    /**
     * Extracts imports from a file
     * @private
     * @param {string} filePath - File path
     * @param {string} content - File content
     * @returns {string[]} List of imported file paths
     */
    _extractImports(filePath, content) {
        const imports = [];
        const ext = path.extname(filePath).toLowerCase();
        const fileDir = path.dirname(filePath);
        
        // Import patterns for different languages
        let importPatterns = [];
        
        // JavaScript / TypeScript
        if (['.js', '.jsx', '.ts', '.tsx'].includes(ext)) {
            importPatterns = [
                // ES modules: import ... from '...'
                { regex: /import\s+.+\s+from\s+['"]([^'"]+)['"]/g, group: 1 },
                // CommonJS: require('...')
                { regex: /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g, group: 1 },
                // Dynamic import: import('...')
                { regex: /import\s*\(\s*['"]([^'"]+)['"]\s*\)/g, group: 1 }
            ];
        }
        // Python
        else if (ext === '.py') {
            importPatterns = [
                // import module
                { regex: /import\s+([a-zA-Z0-9_.]+)/g, group: 1 },
                // from module import ...
                { regex: /from\s+([a-zA-Z0-9_.]+)\s+import/g, group: 1 }
            ];
        }
        // Java
        else if (ext === '.java') {
            importPatterns = [
                // import package.Class
                { regex: /import\s+([a-zA-Z0-9_.]+);/g, group: 1 }
            ];
        }
        
        // Extract imports based on patterns
        for (const pattern of importPatterns) {
            let match;
            while ((match = pattern.regex.exec(content)) !== null) {
                const importPath = match[pattern.group];
                
                // Resolve module/file path
                const resolvedPath = this._resolveImportPath(importPath, filePath, ext);
                if (resolvedPath) {
                    imports.push(resolvedPath);
                }
            }
        }
        
        return imports;
    }
    
    /**
     * Resolves the path of an import to an absolute file path
     * @private
     * @param {string} importPath - Import path
     * @param {string} currentFilePath - Current file path
     * @param {string} fileExt - Current file extension
     * @returns {string|null} Resolved absolute path or null if unable to resolve
     */
    _resolveImportPath(importPath, currentFilePath, fileExt) {
        const currentDir = path.dirname(currentFilePath);
        
        // JavaScript/TypeScript: resolve relative path
        if (['.js', '.jsx', '.ts', '.tsx'].includes(fileExt)) {
            if (importPath.startsWith('.')) {
                // Relative path, add extension if necessary
                let resolvedPath = path.resolve(currentDir, importPath);
                
                // Check if path exists with extension
                if (fs.existsSync(resolvedPath)) {
                    return resolvedPath;
                }
                
                // Try adding common extensions
                const extensions = ['.js', '.jsx', '.

# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
