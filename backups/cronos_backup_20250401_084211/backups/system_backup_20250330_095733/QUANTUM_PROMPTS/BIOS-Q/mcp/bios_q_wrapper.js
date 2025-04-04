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

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuração
const config = {
    pythonPath: 'python',
    scriptPath: path.join(__dirname, 'bios_q_minimal_mcp.py'),
    logPath: 'C:\\Eva Guarani EGOS\\logs',
    env: {
        ...process.env,
        PYTHONUNBUFFERED: '1',
        QUANTUM_LOG_LEVEL: 'DEBUG',
        QUANTUM_STATE_DIR: 'C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS',
        BIOS_Q_CONFIG: 'C:\\Eva Guarani EGOS\\BIOS-Q\\config\\bios_q_config.json',
        PYTHONPATH: 'C:\\Eva Guarani EGOS\\BIOS-Q;C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS'
    }
};

// Garantir que o diretório de logs existe
if (!fs.existsSync(config.logPath)) {
    fs.mkdirSync(config.logPath, { recursive: true });
}

// Função para log com timestamp
function log(message, type = 'INFO') {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${type}] ${message}\n`;

    // Log para console
    console.log(logMessage);

    // Log para arquivo
    fs.appendFileSync(path.join(config.logPath, 'bios_q_wrapper.log'), logMessage);
}

// Função para iniciar o processo Python
function startPythonProcess() {
    log('Starting BIOS-Q MCP...', 'INFO');
    log(`Using Python script: ${config.scriptPath}`, 'DEBUG');
    log(`Environment variables: ${JSON.stringify(config.env, null, 2)}`, 'DEBUG');

    const pythonProcess = spawn(config.pythonPath, [config.scriptPath], {
        env: config.env,
        stdio: ['pipe', 'pipe', 'pipe'],
        windowsHide: true
    });

    // Log do PID
    log(`BIOS-Q process started with PID: ${pythonProcess.pid}`, 'INFO');

    // Pipe do stdin/stdout com buffering
    let stdoutBuffer = '';
    let stderrBuffer = '';

    process.stdin.pipe(pythonProcess.stdin);

    pythonProcess.stdout.on('data', (data) => {
        stdoutBuffer += data.toString();
        if (stdoutBuffer.includes('\n')) {
            const lines = stdoutBuffer.split('\n');
            stdoutBuffer = lines.pop(); // Manter o que sobrou após último \n
            lines.forEach(line => {
                log(`STDOUT: ${line}`, 'OUTPUT');
                process.stdout.write(line + '\n');
            });
        }
    });

    // Log de erros com buffering
    pythonProcess.stderr.on('data', (data) => {
        stderrBuffer += data.toString();
        if (stderrBuffer.includes('\n')) {
            const lines = stderrBuffer.split('\n');
            stderrBuffer = lines.pop();
            lines.forEach(line => {
                log(`STDERR: ${line}`, 'ERROR');
                process.stderr.write(line + '\n');
            });
        }
    });

    // Gerenciamento do processo
    pythonProcess.on('close', (code, signal) => {
        log(`BIOS-Q process exited with code ${code} and signal ${signal}`, 'WARN');
        process.exit(code);
    });

    // Tratamento de erros
    pythonProcess.on('error', (err) => {
        log(`Failed to start BIOS-Q process: ${err.message}`, 'ERROR');
        log(err.stack, 'ERROR');
        process.exit(1);
    });

    return pythonProcess;
}

// Iniciar o processo
let currentProcess = startPythonProcess();

// Gerenciar sinais do processo
process.on('SIGINT', () => {
    log('Received SIGINT. Shutting down BIOS-Q MCP...', 'INFO');
    if (currentProcess) {
        currentProcess.kill('SIGINT');
    }
    process.exit(0);
});

process.on('SIGTERM', () => {
    log('Received SIGTERM. Shutting down BIOS-Q MCP...', 'INFO');
    if (currentProcess) {
        currentProcess.kill('SIGTERM');
    }
    process.exit(0);
});

// Capturar erros não tratados
process.on('uncaughtException', (err) => {
    log(`Uncaught Exception: ${err.message}`, 'ERROR');
    log(err.stack, 'ERROR');
    if (currentProcess) {
        currentProcess.kill('SIGTERM');
    }
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    log(`Unhandled Rejection at: ${promise}, reason: ${reason}`, 'ERROR');
    if (currentProcess) {
        currentProcess.kill('SIGTERM');
    }
    process.exit(1);
});
