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
  type: test
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

#!/usr/bin/env node

/**
 * EVA & GUARANI - Filesystem Module CLI Test
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This utility allows testing the filesystem module from the command line.
 */

const fs = require('fs');
const path = require('path');
const express = require('express');
const fsModule = require('./index');

// Create a minimal express app for testing
const app = express();
app.use(express.json());

// Setup logger
const logger = {
    info: (...args) => console.log('\x1b[36m[INFO]\x1b[0m', ...args),
    debug: (...args) => console.log('\x1b[90m[DEBUG]\x1b[0m', ...args),
    warn: (...args) => console.log('\x1b[33m[WARN]\x1b[0m', ...args),
    error: (...args) => console.log('\x1b[31m[ERROR]\x1b[0m', ...args)
};

// Parse command line arguments
const args = process.argv.slice(2);
const command = args[0];

// Define allowed directories
const allowedDirectories = [
    process.cwd(),
    path.resolve(process.cwd(), '..')
];

// Initialize the filesystem module
const fsModuleInstance = fsModule.initialize(
    {
        allowedDirectories,
        maxFileSize: 10 * 1024 * 1024, // 10MB
        maxResults: 100
    },
    { logger }
);

// Register routes
fsModuleInstance.routes.forEach(route => {
    app[route.method.toLowerCase()](route.path, route.handler);
});

// Show help
function showHelp() {
    console.log('\n\x1b[1mEVA & GUARANI Filesystem Module CLI Test\x1b[0m');
    console.log('\x1b[90mVersion 1.0.0\x1b[0m\n');
    console.log('Commands:');
    console.log('  help                 Show this help message');
    console.log('  server               Start a test server on port 3001');
    console.log('  read <path>          Read a file');
    console.log('  write <path> <text>  Write text to a file');
    console.log('  list <path> [--recursive] [--pattern <pattern>]');
    console.log('                       List contents of a directory');
    console.log('  search <path> <query> [--recursive] [--limit <number>]');
    console.log('                       Search for files by name or content');
    console.log('  delete <path> [--recursive]');
    console.log('                       Delete a file or directory');
    console.log('  info                 Show module information');
    console.log('\nAllowed directories:');
    allowedDirectories.forEach(dir => {
        console.log(`  - ${dir}`);
    });
    console.log('');
}

// Mock request and response objects
function createMockReq(method, path, query, body) {
    return {
        method,
        path,
        query: query || {},
        body: body || {}
    };
}

function createMockRes() {
    const res = {
        statusCode: 200,
        data: null,
        status(code) {
            this.statusCode = code;
            return this;
        },
        json(data) {
            this.data = data;
            console.log(JSON.stringify(data, null, 2));
            return this;
        }
    };
    return res;
}

