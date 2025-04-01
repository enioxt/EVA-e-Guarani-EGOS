---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: QUANTUM_PROMPTS
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
  subsystem: QUANTUM_PROMPTS
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
 * EVA & GUARANI - Agendador de Atualização de Roadmap
 * ✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧
 * 
 * Este script agenda a execução do atualizador de roadmap para manter
 * a documentação sempre atualizada.
 */

const cron = require('node-cron');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configurações
const UPDATE_SCRIPT = path.join(__dirname, 'update_roadmap.js');
const LOG_FILE = path.join(__dirname, '..', 'logs', 'roadmap_scheduler.log');

// Garantir que o diretório de logs existe
const logsDir = path.join(__dirname, '..', 'logs');
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
}

/**
 * Registra uma mensagem no arquivo de log
 * @param {string} message - Mensagem a ser registrada
 */
function log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `${timestamp} - ${message}\n`;

    console.log(message);

    // Adicionar ao arquivo de log
    if (fs.existsSync(LOG_FILE)) {
        fs.appendFileSync(LOG_FILE, logMessage);
    } else {
        fs.writeFileSync(LOG_FILE, logMessage);
    }
}

/**
 * Executa o script de atualização do roadmap
 */
function runUpdateScript() {
    log('Executando atualizador de roadmap...');

    exec(`node ${UPDATE_SCRIPT}`, (error, stdout, stderr) => {
        if (error) {
            log(`Erro ao executar o script: ${error.message}`);
            return;
        }

        if (stderr) {
            log(`Erro no script: ${stderr}`);
            return;
        }

        log('Script executado com sucesso!');
        log(`Saída: ${stdout}`);
    });
}

// Iniciar o agendador
console.log('✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧');
console.log('Agendador de Atualização de Roadmap');
console.log();

// Executar a atualização imediatamente na inicialização
log('Inicializando agendador...');
runUpdateScript();

// Agendar para executar a cada 6 horas
cron.schedule('0 */6 * * *', () => {
    log('Executando atualização agendada...');
    runUpdateScript();
});

log('Agendador inicializado! O roadmap será atualizado a cada 6 horas.');
console.log();
console.log('Pressione Ctrl+C para parar o agendador.');
console.log('✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧'); 