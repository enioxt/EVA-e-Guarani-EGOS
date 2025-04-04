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
 * EVA & GUARANI - Dynamic Roadmap Updater
 * ✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧
 *
 * Este script atualiza automaticamente o roadmap com base nas alterações
 * detectadas nos arquivos do projeto, mantendo uma documentação viva.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configurações
const BASE_DIR = process.env.EVA_GUARANI_DIR || path.resolve(__dirname, '..');
const MASTER_DIR = path.join(BASE_DIR, 'QUANTUM_PROMPTS', 'MASTER');
const ROADMAP_FILE = path.join(MASTER_DIR, 'quantum_roadmap.md');
const CHANGELOG_FILE = path.join(BASE_DIR, 'logs', 'roadmap_updates.log');

// Garantir que o diretório de logs existe
const logsDir = path.join(BASE_DIR, 'logs');
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
}

// Configuração de cores para o console
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
        white: '\x1b[37m'
    },
    bg: {
        black: '\x1b[40m',
        red: '\x1b[41m',
        green: '\x1b[42m',
        yellow: '\x1b[43m',
        blue: '\x1b[44m',
        magenta: '\x1b[45m',
        cyan: '\x1b[46m',
        white: '\x1b[47m'
    }
};

/**
 * Registra uma mensagem no console e no arquivo de log
 * @param {string} message - Mensagem a ser registrada
 * @param {string} level - Nível de log (info, warn, error)
 */
function log(message, level = 'info') {
    const timestamp = new Date().toISOString();
    let coloredMessage = '';

    switch (level) {
        case 'info':
            coloredMessage = `${colors.fg.green}[INFO]${colors.reset} ${message}`;
            break;
        case 'warn':
            coloredMessage = `${colors.fg.yellow}[WARN]${colors.reset} ${message}`;
            break;
        case 'error':
            coloredMessage = `${colors.fg.red}[ERROR]${colors.reset} ${message}`;
            break;
        default:
            coloredMessage = `[${level.toUpperCase()}] ${message}`;
    }

    console.log(coloredMessage);

    // Adicionar ao arquivo de log
    if (fs.existsSync(CHANGELOG_FILE)) {
        fs.appendFileSync(CHANGELOG_FILE, `${timestamp} [${level.toUpperCase()}] ${message}\n`);
    } else {
        fs.writeFileSync(CHANGELOG_FILE, `${timestamp} [${level.toUpperCase()}] ${message}\n`);
    }
}

/**
 * Obtém as últimas alterações no repositório
 * @returns {Array} Lista de arquivos alterados
 */
function getRecentChanges() {
    try {
        const output = execSync('git diff --name-only HEAD~5 HEAD', { encoding: 'utf-8' });
        return output.split('\n').filter(line => line.trim() !== '');
    } catch (error) {
        log(`Erro ao obter alterações recentes: ${error.message}`, 'error');
        return [];
    }
}

/**
 * Analisa os arquivos recentemente alterados para entender o progresso
 * @param {Array} changedFiles - Lista de arquivos alterados
 * @returns {Object} Informações sobre o progresso
 */
function analyzeProgress(changedFiles) {
    const progress = {
        subsystems: {
            MASTER: { changes: 0 },
            ATLAS: { changes: 0 },
            NEXUS: { changes: 0 },
            CRONOS: { changes: 0 },
            ETHIK: { changes: 0 },
            SLOP: { changes: 0 },
            MYCELIUM: { changes: 0 }
        },
        totalChanges: changedFiles.length,
        categories: {
            documentation: 0,
            code: 0,
            tests: 0,
            configuration: 0
        }
    };

    // Categorizar as alterações
    changedFiles.forEach(file => {
        // Identificar o subsistema
        if (file.includes('MASTER')) {
            progress.subsystems.MASTER.changes++;
        } else if (file.includes('ATLAS')) {
            progress.subsystems.ATLAS.changes++;
        } else if (file.includes('NEXUS')) {
            progress.subsystems.NEXUS.changes++;
        } else if (file.includes('CRONOS')) {
            progress.subsystems.CRONOS.changes++;
        } else if (file.includes('ETHIK')) {
            progress.subsystems.ETHIK.changes++;
        } else if (file.includes('slop')) {
            progress.subsystems.SLOP.changes++;
        } else if (file.includes('mycelium')) {
            progress.subsystems.MYCELIUM.changes++;
        }

        // Categorizar por tipo
        if (file.endsWith('.md') || file.includes('doc')) {
            progress.categories.documentation++;
        } else if (file.includes('test') || file.endsWith('.test.js') || file.endsWith('_test.py')) {
            progress.categories.tests++;
        } else if (file.endsWith('.json') || file.endsWith('.yml') || file.endsWith('.config')) {
            progress.categories.configuration++;
        } else {
            progress.categories.code++;
        }
    });

    return progress;
}

/**
 * Atualiza o roadmap com base nas alterações analisadas
 * @param {Object} progress - Informações sobre o progresso
 */
function updateRoadmap(progress) {
    // Carregar o roadmap atual
    if (!fs.existsSync(ROADMAP_FILE)) {
        log(`Arquivo de roadmap não encontrado em ${ROADMAP_FILE}`, 'error');
        return;
    }

    let roadmapContent = fs.readFileSync(ROADMAP_FILE, 'utf-8');

    // Atualizar a data da última atualização
    const date = new Date().toLocaleDateString('pt-BR');
    roadmapContent = roadmapContent.replace(
        /\*\*Última atualização:\*\* .*$/m,
        `**Última atualização:** ${date}`
    );

    // Salvar o roadmap atualizado
    fs.writeFileSync(ROADMAP_FILE, roadmapContent);

    log(`Roadmap atualizado com sucesso!`, 'info');
    log(`Total de alterações analisadas: ${progress.totalChanges}`, 'info');
    log(`Alterações por subsistema: MASTER (${progress.subsystems.MASTER.changes}), ATLAS (${progress.subsystems.ATLAS.changes}), NEXUS (${progress.subsystems.NEXUS.changes}), CRONOS (${progress.subsystems.CRONOS.changes}), ETHIK (${progress.subsystems.ETHIK.changes}), SLOP (${progress.subsystems.SLOP.changes}), MYCELIUM (${progress.subsystems.MYCELIUM.changes})`, 'info');
}

/**
 * Função principal
 */
function main() {
    console.log(`${colors.fg.magenta}✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧${colors.reset}`);
    console.log(`${colors.fg.cyan}Dynamic Roadmap Updater${colors.reset}`);
    console.log();

    log('Iniciando atualização do roadmap...', 'info');

    // Obter alterações recentes
    const changedFiles = getRecentChanges();
    if (changedFiles.length === 0) {
        log('Nenhuma alteração recente encontrada.', 'warn');
        return;
    }

    log(`Encontradas ${changedFiles.length} alterações recentes.`, 'info');

    // Analisar o progresso
    const progress = analyzeProgress(changedFiles);

    // Atualizar o roadmap
    updateRoadmap(progress);

    console.log();
    console.log(`${colors.fg.magenta}✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧${colors.reset}`);
}

// Executar o script
main();
