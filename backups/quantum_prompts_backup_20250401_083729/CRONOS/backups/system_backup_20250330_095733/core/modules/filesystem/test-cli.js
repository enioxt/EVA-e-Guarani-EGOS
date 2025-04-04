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
 * EVA & GUARANI - SLOP Filesystem Module CLI Tester
 * Version: 1.0.0
 * Date: 2025-03-29
 *
 * This utility allows testing filesystem operations from the command line.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { promisify } = require('util');
const filesystemModule = require('./index');

// Setup colored console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    dim: '\x1b[2m',
    underscore: '\x1b[4m',
    blink: '\x1b[5m',
    reverse: '\x1b[7m',
    hidden: '\x1b[8m',

    fg: {
        black: '\x1b[30m',
        red: '\x1b[31m',
        green: '\x1b[32m',
        yellow: '\x1b[33m',
        blue: '\x1b[34m',
        magenta: '\x1b[35m',
        cyan: '\x1b[36m',
        white: '\x1b[37m',
        crimson: '\x1b[38m'
    },

    bg: {
        black: '\x1b[40m',
        red: '\x1b[41m',
        green: '\x1b[42m',
        yellow: '\x1b[43m',
        blue: '\x1b[44m',
        magenta: '\x1b[45m',
        cyan: '\x1b[46m',
        white: '\x1b[47m',
        crimson: '\x1b[48m'
    }
};

// Setup mock Express response
class MockResponse {
    constructor() {
        this.statusCode = 200;
        this.data = null;
    }

    status(code) {
        this.statusCode = code;
        return this;
    }

    json(data) {
        this.data = data;
        return this;
    }

    send(data) {
        this.data = data;
        return this;
    }
}

// Setup readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = promisify(rl.question).bind(rl);

// Initialize filesystem module
const filesystem = filesystemModule.initialize({
    allowedDirectories: [process.cwd(), 'C:/Eva Guarani EGOS'],
    maxFileSize: 10 * 1024 * 1024,
    maxResults: 1000,
    logLevel: 'debug'
}, {
    logger: {
        debug: (...args) => console.log(colors.fg.blue, '[DEBUG]', ...args, colors.reset),
        info: (...args) => console.log(colors.fg.green, '[INFO]', ...args, colors.reset),
        warn: (...args) => console.log(colors.fg.yellow, '[WARN]', ...args, colors.reset),
        error: (...args) => console.error(colors.fg.red, '[ERROR]', ...args, colors.reset),
        child: () => ({
            debug: (...args) => console.log(colors.fg.blue, '[DEBUG][CHILD]', ...args, colors.reset),
            info: (...args) => console.log(colors.fg.green, '[INFO][CHILD]', ...args, colors.reset),
            warn: (...args) => console.log(colors.fg.yellow, '[WARN][CHILD]', ...args, colors.reset),
            error: (...args) => console.error(colors.fg.red, '[ERROR][CHILD]', ...args, colors.reset),
        })
    }
});

// Get routes from filesystem module
const routes = filesystem.routes;

// Display header
console.log(colors.fg.magenta);
console.log('╔══════════════════════════════════════════════════════════════╗');
console.log('║                                                              ║');
console.log('║  EVA & GUARANI - SLOP Filesystem Module CLI Tester v1.0.0    ║');
console.log('║                                                              ║');
console.log('╚══════════════════════════════════════════════════════════════╝');
console.log(colors.reset);

// Display available routes
console.log(colors.fg.cyan, 'Available Commands:', colors.reset);
routes.forEach((route, index) => {
    console.log(`  ${colors.fg.yellow}${index + 1}${colors.reset}. ${colors.fg.green}${route.method}${colors.reset} ${colors.fg.white}${route.path}${colors.reset} - ${route.description}`);
});
console.log(`  ${colors.fg.yellow}q${colors.reset}. Quit`);
console.log();

