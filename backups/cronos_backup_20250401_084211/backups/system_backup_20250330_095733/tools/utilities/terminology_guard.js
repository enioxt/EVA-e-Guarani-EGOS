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
 * EVA & GUARANI - Terminology Guard
 * =================================
 * 
 * This module monitors and validates terminological consistency in the code,
 * ensuring that important terms are used correctly and maintaining the conceptual coherence
 * of the EVA & GUARANI system.
 * 
 * Incorporated principles:
 * - Ethics: Suggested corrections with respect to the original intent
 * - Love: Constructive and educational feedback
 * - Economy: Efficient checks that do not impact performance
 * - Art: Clear and harmonious communication of suggestions
 * 
 * @context EVA_GUARANI_QUANTUM_TERMINOLOGY
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Standard terminology base of EVA & GUARANI
 * Organized by semantic categories for easy context and use.
 * @private
 */
const DEFAULT_TERMINOLOGY = {
    // Core concepts
    core: {
        // Preferred terms and their non-preferred synonyms or variations
        "modular analysis": ["module analysis", "analytical modulation"],
        "systemic cartography": ["systemic mapping", "system mapping"],
        "quantum ethics": ["system ethics", "computational ethics"],
        "evolutionary preservation": ["evolution preservation", "evolutionary backup"],
        "integrated consciousness": ["systemic consciousness", "conscious integration"],
        "unconditional love": ["code love", "loving development"],
        "compassionate temporality": ["compassionate time", "temporal compassion"],
        "universal possibility of redemption": ["universal redemption", "possibility of redemption"]
    },
    
    // Subsystems
    systems: {
        "ATLAS": ["atlas", "Atlas", "cartography system", "cartography"],
        "NEXUS": ["nexus", "Nexus", "analysis system", "analyzer"],
        "CRONOS": ["cronos", "Cronos", "preservation system", "preserver"]
    },
    
    // Technical aspects
    technical: {
        "quantum context": ["context", "code context"],
        "quantum matrix": ["matrix", "system matrix"],
        "exploratory mode": ["exploration mode", "exploration"],
        "analytical mode": ["analysis mode"],
        "integrative mode": ["integration mode", "integration"],
        "preservative mode": ["preservation mode"],
        "evolutionary mode": ["evolution mode"],
        "quantum mode": ["quantum mode", "quantum"]
    },
    
    // Metrics and indicators
    metrics: {
        "cartographic clarity": ["map clarity", "cartography clarity"],
        "modular quality": ["module quality", "module quality"],
        "backup integrity": ["preservation integrity", "saving integrity"],
        "systemic cohesion": ["system cohesion", "system cohesion"],
        "ethical evolution": ["ethical progress", "evolutionary ethics"],
        "expansion of connections": ["interconnections expansion", "connections increase"],
        "technical optimization": ["technical improvement", "technical enhancement"],
        "contextual preservation": ["contextual maintenance", "context permanence"]
    },
    
    // Processes and operations
    processes: {
        "cartograph": ["map system", "create map"],
        "analyze modularly": ["analyze modules", "perform modular analysis"],
        "preserve evolutionarily": ["preserve with evolution", "make evolutionary backup"],
        "integrate consciously": ["integrate with consciousness", "make conscious integration"],
        "evolve ethically": ["evolve with ethics", "develop ethically"],
        "visualize artistically": ["visualize with art", "create artistic visualization"]
    }
};

/**
 * Class responsible for monitoring and ensuring terminological
 * consistency in the code, with respect and educational approach.
 */
class TerminologyGuard {
    /**
     * Initializes the terminology guard
     * @param {vscode.DiagnosticCollection} diagnosticCollection - Collection for reporting diagnostics
     * @param {Object} config - EVA & GUARANI configuration
     */
    constructor(diagnosticCollection, config) {
        this.diagnosticCollection = diagnosticCollection;
        this.config = config;
        this.terminology = {...DEFAULT_TERMINOLOGY};
        
        // Inverse mapping for efficient search
        this.termMapping = this._buildTermMapping();
        
        // Load custom project terminology
        this._loadCustomTerminology();
    }
    