// Start a test server
function startServer() {
    const port = 3001;

    app.get('/', (req, res) => {
        res.send(`
            <html>
                <head>
                    <title>EVA & GUARANI Filesystem Module Test</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                        h1 { color: #333; }
                        .operation { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                        .operation h2 { margin-top: 0; }
                        label { display: block; margin-bottom: 5px; font-weight: bold; }
                        input, textarea { width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; }
                        button { background: #4CAF50; color: white; border: none; padding: 10px 15px; cursor: pointer; }
                        pre { background: #f5f5f5; padding: 10px; overflow: auto; }
                        .result { margin-top: 10px; }
                    </style>
                </head>
                <body>
                    <h1>EVA & GUARANI Filesystem Module Test</h1>

                    <div class="operation">
                        <h2>Read File</h2>
                        <form id="readForm">
                            <label for="readPath">File Path:</label>
                            <input type="text" id="readPath" required>
                            <button type="submit">Read</button>
                        </form>
                        <div id="readResult" class="result"></div>
                    </div>

                    <div class="operation">
                        <h2>Write File</h2>
                        <form id="writeForm">
                            <label for="writePath">File Path:</label>
                            <input type="text" id="writePath" required>
                            <label for="writeContent">Content:</label>
                            <textarea id="writeContent" rows="5" required></textarea>
                            <label>
                                <input type="checkbox" id="createDirectories">
                                Create directories if they don't exist
                            </label>
                            <button type="submit">Write</button>
                        </form>
                        <div id="writeResult" class="result"></div>
                    </div>

                    <div class="operation">
                        <h2>List Directory</h2>
                        <form id="listForm">
                            <label for="listPath">Directory Path:</label>
                            <input type="text" id="listPath" required>
                            <label>
                                <input type="checkbox" id="listRecursive">
                                Recursive
                            </label>
                            <label for="listPattern">Pattern (optional):</label>
                            <input type="text" id="listPattern">
                            <button type="submit">List</button>
                        </form>
                        <div id="listResult" class="result"></div>
                    </div>

                    <div class="operation">
                        <h2>Search Files</h2>
                        <form id="searchForm">
                            <label for="searchPath">Directory Path:</label>
                            <input type="text" id="searchPath" required>
                            <label for="searchQuery">Search Query:</label>
                            <input type="text" id="searchQuery" required>
                            <label>
                                <input type="checkbox" id="searchRecursive" checked>
                                Recursive
                            </label>
                            <label for="searchLimit">Result Limit:</label>
                            <input type="number" id="searchLimit" value="100">
                            <button type="submit">Search</button>
                        </form>
                        <div id="searchResult" class="result"></div>
                    </div>

                    <div class="operation">
                        <h2>Delete File/Directory</h2>
                        <form id="deleteForm">
                            <label for="deletePath">Path:</label>
                            <input type="text" id="deletePath" required>
                            <label>
                                <input type="checkbox" id="deleteRecursive">
                                Recursive (for directories)
                            </label>
                            <button type="submit">Delete</button>
                        </form>
                        <div id="deleteResult" class="result"></div>
                    </div>

                    <div class="operation">
                        <h2>Module Info</h2>
                        <button id="infoButton">Get Info</button>
                        <div id="infoResult" class="result"></div>
                    </div>

                    <script>
                        // Helper function to display results
                        function displayResult(elementId, data) {
                            const element = document.getElementById(elementId);
                            element.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                        }

                        // Read File
                        document.getElementById('readForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('readPath').value;

                            try {
                                const response = await fetch(`/ filesystem / read ? path = ${ encodeURIComponent(path) }`);
                                const result = await response.json();
                                displayResult('readResult', result);
                            } catch (error) {
                                displayResult('readResult', { error: error.message });
                            }
                        });

                        // Write File
                        document.getElementById('writeForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('writePath').value;
                            const content = document.getElementById('writeContent').value;
                            const createDirectories = document.getElementById('createDirectories').checked;

                            try {
                                const response = await fetch('/filesystem/write', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ path, content, createDirectories })
                                });
                                const result = await response.json();
                                displayResult('writeResult', result);
                            } catch (error) {
                                displayResult('writeResult', { error: error.message });
                            }
                        });

                        // List Directory
                        document.getElementById('listForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('listPath').value;
                            const recursive = document.getElementById('listRecursive').checked;
                            const pattern = document.getElementById('listPattern').value;

                            try {
                                const url = new URL('/filesystem/list', window.location.origin);
                                url.searchParams.append('path', path);
                                url.searchParams.append('recursive', recursive);
                                if (pattern) url.searchParams.append('pattern', pattern);

                                const response = await fetch(url);
                                const result = await response.json();
                                displayResult('listResult', result);
                            } catch (error) {
                                displayResult('listResult', { error: error.message });
                            }
                        });

                        // Search Files
                        document.getElementById('searchForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('searchPath').value;
                            const query = document.getElementById('searchQuery').value;
                            const recursive = document.getElementById('searchRecursive').checked;
                            const limit = document.getElementById('searchLimit').value;

                            try {
                                const url = new URL('/filesystem/search', window.location.origin);
                                url.searchParams.append('path', path);
                                url.searchParams.append('query', query);
                                url.searchParams.append('recursive', recursive);
                                url.searchParams.append('limit', limit);

                                const response = await fetch(url);
                                const result = await response.json();
                                displayResult('searchResult', result);
                            } catch (error) {
                                displayResult('searchResult', { error: error.message });
                            }
                        });

                        // Delete File/Directory
                        document.getElementById('deleteForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('deletePath').value;
                            const recursive = document.getElementById('deleteRecursive').checked;

                            if (!confirm(`Are you sure you want to delete ${ path } ? `)) {
                                return;
                            }

                            try {
                                const url = new URL('/filesystem/delete', window.location.origin);
                                url.searchParams.append('path', path);
                                url.searchParams.append('recursive', recursive);

                                const response = await fetch(url, { method: 'DELETE' });
                                const result = await response.json();
                                displayResult('deleteResult', result);
                            } catch (error) {
                                displayResult('deleteResult', { error: error.message });
                            }
                        });

                        // Module Info
                        document.getElementById('infoButton').addEventListener('click', async () => {
                            try {
                                const response = await fetch('/filesystem/info');
                                const result = await response.json();
                                displayResult('infoResult', result);
                            } catch (error) {
                                displayResult('infoResult', { error: error.message });
                            }
                        });
                    </script>
                </body>
            </html>
        `);
    });

    app.get('/filesystem/info', (req, res) => {
        res.json({
            status: 'success',
            data: {
                name: fsModuleInstance.name,
                version: fsModuleInstance.version,
                routes: fsModuleInstance.routes.map(r => ({
                    method: r.method,
                    path: r.path,
                    description: r.description
                })),
                config: {
                    allowedDirectories,
                    maxFileSize: fsModuleInstance.config?.maxFileSize || 10 * 1024 * 1024,
                    maxResults: fsModuleInstance.config?.maxResults || 100
                }
            }
        });
    });

    app.listen(port, () => {
        logger.info(`Test server running at http://localhost:${port}`);
        logger.info(`Press Ctrl+C to stop`);
    });
}

