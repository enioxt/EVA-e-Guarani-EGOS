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
 * EVA & GUARANI - Filesystem Module for SLOP Server
 * Version: 1.0.0
 * Date: 2025-03-29
 * 
 * This module provides filesystem operations for the SLOP server.
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

// Default configuration
const DEFAULT_CONFIG = {
    allowedDirectories: [
        'C:/Eva Guarani EGOS'
    ],
    maxFileSize: 10 * 1024 * 1024, // 10MB
    maxResults: 1000,
    logLevel: 'info'
};

// Module state
let state = {
    config: { ...DEFAULT_CONFIG },
    logger: console,
    initialized: false,
    stats: {
        reads: 0,
        writes: 0,
        deletes: 0,
        lists: 0,
        searches: 0,
        errors: 0,
        lastOperation: null
    }
};

/**
 * Initialize the filesystem module
 * @param {Object} options - Configuration options
 * @param {Object} dependencies - Module dependencies
 * @returns {Object} - Module API
 */
function initialize(options = {}, dependencies = {}) {
    // Merge configuration
    state.config = {
        ...DEFAULT_CONFIG,
        ...options
    };

    // Set logger
    state.logger = dependencies.logger || console;

    // Mark as initialized
    state.initialized = true;

    state.logger.info(`[Filesystem] Module initialized with ${state.config.allowedDirectories.length} allowed directories`);

    return {
        name: 'filesystem',
        version: '1.0.0',
        routes: getRoutes(),
        stats: getStats,
        isPathAllowed: isPathAllowed
    };
}

/**
 * Get module routes
 * @returns {Array} - Array of route configurations
 */
function getRoutes() {
    return [
        {
            method: 'GET',
            path: '/filesystem/read',
            handler: readFile,
            description: 'Read file contents'
        },
        {
            method: 'POST',
            path: '/filesystem/write',
            handler: writeFile,
            description: 'Write content to a file'
        },
        {
            method: 'GET',
            path: '/filesystem/list',
            handler: listDirectory,
            description: 'List directory contents'
        },
        {
            method: 'GET',
            path: '/filesystem/search',
            handler: searchFiles,
            description: 'Search for files'
        },
        {
            method: 'DELETE',
            path: '/filesystem/delete',
            handler: deleteFile,
            description: 'Delete a file or directory'
        }
    ];
}

/**
 * Get module statistics
 * @returns {Object} - Module statistics
 */
function getStats() {
    return { ...state.stats };
}

/**
 * Check if a path is allowed
 * @param {string} targetPath - The path to check
 * @returns {boolean} - Whether the path is allowed
 */
function isPathAllowed(targetPath) {
    const normalizedPath = path.normalize(targetPath);

    return state.config.allowedDirectories.some(allowedDir => {
        const normalizedAllowedDir = path.normalize(allowedDir);
        return normalizedPath.startsWith(normalizedAllowedDir);
    });
}

/**
 * Generate a unique ID for a file
 * @param {string} filePath - The file path
 * @returns {string} - Unique file ID
 */
function generateFileId(filePath) {
    return crypto
        .createHash('md5')
        .update(path.normalize(filePath))
        .digest('hex');
}

