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
 * EVA & GUARANI - Filesystem Module Integration
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This file provides integration functions for the filesystem module.
 */

const fsModule = require('./index');

/**
 * Register the filesystem module with the SLOP server
 * @param {Object} slopServer - The SLOP server instance
 * @param {Object} options - Configuration options
 * @returns {Object} - Module instance
 */
function register(slopServer, options = {}) {
    const logger = slopServer.logger || console;

    logger.info('[Filesystem] Registering filesystem module with SLOP server');

    // Initialize the filesystem module
    const module = fsModule.initialize(options, {
        logger: logger
    });

    // Register routes
    const routes = module.routes;

    routes.forEach(route => {
        logger.debug(`[Filesystem] Registering route: ${route.method} ${route.path}`);

        // Add route to Express app
        slopServer.app[route.method.toLowerCase()](route.path, route.handler);
    });

    // Add module info endpoint
    slopServer.app.get('/filesystem/info', (req, res) => {
        const stats = module.stats();

        res.json({
            status: 'success',
            data: {
                name: module.name,
                version: module.version,
                stats: stats,
                routes: routes.map(r => ({
                    method: r.method,
                    path: r.path,
                    description: r.description
                })),
                config: {
                    allowedDirectories: options.allowedDirectories || [],
                    maxFileSize: options.maxFileSize || 0,
                    maxResults: options.maxResults || 0
                }
            }
        });
    });

    // Register WebSocket events if needed
    if (slopServer.wss) {
        slopServer.wss.on('connection', (ws) => {
            ws.on('message', (message) => {
                try {
                    const data = JSON.parse(message);

                    // Handle filesystem-specific messages
                    if (data.type === 'filesystem') {
                        switch (data.action) {
                            case 'stats':
                                ws.send(JSON.stringify({
                                    type: 'filesystem',
                                    action: 'stats',
                                    data: module.stats()
                                }));
                                break;

                            default:
                                ws.send(JSON.stringify({
                                    type: 'filesystem',
                                    action: 'error',
                                    error: 'Unknown action'
                                }));
                        }
                    }
                } catch (error) {
                    logger.error(`[Filesystem] WebSocket error: ${error.message}`);
                }
            });
        });
    }

    // Log registration completion
    logger.info('[Filesystem] Module successfully registered with SLOP server');

    return module;
}

module.exports = {
    register
};