    /**
     * Builds inverse mapping of non-preferred terms to their
     * preferred equivalents, optimizing search.
     * @private
     * @returns {Map<string, {preferred: string, category: string}>} Inverse mapping
     */
    _buildTermMapping() {
        const mapping = new Map();
        
        // For each category in the terminology
        for (const category in this.terminology) {
            // For each preferred term in the category
            for (const preferred in this.terminology[category]) {
                // Add preferred term to mapping (pointing to itself)
                mapping.set(preferred.toLowerCase(), {
                    preferred: preferred,
                    category: category
                });
                
                // For each non-preferred synonym
                for (const nonPreferred of this.terminology[category][preferred]) {
                    // Add synonym to mapping (pointing to the preferred term)
                    mapping.set(nonPreferred.toLowerCase(), {
                        preferred: preferred,
                        category: category
                    });
                }
            }
        }
        
        return mapping;
    }
    
    /**
     * Loads custom project terminology
     * respecting autonomy and specific needs.
     * @private
     */
    _loadCustomTerminology() {
        const projectRoot = this.config.getProjectRoot();
        if (!projectRoot) return;
        
        const terminologyPath = path.join(projectRoot, '.evaguarani', 'terminology.json');
        
        if (fs.existsSync(terminologyPath)) {
            try {
                const customTerminology = JSON.parse(fs.readFileSync(terminologyPath, 'utf8'));
                
                // Merge with the default terminology
                for (const category in customTerminology) {
                    if (!this.terminology[category]) {
                        this.terminology[category] = {};
                    }
                    
                    // Add or overwrite terms
                    for (const preferred in customTerminology[category]) {
                        this.terminology[category][preferred] = customTerminology[category][preferred];
                    }
                }
                
                // Rebuild mapping
                this.termMapping = this._buildTermMapping();
                
                console.log('EVA & GUARANI: Custom terminology loaded with love and respect');
            } catch (error) {
                console.log(`EVA & GUARANI: Error loading custom terminology: ${error.message}`);
            }
        }
    }
    
    /**
     * Checks the terminology used in a document
     * @param {vscode.TextDocument} document - Document to be checked
     */
    checkTerminology(document) {
        // Check if enabled
        if (!this.config.isEnabled() || !this.config.get('enforceTerminology', true)) {
            this.diagnosticCollection.delete(document.uri);
            return;
        }
        
        // Check if we should analyze this file
        if (!this.config.shouldAnalyzeFile(document.uri.fsPath)) {
            this.diagnosticCollection.delete(document.uri);
            return;
        }
        
        // Get the configured severity
        const severity = this._getSeverity();
        
        // Start diagnostics array
        const diagnostics = [];
        
        // Get the full text of the document
        const text = document.getText();
        
        // Check each non-preferred term
        for (const [nonPreferred, info] of this.termMapping) {
            // Skip if it's the preferred term itself
            if (nonPreferred === info.preferred.toLowerCase()) {
                continue;
            }
            
            // Search for occurrences of the non-preferred term
            let searchIndex = 0;
            let match;
            
            // Regular expression to find the complete term (with word boundaries)
            const regex = new RegExp(`\\b${this._escapeRegex(nonPreferred)}\\b`, 'gi');
            
            // While finding occurrences
            while ((match = regex.exec(text)) !== null) {
                // Start and end position of the occurrence
                const startPos = document.positionAt(match.index);
                const endPos = document.positionAt(match.index + match[0].length);
                
                // Range of the occurrence
                const range = new vscode.Range(startPos, endPos);
                
                // Create diagnostic with educational message and suggestion
                const diagnostic = new vscode.Diagnostic(
                    range,
                    `Consider using "${info.preferred}" instead of "${match[0]}" to maintain terminological consistency.`,
                    severity
                );
                
                // Add code and source to the diagnostic
                diagnostic.code = 'evaguarani.terminology';
                diagnostic.source = 'EVA & GUARANI';
                
                // Add correction action
                diagnostic.relatedInformation = [
                    new vscode.DiagnosticRelatedInformation(
                        new vscode.Location(document.uri, range),
                        `"${info.preferred}" is the preferred term in the "${info.category}" category.`
                    )
                ];
                
                // Add to diagnostics array
                diagnostics.push(diagnostic);
            }
        }
        
        // Update diagnostics in the collection
        this.diagnosticCollection.set(document.uri, diagnostics);
    }
    