/**
 * Read a file from the filesystem
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function readFile(req, res) {
    try {
        const filePath = req.query.path;

        if (!filePath) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required parameter: path'
            });
        }

        // Check if path is allowed
        if (!isPathAllowed(filePath)) {
            state.logger.warn(`[Filesystem] Attempted to read unauthorized path: ${filePath}`);
            state.stats.errors++;

            return res.status(403).json({
                status: 'error',
                message: 'Access to this path is not allowed'
            });
        }

        // Check if file exists
        const stats = await fs.stat(filePath);

        if (!stats.isFile()) {
            state.logger.warn(`[Filesystem] Attempted to read a non-file: ${filePath}`);
            state.stats.errors++;

            return res.status(400).json({
                status: 'error',
                message: 'The specified path is not a file'
            });
        }

        // Check file size
        if (stats.size > state.config.maxFileSize) {
            state.logger.warn(`[Filesystem] File too large: ${filePath} (${stats.size} bytes)`);
            state.stats.errors++;

            return res.status(400).json({
                status: 'error',
                message: `File size exceeds the maximum allowed size (${state.config.maxFileSize} bytes)`
            });
        }

        // Read file content
        const content = await fs.readFile(filePath, 'utf8');

        // Update stats
        state.stats.reads++;
        state.stats.lastOperation = {
            type: 'read',
            path: filePath,
            timestamp: new Date().toISOString()
        };

        state.logger.debug(`[Filesystem] Read file: ${filePath} (${content.length} bytes)`);

        // Return successful response
        res.status(200).json({
            status: 'success',
            message: 'File read successfully',
            data: {
                path: filePath,
                content,
                fileId: generateFileId(filePath),
                stats: {
                    size: stats.size,
                    created: stats.birthtime,
                    modified: stats.mtime,
                    accessed: stats.atime
                }
            }
        });
    } catch (error) {
        state.stats.errors++;
        state.logger.error(`[Filesystem] Error reading file: ${error.message}`);

        // Return error response
        res.status(500).json({
            status: 'error',
            message: `Error reading file: ${error.message}`
        });
    }
}

/**
 * Write content to a file
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function writeFile(req, res) {
    try {
        const { path: filePath, content, createDirectories } = req.body;

        if (!filePath || content === undefined) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required parameters: path and content'
            });
        }

        // Check if path is allowed
        if (!isPathAllowed(filePath)) {
            state.logger.warn(`[Filesystem] Attempted to write to unauthorized path: ${filePath}`);
            state.stats.errors++;

            return res.status(403).json({
                status: 'error',
                message: 'Access to this path is not allowed'
            });
        }

        // Check content size
        if (Buffer.byteLength(content, 'utf8') > state.config.maxFileSize) {
            state.logger.warn(`[Filesystem] Content too large for file: ${filePath}`);
            state.stats.errors++;

            return res.status(400).json({
                status: 'error',
                message: `Content size exceeds the maximum allowed size (${state.config.maxFileSize} bytes)`
            });
        }

        // Create directory if it doesn't exist and createDirectories is true
        if (createDirectories) {
            const directory = path.dirname(filePath);
            await fs.mkdir(directory, { recursive: true });
        }

        // Write content to file
        await fs.writeFile(filePath, content, 'utf8');

        // Get file stats
        const stats = await fs.stat(filePath);

        // Update stats
        state.stats.writes++;
        state.stats.lastOperation = {
            type: 'write',
            path: filePath,
            timestamp: new Date().toISOString()
        };

        state.logger.debug(`[Filesystem] Wrote to file: ${filePath} (${Buffer.byteLength(content, 'utf8')} bytes)`);

        // Return successful response
        res.status(200).json({
            status: 'success',
            message: 'File written successfully',
            data: {
                path: filePath,
                fileId: generateFileId(filePath),
                stats: {
                    size: stats.size,
                    created: stats.birthtime,
                    modified: stats.mtime
                }
            }
        });
    } catch (error) {
        state.stats.errors++;
        state.logger.error(`[Filesystem] Error writing file: ${error.message}`);

        // Return error response
        res.status(500).json({
            status: 'error',
            message: `Error writing file: ${error.message}`
        });
    }
}

/**
 * List directory contents
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function listDirectory(req, res) {
    try {
        const { path: dirPath, recursive, pattern } = req.query;

        if (!dirPath) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required parameter: path'
            });
        }

        // Check if path is allowed
        if (!isPathAllowed(dirPath)) {
            state.logger.warn(`[Filesystem] Attempted to list unauthorized directory: ${dirPath}`);
            state.stats.errors++;

            return res.status(403).json({
                status: 'error',
                message: 'Access to this path is not allowed'
            });
        }

        // Read directory
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        // Process entries
        const files = [];
        const directories = [];

        for (const entry of entries) {
            const entryPath = path.join(dirPath, entry.name);

            // Skip if pattern is provided and doesn't match
            if (pattern && !entry.name.match(new RegExp(pattern))) {
                continue;
            }

            if (entry.isDirectory()) {
                directories.push({
                    name: entry.name,
                    path: entryPath,
                    type: 'directory'
                });

                // Process subdirectories if recursive is true
                if (recursive === 'true') {
                    const subDirResult = await listDirectory({
                        query: {
                            path: entryPath,
                            recursive: 'true',
                            pattern
                        }
                    }, { json: () => { } });

                    if (subDirResult.data) {
                        directories[directories.length - 1].children = {
                            files: subDirResult.data.files,
                            directories: subDirResult.data.directories
                        };
                    }
                }
            } else if (entry.isFile()) {
                const stats = await fs.stat(entryPath);

                files.push({
                    name: entry.name,
                    path: entryPath,
                    type: 'file',
                    fileId: generateFileId(entryPath),
                    size: stats.size,
                    created: stats.birthtime,
                    modified: stats.mtime
                });
            }
        }

        // Update stats
        state.stats.lists++;
        state.stats.lastOperation = {
            type: 'list',
            path: dirPath,
            timestamp: new Date().toISOString()
        };

        state.logger.debug(`[Filesystem] Listed directory: ${dirPath} (${files.length} files, ${directories.length} dirs)`);

        // Return successful response
        res.status(200).json({
            status: 'success',
            message: 'Directory listed successfully',
            data: {
                path: dirPath,
                files,
                directories,
                totalCount: files.length + directories.length
            }
        });
    } catch (error) {
        state.stats.errors++;
        state.logger.error(`[Filesystem] Error listing directory: ${error.message}`);

        // Return error response
        res.status(500).json({
            status: 'error',
            message: `Error listing directory: ${error.message}`
        });
    }
}

/**
 * Search for files
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function searchFiles(req, res) {
    try {
        const { path: startPath, query, recursive, limit } = req.query;

        if (!startPath || !query) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required parameters: path and query'
            });
        }

        // Check if path is allowed
        if (!isPathAllowed(startPath)) {
            state.logger.warn(`[Filesystem] Attempted to search in unauthorized directory: ${startPath}`);
            state.stats.errors++;

            return res.status(403).json({
                status: 'error',
                message: 'Access to this path is not allowed'
            });
        }

        // Set limit
        const maxResults = limit ? parseInt(limit, 10) : state.config.maxResults;

        // Results
        const results = {
            matchesByName: [],
            matchesByContent: []
        };

        // Search function
        async function searchInDirectory(dirPath) {
            // Stop if we've reached the limit
            if (
                results.matchesByName.length + results.matchesByContent.length >= maxResults
            ) {
                return;
            }

            // Read directory
            const entries = await fs.readdir(dirPath, { withFileTypes: true });

            // Process entries
            for (const entry of entries) {
                // Stop if we've reached the limit
                if (
                    results.matchesByName.length + results.matchesByContent.length >= maxResults
                ) {
                    break;
                }

                const entryPath = path.join(dirPath, entry.name);

                if (entry.isDirectory() && recursive === 'true') {
                    // Process subdirectory
                    await searchInDirectory(entryPath);
                } else if (entry.isFile()) {
                    // Check filename
                    if (entry.name.toLowerCase().includes(query.toLowerCase())) {
                        const stats = await fs.stat(entryPath);

                        results.matchesByName.push({
                            name: entry.name,
                            path: entryPath,
                            type: 'file',
                            fileId: generateFileId(entryPath),
                            size: stats.size,
                            created: stats.birthtime,
                            modified: stats.mtime
                        });
                    }

                    // Check content if file is not too large
                    const stats = await fs.stat(entryPath);

                    if (stats.size <= state.config.maxFileSize) {
                        try {
                            const content = await fs.readFile(entryPath, 'utf8');

                            if (content.toLowerCase().includes(query.toLowerCase())) {
                                // Find context around the match
                                const contentLines = content.split('\n');
                                const matchingLines = [];

                                for (let i = 0; i < contentLines.length; i++) {
                                    if (contentLines[i].toLowerCase().includes(query.toLowerCase())) {
                                        const startLine = Math.max(0, i - 1);
                                        const endLine = Math.min(contentLines.length - 1, i + 1);

                                        matchingLines.push({
                                            line: i + 1,
                                            context: contentLines.slice(startLine, endLine + 1).join('\n')
                                        });

                                        if (matchingLines.length >= 5) {
                                            break; // Limit to 5 matches per file
                                        }
                                    }
                                }

                                results.matchesByContent.push({
                                    name: entry.name,
                                    path: entryPath,
                                    type: 'file',
                                    fileId: generateFileId(entryPath),
                                    size: stats.size,
                                    created: stats.birthtime,
                                    modified: stats.mtime,
                                    matches: matchingLines
                                });
                            }
                        } catch (err) {
                            // Skip non-text files
                            state.logger.debug(`[Filesystem] Skipping binary file: ${entryPath}`);
                        }
                    }
                }
            }
        }

        // Start search
        await searchInDirectory(startPath);

        // Update stats
        state.stats.searches++;
        state.stats.lastOperation = {
            type: 'search',
            path: startPath,
            query,
            timestamp: new Date().toISOString()
        };

        state.logger.debug(
            `[Filesystem] Search in ${startPath} for "${query}": ` +
            `${results.matchesByName.length} name matches, ${results.matchesByContent.length} content matches`
        );

        // Return successful response
        res.status(200).json({
            status: 'success',
            message: 'Search completed successfully',
            data: {
                query,
                path: startPath,
                nameMatches: results.matchesByName,
                contentMatches: results.matchesByContent,
                totalMatches: results.matchesByName.length + results.matchesByContent.length,
                limitReached: (
                    results.matchesByName.length + results.matchesByContent.length >= maxResults
                )
            }
        });
    } catch (error) {
        state.stats.errors++;
        state.logger.error(`[Filesystem] Error searching: ${error.message}`);

        // Return error response
        res.status(500).json({
            status: 'error',
            message: `Error searching: ${error.message}`
        });
    }
}

/**
 * Delete a file or directory
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function deleteFile(req, res) {
    try {
        const { path: targetPath, recursive } = req.query;

        if (!targetPath) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required parameter: path'
            });
        }

        // Check if path is allowed
        if (!isPathAllowed(targetPath)) {
            state.logger.warn(`[Filesystem] Attempted to delete unauthorized path: ${targetPath}`);
            state.stats.errors++;

            return res.status(403).json({
                status: 'error',
                message: 'Access to this path is not allowed'
            });
        }

        // Check if path exists
        const stats = await fs.stat(targetPath);

        if (stats.isDirectory()) {
            // Delete directory
            if (recursive === 'true') {
                // Recursively delete directory
                await fs.rm(targetPath, { recursive: true, force: true });
            } else {
                // Non-recursive directory delete
                try {
                    await fs.rmdir(targetPath);
                } catch (err) {
                    if (err.code === 'ENOTEMPTY') {
                        return res.status(400).json({
                            status: 'error',
                            message: 'Directory is not empty. Use recursive=true to delete non-empty directories.'
                        });
                    }
                    throw err;
                }
            }
        } else {
            // Delete file
            await fs.unlink(targetPath);
        }

        // Update stats
        state.stats.deletes++;
        state.stats.lastOperation = {
            type: 'delete',
            path: targetPath,
            timestamp: new Date().toISOString()
        };

        state.logger.debug(`[Filesystem] Deleted ${stats.isDirectory() ? 'directory' : 'file'}: ${targetPath}`);

        // Return successful response
        res.status(200).json({
            status: 'success',
            message: `${stats.isDirectory() ? 'Directory' : 'File'} deleted successfully`,
            data: {
                path: targetPath,
                type: stats.isDirectory() ? 'directory' : 'file'
            }
        });
    } catch (error) {
        state.stats.errors++;
        state.logger.error(`[Filesystem] Error deleting: ${error.message}`);

        // Return error response
        res.status(500).json({
            status: 'error',
            message: `Error deleting: ${error.message}`
        });
    }
}

// Export the initialize function
module.exports = {
    initialize
}; 