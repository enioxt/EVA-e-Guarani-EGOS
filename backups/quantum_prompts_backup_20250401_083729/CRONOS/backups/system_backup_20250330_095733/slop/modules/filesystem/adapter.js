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
 * EVA & GUARANI - Filesystem Module Client Adapter
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This module provides a client-side adapter for the filesystem module.
 */

/**
 * Create a client adapter for the filesystem module
 * @param {Object} options - Configuration options
 * @returns {Object} - Filesystem client API
 */
function createAdapter(options = {}) {
    const baseUrl = options.baseUrl || 'http://localhost:3000';
    const fetch = options.fetch || global.fetch;

    if (!fetch) {
        throw new Error('Fetch implementation is required. Please provide a fetch implementation in options.');
    }

    /**
     * Make an API request to the filesystem module
     * @param {string} endpoint - API endpoint
     * @param {string} method - HTTP method
     * @param {Object} data - Request data
     * @returns {Promise<Object>} - Response data
     */
    async function makeRequest(endpoint, method, data = null) {
        const url = new URL(`${baseUrl}${endpoint}`);

        const requestOptions = {
            method: method,
            headers: {
                'Accept': 'application/json'
            }
        };

        // For GET requests, add parameters to URL
        if (method === 'GET' && data) {
            Object.entries(data).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    url.searchParams.append(key, value);
                }
            });
        } else if (data) {
            // For other requests, send data in body
            requestOptions.headers['Content-Type'] = 'application/json';
            requestOptions.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url.toString(), requestOptions);
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || `API request failed with status ${response.status}`);
            }

            return result;
        } catch (error) {
            throw new Error(`Filesystem API request failed: ${error.message}`);
        }
    }

    return {
        /**
         * Read a file from the filesystem
         * @param {string} filePath - Path to the file
         * @returns {Promise<Object>} - File content and metadata
         */
        async readFile(filePath) {
            const result = await makeRequest('/filesystem/read', 'GET', { path: filePath });
            return result.data;
        },

        /**
         * Write content to a file
         * @param {string} filePath - Path to the file
         * @param {string} content - Content to write
         * @param {boolean} createDirectories - Whether to create parent directories
         * @returns {Promise<Object>} - File metadata
         */
        async writeFile(filePath, content, createDirectories = false) {
            const result = await makeRequest('/filesystem/write', 'POST', {
                path: filePath,
                content,
                createDirectories
            });
            return result.data;
        },

        /**
         * List directory contents
         * @param {string} directoryPath - Path to the directory
         * @param {boolean} recursive - Whether to list recursively
         * @param {string} pattern - Optional pattern to filter files
         * @returns {Promise<Object>} - Directory contents
         */
        async listDirectory(directoryPath, recursive = false, pattern = null) {
            const result = await makeRequest('/filesystem/list', 'GET', {
                path: directoryPath,
                recursive: recursive.toString(),
                pattern
            });
            return result.data;
        },

        /**
         * Search for files
         * @param {string} directoryPath - Path to search in
         * @param {string} query - Search query
         * @param {boolean} recursive - Whether to search recursively
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - Search results
         */
        async searchFiles(directoryPath, query, recursive = true, limit = 100) {
            const result = await makeRequest('/filesystem/search', 'GET', {
                path: directoryPath,
                query,
                recursive: recursive.toString(),
                limit
            });
            return result.data;
        },

        /**
         * Delete a file or directory
         * @param {string} filePath - Path to delete
         * @param {boolean} recursive - Whether to delete recursively
         * @returns {Promise<Object>} - Result of deletion
         */
        async deleteFile(filePath, recursive = false) {
            const result = await makeRequest('/filesystem/delete', 'DELETE', {
                path: filePath,
                recursive: recursive.toString()
            });
            return result.data;
        },

        /**
         * Get filesystem module information
         * @returns {Promise<Object>} - Module information
         */
        async getInfo() {
            const result = await makeRequest('/filesystem/info', 'GET');
            return result.data;
        }
    };
}

// For CommonJS environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { createAdapter };
}

// For browser environments
if (typeof window !== 'undefined') {
    window.EVAFilesystem = { createAdapter };
}
