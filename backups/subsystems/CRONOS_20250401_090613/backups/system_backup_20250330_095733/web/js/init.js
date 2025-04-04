// Initialize Metadata Client
document.addEventListener('DOMContentLoaded', () => {
    const terminal = document.getElementById('system-terminal');
    const statusIndicator = document.querySelector('.websocket-status .status-indicator');
    const statusText = document.querySelector('.websocket-status .status-text');

    // Initialize metadata client
    const client = new MetadataClient('ws://localhost:8080/metadata');

    // Update quantum metrics
    client.onQuantumUpdate((metrics) => {
        document.getElementById('quantum-consciousness').textContent = metrics.consciousness.toFixed(3);
        document.getElementById('quantum-love').textContent = metrics.love.toFixed(3);
        document.getElementById('quantum-divine-spark').textContent = metrics.divineSpark.toFixed(3);
        document.getElementById('quantum-ethics').textContent = metrics.ethics.toFixed(3);
    });

    // Update connection status
    client.onConnectionChange((status) => {
        statusIndicator.className = `status-indicator status-${status}`;
        statusText.textContent = status === 'online' ? 'Connected' : 'Disconnected';

        // Log to terminal
        const timestamp = new Date().toLocaleTimeString();
        terminal.innerHTML += `\n[${timestamp}] WebSocket ${status === 'online' ? 'connected' : 'disconnected'}`;
        terminal.scrollTop = terminal.scrollHeight;
    });

    // Handle metadata updates
    client.onMetadataUpdate((metadata) => {
        const timestamp = new Date().toLocaleTimeString();
        terminal.innerHTML += `\n[${timestamp}] Metadata updated: ${metadata.path}`;
        terminal.scrollTop = terminal.scrollHeight;
    });

    // Connect to WebSocket server
    client.connect().catch(error => {
        console.error('Failed to connect:', error);
        terminal.innerHTML += `\nError connecting to WebSocket server: ${error.message}`;
    });
});
