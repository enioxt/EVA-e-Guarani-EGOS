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
 * EVA & GUARANI - ATLAS (Systemic Cartography)
 * ===========================================
 *
 * This module exports the functionality of systemic cartography (ATLAS)
 * for the VSCode extension, enabling the visualization and analysis
 * of relationships between code components with ethical awareness.
 *
 * @context EVA_GUARANI_ATLAS
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

const AtlasAnalyzer = require('./atlas_analyzer');

/**
 * Activates the ATLAS subsystem
 * @param {vscode.ExtensionContext} context - Extension context
 * @param {Object} config - Global system configuration
 * @returns {Object} ATLAS subsystem interface
 */
function activate(context, config) {
    // Instantiate the cartography analyzer
    const atlasAnalyzer = new AtlasAnalyzer(context, config);

    // Register commands
    const commands = registerCommands(context, atlasAnalyzer);

    // Return public interface of the subsystem
    return {
        analyzer: atlasAnalyzer,
        commands: commands,

        // Direct access methods
        startCartography: (targetPath, options) => atlasAnalyzer.startCartography(targetPath, options),
        cancelCartography: () => atlasAnalyzer.cancelCartography(),
        getLatestResult: () => atlasAnalyzer.getLatestCartographyResult(),
        createVisualization: (resultId, options) => atlasAnalyzer.createVisualizationPanel(resultId, options),
        exportResult: (resultId, outputPath) => atlasAnalyzer.exportCartographyResult(resultId, outputPath)
    };
}

/**
 * Registers commands for the ATLAS subsystem
 * @param {vscode.ExtensionContext} context - Extension context
 * @param {AtlasAnalyzer} analyzer - Analyzer instance
 * @returns {Object} Registered commands
 */
function registerCommands(context, analyzer) {
    const vscode = require('vscode');
    const commands = {};

    // Command: Start cartography
    commands.startCartography = vscode.commands.registerCommand(
        'evaguarani.atlas.startCartography',
        async () => {
            try {
                // Obtain analysis target
                let targetPath = "";

                // If there is an open file, use it as target
                const activeEditor = vscode.window.activeTextEditor;
                if (activeEditor) {
                    targetPath = activeEditor.document.uri.fsPath;
                }
                // Otherwise, use root folder of the workspace
                else if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
                    targetPath = vscode.workspace.workspaceFolders[0].uri.fsPath;
                } else {
                    throw new Error("No open file or available workspace for analysis");
                }

                // Choose visualization type
                const visualizationType = await vscode.window.showQuickPick(
                    [
                        { label: "Dependency Graph", value: "dependency_graph" },
                        { label: "Complexity Heatmap", value: "complexity_heatmap" },
                        { label: "Data Flow", value: "data_flow" },
                        { label: "Module Constellation", value: "module_constellation" },
                        { label: "Evolution Timeline", value: "evolution_timeline" }
                    ],
                    { placeHolder: "Choose the type of cartographic visualization" }
                );

                if (!visualizationType) {
                    return; // User canceled
                }

                // Choose scope
                const scope = await vscode.window.showQuickPick(
                    [
                        { label: "File", value: "file" },
                        { label: "Module", value: "module" },
                        { label: "Project", value: "project" },
                        { label: "Workspace", value: "workspace" }
                    ],
                    { placeHolder: "Choose the scope of the analysis" }
                );

                if (!scope) {
                    return; // User canceled
                }

                // Show progress
                vscode.window.withProgress(
                    {
                        location: vscode.ProgressLocation.Notification,
                        title: "EVA & GUARANI: Systemic Cartography",
                        cancellable: true
                    },
                    async (progress, token) => {
                        // Progress callback
                        const progressCallback = (percent) => {
                            progress.report({
                                message: `Analyzing... ${percent}%`,
                                increment: null
                            });
                        };

                        // Cancellation
                        token.onCancellationRequested(() => {
                            analyzer.cancelCartography();
                        });

                        try {
                            // Start analysis
                            const result = await analyzer.startCartography(targetPath, {
                                visualizationType: visualizationType.value,
                                scope: scope.value,
                                progressCallback: progressCallback
                            });

                            // Ask if should show visualization
                            const showVisualization = await vscode.window.showInformationMessage(
                                "Cartography completed. Do you want to view the result?",
                                "Yes", "No"
                            );

                            if (showVisualization === "Yes") {
                                // Find ID of the most recent result
                                const resultIds = Array.from(analyzer.cartographyResults.keys());
                                const resultId = resultIds[resultIds.length - 1];

                                // Show visualization
                                analyzer.createVisualizationPanel(resultId);
                            }

                            return result;
                        } catch (error) {
                            vscode.window.showErrorMessage(`Cartography error: ${error.message}`);
                            throw error;
                        }
                    }
                );
            } catch (error) {
                vscode.window.showErrorMessage(`Error starting cartography: ${error.message}`);
            }
        }
    );

    // Command: Visualize latest result
    commands.visualizeLatestResult = vscode.commands.registerCommand(
        'evaguarani.atlas.visualizeLatestResult',
        () => {
            try {
                const latestResult = analyzer.getLatestCartographyResult();

                if (!latestResult) {
                    vscode.window.showInformationMessage("No cartography result available. Perform an analysis first.");
                    return;
                }

                // Find ID of the most recent result
                const resultIds = Array.from(analyzer.cartographyResults.keys());
                const resultId = resultIds[resultIds.length - 1];

                // Show visualization
                analyzer.createVisualizationPanel(resultId);
            } catch (error) {
                vscode.window.showErrorMessage(`Error visualizing result: ${error.message}`);
            }
        }
    );

    // Command: Export result
    commands.exportResult = vscode.commands.registerCommand(
        'evaguarani.atlas.exportResult',
        async () => {
            try {
                const latestResult = analyzer.getLatestCartographyResult();

                if (!latestResult) {
                    vscode.window.showInformationMessage("No cartography result available. Perform an analysis first.");
                    return;
                }

                // Find ID of the most recent result
                const resultIds = Array.from(analyzer.cartographyResults.keys());
                const resultId = resultIds[resultIds.length - 1];

                // Request save path
                const uri = await vscode.window.showSaveDialog({
                    defaultUri: vscode.Uri.file('cartography_result.json'),
                    filters: {
                        'JSON': ['json']
                    }
                });

                if (uri) {
                    // Export result
                    const outputPath = await analyzer.exportCartographyResult(resultId, uri.fsPath);
                    vscode.window.showInformationMessage(`Result exported to ${outputPath}`);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Error exporting result: ${error.message}`);
            }
        }
    );

    // Register the commands in the context
    context.subscriptions.push(commands.startCartography);
    context.subscriptions.push(commands.visualizeLatestResult);
    context.subscriptions.push(commands.exportResult);

    return commands;
}

module.exports = {
    activate
};
