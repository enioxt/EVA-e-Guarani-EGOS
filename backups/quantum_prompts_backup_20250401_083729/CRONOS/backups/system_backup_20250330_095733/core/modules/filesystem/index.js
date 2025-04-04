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
 * EVA & GUARANI - SLOP Filesystem Module
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This module provides filesystem access through the SLOP API.
 * It allows reading, writing, listing, and searching files in specified directories.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration with allowed directories - this should be loaded from environment or config
const DEFAULT_CONFIG = {
    allowedDirectories: [
        'C:/Eva Guarani EGOS' // Default allowed directory
    ],
    maxFileSize: 10 * 1024 * 1024, // 10MB
    maxResults: 1000,
    logLevel: 'info'
};

// Module state
let config = { ...DEFAULT_CONFIG };
let logger = console;

/**
 * Initialize the filesystem module
 * @param {Object} options - Configuration options
 * @param {Object} dependencies - Dependencies including logger
 */
function initialize(options = {}, dependencies = {}) {
    config = { ...DEFAULT_CONFIG, ...options };
    logger = dependencies.logger || console;

    logger.info('[SLOP][FS] Filesystem module initialized with config:', config);

    // Ensure all paths use consistent format
    config.allowedDirectories = config.allowedDirectories.map(dir =>
        path.normalize(dir).replace(/\\/g, '/')
    );

    return {
        name: 'filesystem',
        version: '1.0.0',
        routes: getRoutes()
    };
}

/**
 * Get routes configuration for the module
 * @returns {Array} Routes configuration
 */
function getRoutes() {
    return [
        {
            method: 'POST',
            path: '/fs/read',
            handler: readFile,
            description: 'Read a file from the filesystem'
        },
        {
            method: 'POST',
            path: '/fs/write',
            handler: writeFile,
            description: 'Write content to a file'
        },
        {
            method: 'POST',
            path: '/fs/list',
            handler: listDirectory,
            description: 'List files in a directory'
        },
        {
            method: 'POST',
            path: '/fs/search',
            handler: searchFiles,
            description: 'Search for files by name or content'
        },
        {
            method: 'POST',
            path: '/fs/delete',
            handler: deleteFile,
            description: 'Delete a file'
        }
    ];
}

/**
 * Check if a path is allowed based on configured allowed directories
 * @param {string} targetPath - Path to check
 * @returns {boolean} True if path is allowed
 */
function isPathAllowed(targetPath) {
    const normalizedPath = path.normalize(targetPath).replace(/\\/g, '/');

    return config.allowedDirectories.some(dir => {
        const normalizedDir = path.normalize(dir).replace(/\\/g, '/');
        return normalizedPath.startsWith(normalizedDir);
    });
}

/**
 * Generate a unique ID for a file
 * @param {string} filePath - Path to the file
 * @returns {string} Unique ID
 */
function generateFileId(filePath) {
    return crypto.createHash('md5').update(filePath).digest('hex');
}