// Process commands
async function processCommand() {
    if (!command || command === 'help') {
        showHelp();
        return;
    }

    if (command === 'server') {
        startServer();
        return;
    }

    if (command === 'read') {
        const filePath = args[1];

        if (!filePath) {
            logger.error('Missing file path');
            return;
        }

        const req = createMockReq('GET', '/filesystem/read', { path: filePath });
        const res = createMockRes();

        await fsModuleInstance.routes.find(r => r.path === '/filesystem/read').handler(req, res);
        return;
    }

    if (command === 'write') {
        const filePath = args[1];
        const content = args[2] || '';

        if (!filePath) {
            logger.error('Missing file path');
            return;
        }

        const req = createMockReq('POST', '/filesystem/write', null, {
            path: filePath,
            content,
            createDirectories: args.includes('--create-dirs')
        });
        const res = createMockRes();

        await fsModuleInstance.routes.find(r => r.path === '/filesystem/write').handler(req, res);
        return;
    }

    if (command === 'list') {
        const dirPath = args[1];

        if (!dirPath) {
            logger.error('Missing directory path');
            return;
        }

        const recursive = args.includes('--recursive');
        let pattern = null;

        const patternIndex = args.indexOf('--pattern');
        if (patternIndex !== -1 && args.length > patternIndex + 1) {
            pattern = args[patternIndex + 1];
        }

        const req = createMockReq('GET', '/filesystem/list', {
            path: dirPath,
            recursive: recursive.toString(),
            pattern
        });
        const res = createMockRes();

        await fsModuleInstance.routes.find(r => r.path === '/filesystem/list').handler(req, res);
        return;
    }

    if (command === 'search') {
        const dirPath = args[1];
        const query = args[2];

        if (!dirPath || !query) {
            logger.error('Missing directory path or search query');
            return;
        }

        const recursive = !args.includes('--no-recursive');
        let limit = 100;

        const limitIndex = args.indexOf('--limit');
        if (limitIndex !== -1 && args.length > limitIndex + 1) {
            limit = parseInt(args[limitIndex + 1], 10);
        }

        const req = createMockReq('GET', '/filesystem/search', {
            path: dirPath,
            query,
            recursive: recursive.toString(),
            limit
        });
        const res = createMockRes();

        await fsModuleInstance.routes.find(r => r.path === '/filesystem/search').handler(req, res);
        return;
    }

    if (command === 'delete') {
        const filePath = args[1];

        if (!filePath) {
            logger.error('Missing file path');
            return;
        }

        // Ask for confirmation
        if (!args.includes('--force')) {
            console.log(`Are you sure you want to delete ${filePath}? (y/N)`);
            const stdin = process.stdin;
            stdin.setRawMode(true);
            stdin.resume();
            stdin.setEncoding('utf8');

            await new Promise(resolve => {
                stdin.once('data', (key) => {
                    stdin.setRawMode(false);
                    stdin.pause();

                    if (key.toLowerCase() !== 'y') {
                        console.log('Operation cancelled');
                        resolve(false);
                        return;
                    }

                    resolve(true);
                });
            }).then(confirmed => {
                if (!confirmed) {
                    return;
                }

                const recursive = args.includes('--recursive');

                const req = createMockReq('DELETE', '/filesystem/delete', {
                    path: filePath,
                    recursive: recursive.toString()
                });
                const res = createMockRes();

                fsModuleInstance.routes.find(r => r.path === '/filesystem/delete').handler(req, res);
            });

            return;
        }

        const recursive = args.includes('--recursive');

        const req = createMockReq('DELETE', '/filesystem/delete', {
            path: filePath,
            recursive: recursive.toString()
        });
        const res = createMockRes();

        await fsModuleInstance.routes.find(r => r.path === '/filesystem/delete').handler(req, res);
        return;
    }

    if (command === 'info') {
        console.log('\n\x1b[1mEVA & GUARANI Filesystem Module Information\x1b[0m');
        console.log(`Name: ${fsModuleInstance.name}`);
        console.log(`Version: ${fsModuleInstance.version}`);
        console.log('\nAvailable Routes:');

        fsModuleInstance.routes.forEach(route => {
            console.log(`  ${route.method} ${route.path}`);
            console.log(`    ${route.description}`);
        });

        console.log('\nAllowed Directories:');
        allowedDirectories.forEach(dir => {
            console.log(`  - ${dir}`);
        });

        console.log('\nConfiguration:');
        console.log(`  Max File Size: ${fsModuleInstance.config?.maxFileSize || 10 * 1024 * 1024} bytes`);
        console.log(`  Max Results: ${fsModuleInstance.config?.maxResults || 100}`);

        return;
    }

    logger.error(`Unknown command: ${command}`);
    showHelp();
}

// Run the CLI
processCommand().catch(error => {
    logger.error('Error:', error.message);
    process.exit(1);
});