// Main menu
async function mainMenu() {
    try {
        const answer = await question(`${colors.fg.cyan}Enter command number or 'q' to quit: ${colors.reset}`);

        if (answer.toLowerCase() === 'q') {
            console.log(colors.fg.magenta, 'Goodbye!', colors.reset);
            rl.close();
            return;
        }

        const index = parseInt(answer) - 1;
        if (isNaN(index) || index < 0 || index >= routes.length) {
            console.log(colors.fg.red, 'Invalid command number. Please try again.', colors.reset);
            return mainMenu();
        }

        const route = routes[index];
        await executeRoute(route);

        return mainMenu();
    } catch (error) {
        console.error(colors.fg.red, 'Error:', error.message, colors.reset);
        return mainMenu();
    }
}

// Execute a route
async function executeRoute(route) {
    try {
        console.log(colors.fg.cyan, `\nExecuting ${route.method} ${route.path}`, colors.reset);
        console.log(colors.fg.yellow, 'Please provide the request body as JSON:', colors.reset);

        // Get method-specific input
        let jsonBody = '{}';

        switch (route.path) {
            case '/fs/read':
                const readPath = await question('Enter file path to read: ');
                const readEncoding = await question('Enter encoding (default: utf8): ');
                jsonBody = JSON.stringify({
                    path: readPath,
                    encoding: readEncoding || 'utf8'
                }, null, 2);
                break;

            case '/fs/write':
                const writePath = await question('Enter file path to write: ');
                const writeContent = await question('Enter content: ');
                const writeEncoding = await question('Enter encoding (default: utf8): ');
                const createDirs = await question('Create directories if needed? (y/n): ');
                jsonBody = JSON.stringify({
                    path: writePath,
                    content: writeContent,
                    encoding: writeEncoding || 'utf8',
                    createDirectories: createDirs.toLowerCase() === 'y'
                }, null, 2);
                break;

            case '/fs/list':
                const listPath = await question('Enter directory path to list: ');
                const recursive = await question('List recursively? (y/n): ');
                const pattern = await question('Enter name pattern (regex, optional): ');
                jsonBody = JSON.stringify({
                    path: listPath,
                    recursive: recursive.toLowerCase() === 'y',
                    pattern: pattern || null
                }, null, 2);
                break;

            case '/fs/search':
                const searchPath = await question('Enter directory path to search: ');
                const namePattern = await question('Enter name pattern (regex, optional): ');
                const contentPattern = await question('Enter content pattern (regex, optional): ');
                const searchRecursive = await question('Search recursively? (y/n): ');
                const maxResults = await question('Enter max results (default: 100): ');
                jsonBody = JSON.stringify({
                    path: searchPath,
                    namePattern: namePattern || null,
                    contentPattern: contentPattern || null,
                    recursive: searchRecursive.toLowerCase() === 'y',
                    maxResults: maxResults ? parseInt(maxResults) : 100
                }, null, 2);
                break;

            case '/fs/delete':
                const deletePath = await question('Enter file/directory path to delete: ');
                const deleteRecursive = await question('Delete recursively? (y/n): ');
                jsonBody = JSON.stringify({
                    path: deletePath,
                    recursive: deleteRecursive.toLowerCase() === 'y'
                }, null, 2);
                break;

            default:
                jsonBody = await question('Enter JSON request body: ');
                break;
        }

        // Parse JSON body
        const body = JSON.parse(jsonBody);

        // Create mock request and response
        const req = {
            method: route.method,
            path: route.path,
            body
        };

        const res = new MockResponse();

        // Execute the route handler
        await route.handler(req, res);

        // Display the result
        console.log(colors.fg.cyan, '\nResponse Status:', colors.reset, res.statusCode);
        console.log(colors.fg.cyan, 'Response Body:', colors.reset);
        console.log(JSON.stringify(res.data, null, 2));
        console.log();

    } catch (error) {
        console.error(colors.fg.red, 'Error:', error.message, colors.reset);
    }

    await question(colors.fg.yellow + 'Press Enter to continue...' + colors.reset);
}

// Start the program
mainMenu().catch(error => {
    console.error(colors.fg.red, 'Fatal Error:', error.message, colors.reset);
    rl.close();
});

// Handle exit
process.on('SIGINT', () => {
    console.log(colors.fg.magenta, '\nExiting...', colors.reset);
    rl.close();
});

rl.on('close', () => {
    console.log(colors.fg.magenta, '\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧', colors.reset);
    process.exit(0);
});