    /**
     * Gets the configured severity for terminology violations
     * @private
     * @returns {vscode.DiagnosticSeverity} Configured severity
     */
    _getSeverity() {
        const severityString = this.config.get('terminologyViolationSeverity', 'Warning');
        
        switch (severityString) {
            case 'Hint':
                return vscode.DiagnosticSeverity.Hint;
            case 'Information':
                return vscode.DiagnosticSeverity.Information;
            case 'Warning':
                return vscode.DiagnosticSeverity.Warning;
            case 'Error':
                return vscode.DiagnosticSeverity.Error;
            default:
                return vscode.DiagnosticSeverity.Information;
        }
    }
    
    /**
     * Escapes special characters in a string for use in a regular expression
     * @private
     * @param {string} string - String to be escaped
     * @returns {string} Escaped string
     */
    _escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    /**
     * Registers code action providers to correct terminology
     * @param {vscode.ExtensionContext} context - Extension context
     */
    registerCodeActions(context) {
        // Create code action provider
        const codeActionProvider = this._createCodeActionProvider();
        
        // Register for all language types
        const languageSelector = { pattern: '**/*.*' };
        
        // Add to subscription list
        context.subscriptions.push(
            vscode.languages.registerCodeActionsProvider(
                languageSelector,
                codeActionProvider,
                {
                    providedCodeActionKinds: [vscode.CodeActionKind.QuickFix]
                }
            )
        );
    }
    
    /**
     * Creates a code action provider to correct terminology
     * @private
     * @returns {vscode.CodeActionProvider} Code action provider
     */
    _createCodeActionProvider() {
        // Reference to the current object for use within the provider
        const self = this;
        
        // Return provider object
        return {
            provideCodeActions(document, range, context, token) {
                // Array of code actions
                const actions = [];
                
                // For each diagnostic in the context
                for (const diagnostic of context.diagnostics) {
                    // Check if it's a terminology diagnostic
                    if (diagnostic.code === 'evaguarani.terminology' && diagnostic.source === 'EVA & GUARANI') {
                        // Get the current text
                        const nonPreferredTerm = document.getText(diagnostic.range);
                        
                        // Find the corresponding preferred term
                        const preferredTerm = self._findPreferredTerm(nonPreferredTerm);
                        
                        if (preferredTerm) {
                            // Create correction action with love and education
                            const action = new vscode.CodeAction(
                                `Replace with "${preferredTerm}"`,
                                vscode.CodeActionKind.QuickFix
                            );
                            
                            // Configure text edit
                            action.edit = new vscode.WorkspaceEdit();
                            action.edit.replace(
                                document.uri,
                                diagnostic.range,
                                preferredTerm
                            );
                            
                            // Mark that this action fixes the diagnostic
                            action.diagnostics = [diagnostic];
                            action.isPreferred = true;
                            
                            // Add to actions list
                            actions.push(action);
                            
                            // Add action to ignore this occurrence
                            const ignoreAction = new vscode.CodeAction(
                                `Ignore this occurrence`,
                                vscode.CodeActionKind.QuickFix
                            );
                            ignoreAction.diagnostics = [diagnostic];
                            
                            // Add to actions list
                            actions.push(ignoreAction);
                        }
                    }
                }
                
                return actions;
            }
        };
    }
    
    /**
     * Finds the preferred term for a non-preferred term
     * @private
     * @param {string} nonPreferredTerm - Non-preferred term
     * @returns {string|null} Preferred term or null if not found
     */
    _findPreferredTerm(nonPreferredTerm) {
        const info = this.termMapping.get(nonPreferredTerm.toLowerCase());
        return info ? info.preferred : null;
    }
    