/**
 * Read a file from the filesystem
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
async function readFile(req, res) {
    try {
        const { path: filePath, encoding = 'utf8' } = req.body;

        if (!filePath) {
            return res.status(400).json({ error: 'Missing required parameter: path' });
        }

        // Security check
        if (!isPathAllowed(filePath)) {
            logger.warn(`[SLOP][FS] Attempted to access unauthorized path: ${filePath}`);
            return res.status(403).json({ error: 'Access denied to this path' });
        }

        // Check if file exists
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({ error: 'File not found' });
        }

        // Read file with proper error handling
        try {
            const stats = fs.statSync(filePath);

            // Check if it's a directory
            if (stats.isDirectory()) {
                return res.status(400).json({ error: 'Path is a directory, not a file' });
            }

            // Check file size
            if (stats.size > config.maxFileSize) {
                return res.status(413).json({ error: 'File too large' });
            }

            // Read the file
            const content = await fs.promises.readFile(filePath, { encoding });

            // Log successful read
            logger.info(`[SLOP][FS] Read file: ${filePath}`);

            // Return the file content
            return res.json({
                success: true,
                path: filePath,
                content,
                encoding,
                stats: {
                    size: stats.size,
                    modified: stats.mtime,
                    created: stats.birthtime
                },
                id: generateFileId(filePath)
            });
        } catch (fileError) {
            logger.error(`[SLOP][FS] Error reading file: ${filePath}`, fileError);
            return res.status(500).json({
                error: 'Error reading file',
                details: fileError.message
            });
        }
    } catch (error) {
        logger.error('[SLOP][FS] Server error:', error);
        return res.status(500).json({
            error: 'Server error',
            details: error.message
        });
    }
}

/**
 * Write content to a file
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
async function writeFile(req, res) {
    try {
        const { path: filePath, content, encoding = 'utf8', createDirectories = false } = req.body;

        if (!filePath || content === undefined) {
            return res.status(400).json({ error: 'Missing required parameters: path and content' });
        }

        // Security check
        if (!isPathAllowed(filePath)) {
            logger.warn(`[SLOP][FS] Attempted to write to unauthorized path: ${filePath}`);
            return res.status(403).json({ error: 'Access denied to this path' });
        }

        // Check if content size is within limits
        const contentSize = Buffer.byteLength(content, encoding);
        if (contentSize > config.maxFileSize) {
            return res.status(413).json({ error: 'Content too large' });
        }

        // Create directories if needed
        if (createDirectories) {
            const dirPath = path.dirname(filePath);
            if (!fs.existsSync(dirPath)) {
                await fs.promises.mkdir(dirPath, { recursive: true });
                logger.info(`[SLOP][FS] Created directory: ${dirPath}`);
            }
        }

        // Write the file
        try {
            await fs.promises.writeFile(filePath, content, { encoding });

            // Log successful write
            logger.info(`[SLOP][FS] Wrote file: ${filePath}`);

            // Return success
            return res.json({
                success: true,
                path: filePath,
                size: contentSize,
                id: generateFileId(filePath)
            });
        } catch (fileError) {
            logger.error(`[SLOP][FS] Error writing file: ${filePath}`, fileError);
            return res.status(500).json({
                error: 'Error writing file',
                details: fileError.message
            });
        }
    } catch (error) {
        logger.error('[SLOP][FS] Server error:', error);
        return res.status(500).json({
            error: 'Server error',
            details: error.message
        });
    }
}

/**
 * List files in a directory
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
async function listDirectory(req, res) {
    try {
        const { path: dirPath, recursive = false, pattern = null } = req.body;

        if (!dirPath) {
            return res.status(400).json({ error: 'Missing required parameter: path' });
        }

        // Security check
        if (!isPathAllowed(dirPath)) {
            logger.warn(`[SLOP][FS] Attempted to list unauthorized directory: ${dirPath}`);
            return res.status(403).json({ error: 'Access denied to this path' });
        }

        // Check if directory exists
        if (!fs.existsSync(dirPath)) {
            return res.status(404).json({ error: 'Directory not found' });
        }

        // Check if it's a directory
        const stats = fs.statSync(dirPath);
        if (!stats.isDirectory()) {
            return res.status(400).json({ error: 'Path is not a directory' });
        }

        // List files
        try {
            let files = [];

            if (recursive) {
                // Use a recursive function to list all files
                files = listFilesRecursively(dirPath);
            } else {
                // List only files in the current directory
                const entries = await fs.promises.readdir(dirPath, { withFileTypes: true });

                files = entries.map(entry => {
                    const entryPath = path.join(dirPath, entry.name);
                    const isDir = entry.isDirectory();

                    return {
                        name: entry.name,
                        path: entryPath,
                        isDirectory: isDir,
                        id: generateFileId(entryPath)
                    };
                });
            }

            // Apply pattern filtering if provided
            if (pattern) {
                const regex = new RegExp(pattern);
                files = files.filter(file => regex.test(file.name));
            }

            // Limit results
            if (files.length > config.maxResults) {
                files = files.slice(0, config.maxResults);
            }

            // Log successful listing
            logger.info(`[SLOP][FS] Listed directory: ${dirPath}, found ${files.length} entries`);

            // Return the file list
            return res.json({
                success: true,
                path: dirPath,
                files,
                count: files.length,
                limited: files.length === config.maxResults
            });
        } catch (dirError) {
            logger.error(`[SLOP][FS] Error listing directory: ${dirPath}`, dirError);
            return res.status(500).json({
                error: 'Error listing directory',
                details: dirError.message
            });
        }
    } catch (error) {
        logger.error('[SLOP][FS] Server error:', error);
        return res.status(500).json({
            error: 'Server error',
            details: error.message
        });
    }
}

/**
 * List files recursively in a directory
 * @param {string} dirPath - Path to the directory
 * @returns {Array} List of files and directories
 */
function listFilesRecursively(dirPath) {
    let results = [];
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
        const entryPath = path.join(dirPath, entry.name);
        const isDir = entry.isDirectory();

        results.push({
            name: entry.name,
            path: entryPath,
            isDirectory: isDir,
            id: generateFileId(entryPath)
        });

        if (isDir) {
            const subResults = listFilesRecursively(entryPath);
            results = results.concat(subResults);
        }
    }

    return results;
}

