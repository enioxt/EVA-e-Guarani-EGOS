---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: slop
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

/**
 * EVA & GUARANI - Filesystem Module Integration for SLOP Server
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This file integrates the Filesystem Module with the main SLOP server.
 */

const path = require('path');
const fs = require('fs');

// Define paths
const BASE_PATH = path.resolve(__dirname, '..');
const LOGS_PATH = path.resolve(BASE_PATH, '..', 'logs', 'slop');
const MODULE_PATH = path.resolve(__dirname, 'modules', 'filesystem');
const ALLOWED_DIRS = [
    path.resolve(BASE_PATH, '..'), // Eva Guarani EGOS root
    path.resolve(BASE_PATH),       // QUANTUM_PROMPTS
    path.resolve(BASE_PATH, '..', 'logs') // Logs directory
];

// Ensure logs directory exists
if (!fs.existsSync(LOGS_PATH)) {
    fs.mkdirSync(LOGS_PATH, { recursive: true });
}

/**
 * Register the filesystem module with the SLOP server
 * @param {Object} slopServer - The SLOP server instance
 */
function registerFilesystemModule(slopServer) {
    try {
        // Log the integration
        slopServer.logger.info('[SLOP] Initializing filesystem module integration');

        // Verify module files exist
        if (!fs.existsSync(MODULE_PATH)) {
            slopServer.logger.error(`[SLOP] Filesystem module not found at ${MODULE_PATH}`);
            return false;
        }

        // Import the integration module
        const filesystemIntegration = require(path.join(MODULE_PATH, 'integration'));

        // Register the module
        const fsModule = filesystemIntegration.register(slopServer, {
            allowedDirectories: ALLOWED_DIRS,
            maxFileSize: 20 * 1024 * 1024, // 20MB limit
            maxResults: 1000,
            logLevel: slopServer.config.logLevel || 'info'
        });

        slopServer.logger.info('[SLOP] Filesystem module integration complete');
        slopServer.logger.info(`[SLOP] Allowed directories: ${ALLOWED_DIRS.join(', ')}`);

        // Add a reference to the filesystem module in the SLOP server state
        slopServer.state = slopServer.state || {};
        slopServer.state.filesystemModule = {
            name: fsModule.name,
            version: fsModule.version,
            allowedDirectories: ALLOWED_DIRS,
            timestamp: new Date().toISOString()
        };

        // Return success
        return true;
    } catch (error) {
        if (slopServer.logger) {
            slopServer.logger.error(`[SLOP] Failed to register filesystem module: ${error.message}`);
            slopServer.logger.error(error.stack);
        } else {
            console.error(`[SLOP] Failed to register filesystem module: ${error.message}`);
            console.error(error.stack);
        }
        return false;
    }
}

// Export the registration function
module.exports = {
    register: registerFilesystemModule
};