    /**
     * Exports the terminology to the project
     * Allows customization with respect to autonomy.
     */
    exportTerminologyToProject() {
        const projectRoot = this.config.getProjectRoot();
        if (!projectRoot) {
            vscode.window.showWarningMessage('No EVA & GUARANI project detected.');
            return;
        }
        
        // Create .evaguarani directory
        const configDir = path.join(projectRoot, '.evaguarani');
        
        try {
            if (!fs.existsSync(configDir)) {
                fs.mkdirSync(configDir, { recursive: true });
            }
            
            // Path to terminology file
            const terminologyPath = path.join(configDir, 'terminology.json');
            
            // Export terminology as JSON
            fs.writeFileSync(
                terminologyPath,
                JSON.stringify(this.terminology, null, 2),
                'utf8'
            );
            
            // Create explanatory README
            fs.writeFileSync(
                path.join(configDir, 'TERMINOLOGY.md'),
                `# EVA & GUARANI Terminology

This file documents the standard terminology used in the EVA & GUARANI system.
You can customize this terminology by editing the \`terminology.json\` file.

## Structure

The terminology is organized by semantic categories. In each category, preferred terms
are the keys, and the arrays contain non-preferred synonyms or variations.

## Categories

${Object.keys(this.terminology).map(category => {
    const termCount = Object.keys(this.terminology[category]).length;
    return `### ${category.charAt(0).toUpperCase() + category.slice(1)} (${termCount} terms)\n\nTerms related to ${category}.`;
}).join('\n\n')}

## Usage Example

\`\`\`json
{
  "core": {
    "modular analysis": ["module analysis", "analytical modulation"],
    "systemic cartography": ["systemic mapping", "system mapping"]
  }
}
\`\`\`

## Activation

The custom terminology will be automatically loaded when the EVA & GUARANI extension
is initialized in a project containing this file.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
`
            );
            
            vscode.window.showInformationMessage(
                'Terminology exported with love and consciousness. Now you can customize it!'
            );
            
        } catch (error) {
            console.log(`EVA & GUARANI: Error exporting terminology: ${error.message}`);
            vscode.window.showErrorMessage(
                `Error exporting terminology: ${error.message}`
            );
        }
    }
    
    /**
     * Checks terminology in all workspace files
     * with love and economic consciousness (optimized processing).
     */
    checkAllWorkspaceFiles() {
        // Check if enabled
        if (!this.config.isEnabled() || !this.config.get('enforceTerminology', true)) {
            return;
        }
        
        // Get workspace folders
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return;
        }
        
        // For each folder
        for (const folder of workspaceFolders) {
            // Create search pattern for files
            const pattern = new vscode.RelativePattern(folder, '**/*.*');
            
            // Find files
            vscode.workspace.findFiles(pattern).then(uris => {
                // For each file found (with economic consciousness)
                let processed = 0;
                const checkNextBatch = () => {
                    const batch = uris.slice(processed, processed + 10);
                    processed += 10;
                    
                    if (batch.length === 0) {
                        // All files have been processed
                        vscode.window.showInformationMessage(
                            `Terminology check completed with love and consciousness. ${uris.length} files processed.`
                        );
                        return;
                    }
                    
                    // Process this batch
                    Promise.all(batch.map(uri => {
                        // Check if we should analyze this file
                        if (!this.config.shouldAnalyzeFile(uri.fsPath)) {
                            return Promise.resolve();
                        }
                        
                        // Open document and check terminology
                        return vscode.workspace.openTextDocument(uri).then(document => {
                            this.checkTerminology(document);
                        }, error => {
                            console.log(`EVA & GUARANI: Error opening document ${uri.fsPath}: ${error.message}`);
                        });
                    })).then(() => {
                        // Continue with the next batch
                        setImmediate(checkNextBatch);
                    });
                };
                
                // Start processing in batches
                checkNextBatch();
            });
        }
    }
}

// Export class for integration with the EVA & GUARANI system
module.exports = TerminologyGuard;