/**
 * Search for files by name or content
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
async function searchFiles(req, res) {
    try {
        const {
            path: dirPath,
            namePattern = null,
            contentPattern = null,
            recursive = true,
            maxResults = 100
        } = req.body;

        if (!dirPath) {
            return res.status(400).json({ error: 'Missing required parameter: path' });
        }

        if (!namePattern && !contentPattern) {
            return res.status(400).json({ error: 'At least one pattern (name or content) is required' });
        }

        // Security check
        if (!isPathAllowed(dirPath)) {
            logger.warn(`[SLOP][FS] Attempted to search unauthorized directory: ${dirPath}`);
            return res.status(403).json({ error: 'Access denied to this path' });
        }

        // Check if directory exists
        if (!fs.existsSync(dirPath)) {
            return res.status(404).json({ error: 'Directory not found' });
        }

        // Check if it's a directory
        const stats = fs.statSync(dirPath);
        if (!stats.isDirectory()) {
            return res.status(400).json({ error: 'Path is not a directory' });
        }

        // Search files
        try {
            // Get all files in the directory (recursively if requested)
            let files = [];

            if (recursive) {
                files = listFilesRecursively(dirPath);
            } else {
                const entries = await fs.promises.readdir(dirPath, { withFileTypes: true });

                files = entries.map(entry => {
                    const entryPath = path.join(dirPath, entry.name);

                    return {
                        name: entry.name,
                        path: entryPath,
                        isDirectory: entry.isDirectory(),
                        id: generateFileId(entryPath)
                    };
                });
            }

            // Filter files that are not directories
            const fileResults = files.filter(file => !file.isDirectory);

            // Apply name pattern filtering if provided
            let matches = fileResults;
            if (namePattern) {
                const nameRegex = new RegExp(namePattern, 'i');
                matches = matches.filter(file => nameRegex.test(file.name));
            }

            // Apply content pattern filtering if provided
            if (contentPattern) {
                const contentRegex = new RegExp(contentPattern, 'i');
                const contentMatches = [];

                // This can be resource intensive, so limit the number of files to check
                const filesToCheck = matches.slice(0, Math.min(matches.length, 1000));

                for (const file of filesToCheck) {
                    try {
                        const content = fs.readFileSync(file.path, 'utf8');
                        if (contentRegex.test(content)) {
                            contentMatches.push({
                                ...file,
                                matchesContent: true
                            });
                        }
                    } catch (e) {
                        // Skip files that cannot be read as text
                        logger.warn(`[SLOP][FS] Could not read file for content search: ${file.path}`);
                    }
                }

                matches = contentMatches;
            }

            // Limit results
            const limit = Math.min(maxResults, config.maxResults);
            if (matches.length > limit) {
                matches = matches.slice(0, limit);
            }

            // Log successful search
            logger.info(`[SLOP][FS] Searched in: ${dirPath}, found ${matches.length} matches`);

            // Return the search results
            return res.json({
                success: true,
                path: dirPath,
                matches,
                count: matches.length,
                limited: matches.length === limit
            });
        } catch (searchError) {
            logger.error(`[SLOP][FS] Error searching files: ${dirPath}`, searchError);
            return res.status(500).json({
                error: 'Error searching files',
                details: searchError.message
            });
        }
    } catch (error) {
        logger.error('[SLOP][FS] Server error:', error);
        return res.status(500).json({
            error: 'Server error',
            details: error.message
        });
    }
}

/**
 * Delete a file
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 */
async function deleteFile(req, res) {
    try {
        const { path: filePath, recursive = false } = req.body;

        if (!filePath) {
            return res.status(400).json({ error: 'Missing required parameter: path' });
        }

        // Security check
        if (!isPathAllowed(filePath)) {
            logger.warn(`[SLOP][FS] Attempted to delete unauthorized path: ${filePath}`);
            return res.status(403).json({ error: 'Access denied to this path' });
        }

        // Check if file/directory exists
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({ error: 'File or directory not found' });
        }

        // Delete the file or directory
        try {
            const stats = fs.statSync(filePath);
            const isDirectory = stats.isDirectory();

            if (isDirectory) {
                if (!recursive) {
                    return res.status(400).json({ error: 'Cannot delete directory without recursive flag' });
                }

                await fs.promises.rmdir(filePath, { recursive: true });
            } else {
                await fs.promises.unlink(filePath);
            }

            // Log successful deletion
            logger.info(`[SLOP][FS] Deleted ${isDirectory ? 'directory' : 'file'}: ${filePath}`);

            // Return success
            return res.json({
                success: true,
                path: filePath,
                isDirectory
            });
        } catch (deleteError) {
            logger.error(`[SLOP][FS] Error deleting path: ${filePath}`, deleteError);
            return res.status(500).json({
                error: 'Error deleting file or directory',
                details: deleteError.message
            });
        }
    } catch (error) {
        logger.error('[SLOP][FS] Server error:', error);
        return res.status(500).json({
            error: 'Server error',
            details: error.message
        });
    }
}

module.exports = {
    initialize
};
