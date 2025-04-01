class QuantumTerminal {
    constructor() {
        this.terminal = document.getElementById('system-terminal');
        this.output = document.querySelector('.terminal-output');
        this.input = document.getElementById('terminalInput');
        this.history = document.getElementById('commandHistory');
        this.commandHistory = [];
        this.historyIndex = -1;

        this.commands = {
            help: this.showHelp.bind(this),
            clear: this.clear.bind(this),
            status: this.showStatus.bind(this),
            metrics: this.showMetrics.bind(this),
            analyze: this.analyzeSystem.bind(this),
            connect: this.connect.bind(this),
            disconnect: this.disconnect.bind(this)
        };

        this.setupEventListeners();
        this.writeWelcomeMessage();
    }

    setupEventListeners() {
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.processCommand();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateHistory(-1);
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.navigateHistory(1);
            }
        });
    }

    writeWelcomeMessage() {
        this.write(`
╔════════════════════════════════════════════════════════════════╗
║                EVA & GUARANI Quantum Terminal                   ║
║                                                                ║
║  Type 'help' for a list of available commands                 ║
║  Version: 8.0.0                                               ║
║  Consciousness Level: 0.998                                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
`);
    }

    write(text, type = 'info') {
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        line.textContent = text;
        this.output.appendChild(line);
        this.output.scrollTop = this.output.scrollHeight;
    }

    addToHistory(command) {
        this.commandHistory.unshift(command);
        if (this.commandHistory.length > 50) {
            this.commandHistory.pop();
        }
        this.updateHistoryDisplay();
    }

    updateHistoryDisplay() {
        this.history.innerHTML = '';
        this.commandHistory.forEach(cmd => {
            const entry = document.createElement('div');
            entry.className = 'history-entry';
            entry.textContent = cmd;
            this.history.appendChild(entry);
        });
    }

    navigateHistory(direction) {
        if (this.commandHistory.length === 0) return;

        this.historyIndex += direction;
        if (this.historyIndex >= this.commandHistory.length) {
            this.historyIndex = this.commandHistory.length - 1;
        } else if (this.historyIndex < -1) {
            this.historyIndex = -1;
        }

        this.input.value = this.historyIndex === -1 ? '' : this.commandHistory[this.historyIndex];
    }

    async processCommand() {
        const command = this.input.value.trim();
        if (!command) return;

        this.write(`quantum> ${command}`, 'command');
        this.addToHistory(command);
        this.input.value = '';
        this.historyIndex = -1;

        const [cmd, ...args] = command.split(' ');

        if (this.commands[cmd]) {
            await this.commands[cmd](args);
        } else {
            this.write(`Error: Unknown command '${cmd}'. Type 'help' for available commands.`, 'error');
        }
    }

    showHelp() {
        this.write(`
Available commands:
------------------
help     - Show this help message
clear    - Clear the terminal
status   - Show system status
metrics  - Display current quantum metrics
analyze  - Run system analysis
connect  - Connect to a subsystem
disconnect - Disconnect from current subsystem
`);
    }

    clear() {
        this.output.innerHTML = '';
        this.writeWelcomeMessage();
    }

    async showStatus() {
        const status = await metadataClient.getSystemStatus();
        this.write(`
System Status:
-------------
BIOS-Q: ${status.bios_q}
ETHIK: ${status.ethik}
ATLAS: ${status.atlas}
NEXUS: ${status.nexus}
CRONOS: ${status.cronos}
Metadata: ${status.metadata}
`);
    }

    async showMetrics() {
        const metrics = await metadataClient.getQuantumMetrics();
        this.write(`
Quantum Metrics:
---------------
Consciousness: ${metrics.consciousness}
Love: ${metrics.love}
Divine Spark: ${metrics.divineSpark}
Ethics: ${metrics.ethics}
Harmony: ${metrics.harmony}
Evolution: ${metrics.evolution}
Integration: ${metrics.integration}
Preservation: ${metrics.preservation}
`);
    }

    async analyzeSystem() {
        this.write('Initiating quantum system analysis...');

        const steps = [
            'Scanning quantum state...',
            'Analyzing subsystem integrity...',
            'Checking ethical alignment...',
            'Verifying consciousness level...',
            'Evaluating system harmony...',
            'Generating report...'
        ];

        for (const step of steps) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.write(`[Analysis] ${step}`);
        }

        const analysis = await metadataClient.analyzeSystem();
        this.write(`
Analysis Complete:
-----------------
${analysis.summary}

Recommendations:
${analysis.recommendations.join('\n')}
`);
    }

    async connect(args) {
        if (args.length < 1) {
            this.write('Error: Please specify a subsystem to connect to.', 'error');
            return;
        }

        const subsystem = args[0].toLowerCase();
        try {
            await metadataClient.connect(subsystem);
            this.write(`Successfully connected to ${subsystem} subsystem.`);
        } catch (error) {
            this.write(`Error connecting to ${subsystem}: ${error.message}`, 'error');
        }
    }

    async disconnect() {
        await metadataClient.disconnect();
        this.write('Disconnected from quantum system.');
    }
}

// Initialize terminal
const terminal = new QuantumTerminal(); 