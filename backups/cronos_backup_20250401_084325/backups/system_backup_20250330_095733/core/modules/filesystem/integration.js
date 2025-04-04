---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: modules
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
 * EVA & GUARANI - SLOP Filesystem Module Integration
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This file integrates the filesystem module with the SLOP server.
 */

const filesystemModule = require('./index');

/**
 * Register the filesystem module with the SLOP server
 * @param {Object} app - Express app instance
 * @param {Object} config - Application configuration
 * @param {Object} dependencies - Shared dependencies
 */
function register(app, config, dependencies) {
    // Extract required dependencies
    const { logger } = dependencies;

    logger.info('[SLOP] Registering filesystem module...');

    // Configure the filesystem module
    const fsConfig = {
        allowedDirectories: config.filesystem?.allowedDirectories || ['C:/Eva Guarani EGOS'],
        maxFileSize: config.filesystem?.maxFileSize || 10 * 1024 * 1024, // 10 MB
        maxResults: config.filesystem?.maxResults || 1000
    };

    // Initialize the filesystem module
    const filesystem = filesystemModule.initialize(fsConfig, {
        logger: logger.child({ module: 'filesystem' })
    });

    // Get routes from the filesystem module
    const routes = filesystem.routes;

    // Register all routes
    if (routes && Array.isArray(routes)) {
        routes.forEach(route => {
            const { method, path, handler, description } = route;

            if (method && path && handler) {
                const fullPath = `/api${path}`;

                logger.info(`[SLOP] Registering route: ${method.toUpperCase()} ${fullPath} - ${description || 'No description'}`);

                // Register the route with Express
                app[method.toLowerCase()](fullPath, (req, res) => {
                    // Log the request
                    logger.debug(`[SLOP][FS] ${method.toUpperCase()} ${fullPath}`, {
                        query: req.query,
                        body: req.body,
                        ip: req.ip
                    });

                    // Add request timestamp
                    req.requestTime = Date.now();

                    // Call the handler
                    return handler(req, res);
                });
            } else {
                logger.warn('[SLOP] Invalid route definition:', route);
            }
        });

        logger.info(`[SLOP] Filesystem module registered with ${routes.length} routes`);
    } else {
        logger.warn('[SLOP] No routes defined in filesystem module');
    }

    // Return the module interface for reference
    return {
        name: 'filesystem',
        version: filesystem.version,
        routes: routes.map(route => ({
            method: route.method,
            path: `/api${route.path}`,
            description: route.description
        }))
    };
}

module.exports = {
    register
};
