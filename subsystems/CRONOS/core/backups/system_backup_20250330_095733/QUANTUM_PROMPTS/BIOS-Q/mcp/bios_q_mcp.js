---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: BIOS-Q
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
  subsystem: BIOS-Q
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

const winston = require('winston');
const path = require('path');
const fs = require('fs');
const readline = require('readline');

// Ensure logs directory exists
const logsDir = process.env.LOG_DIR || 'C:\\Eva Guarani EGOS\\logs';
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
}

// Configure Winston logger
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'debug',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({
            filename: path.join(logsDir, 'bios_q.log'),
            level: 'debug'
        }),
        new winston.transports.File({
            filename: path.join(logsDir, 'mcp.log'),
            level: 'debug'
        }),
        new winston.transports.Console({
            format: winston.format.simple(),
            level: 'debug'
        })
    ]
});

// Log startup information
logger.info('BIOS-Q MCP Starting', {
    pid: process.pid,
    nodeVersion: process.version,
    platform: process.platform,
    arch: process.arch,
    workingDirectory: process.cwd(),
    env: process.env
});

// Create readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception:', error);
    process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
    logger.error('Unhandled Rejection:', reason);
    process.exit(1);
});

// Handle process signals
process.on('SIGTERM', () => {
    logger.info('Received SIGTERM signal');
    process.exit(0);
});

process.on('SIGINT', () => {
    logger.info('Received SIGINT signal');
    process.exit(0);
});

// Write message to stdout
function writeMessage(message) {
    try {
        const messageString = JSON.stringify(message);
        process.stdout.write(messageString + '\n');
        logger.debug('Message sent:', message);
    } catch (error) {
        logger.error('Error writing message:', error);
    }
}

// Process incoming messages
rl.on('line', (line) => {
    try {
        const message = JSON.parse(line);
        logger.debug('Received message:', message);

        switch (message.type) {
            case 'shutdown':
                logger.info('Received shutdown command');
                process.exit(0);
                break;

            case 'list_tools':
                writeMessage({
                    type: 'tools',
                    tools: ['bios-q']
                });
                break;

            case 'execute':
                handleExecute(message);
                break;

            default:
                logger.warn('Unknown message type:', message.type);
                break;
        }
    } catch (error) {
        logger.error('Error processing message:', error);
    }
});

// Handle execute commands
function handleExecute(message) {
    try {
        const response = {
            type: 'result',
            id: message.id,
            success: true,
            result: {
                status: 'active',
                timestamp: new Date().toISOString()
            }
        };
        writeMessage(response);
    } catch (error) {
        logger.error('Error handling execute:', error);
        writeMessage({
            type: 'error',
            id: message.id,
            error: error.message
        });
    }
}

// Start heartbeat
setInterval(() => {
    writeMessage({
        type: 'heartbeat',
        timestamp: new Date().toISOString()
    });
}, 5000);

logger.info('BIOS-Q MCP initialized and ready'); 