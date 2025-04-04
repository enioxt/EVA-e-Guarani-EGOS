// EVA & GUARANI - Metadata System Client

class MetadataClient {
    constructor() {
        this.ws = null;
        this.callbacks = new Map();
        this.connect();
    }

    connect() {
        this.ws = new WebSocket('ws://localhost:8081');

        this.ws.onopen = () => {
            console.log('Connected to metadata server');
            this.trigger('connected');
        };

        this.ws.onclose = () => {
            console.log('Disconnected from metadata server');
            this.trigger('disconnected');
            // Try to reconnect after 5 seconds
            setTimeout(() => this.connect(), 5000);
        };

        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            } catch (e) {
                console.error('Error parsing message:', e);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.trigger('error', error);
        };
    }

    handleMessage(message) {
        const { type, data, timestamp } = message;

        switch (type) {
            case 'quantum_update':
                this.trigger('quantum_update', data);
                break;
            case 'metadata_update':
                this.trigger('metadata_update', data);
                break;
            default:
                console.warn('Unknown message type:', type);
        }
    }

    send(type, data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            const message = {
                type,
                data,
                timestamp: new Date().toISOString()
            };
            this.ws.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket not connected');
        }
    }

    on(event, callback) {
        if (!this.callbacks.has(event)) {
            this.callbacks.set(event, new Set());
        }
        this.callbacks.get(event).add(callback);
    }

    off(event, callback) {
        if (this.callbacks.has(event)) {
            this.callbacks.get(event).delete(callback);
        }
    }

    trigger(event, data) {
        if (this.callbacks.has(event)) {
            for (const callback of this.callbacks.get(event)) {
                try {
                    callback(data);
                } catch (e) {
                    console.error('Error in callback:', e);
                }
            }
        }
    }
}

// Export for use in other modules
window.MetadataClient = MetadataClient;

// Initialize the client
const metadataClient = new MetadataClient();

// Connect when the page loads
document.addEventListener('DOMContentLoaded', () => {
    metadataClient.connect();
});

// Reconnect when the page becomes visible
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && !metadataClient.connected) {
        metadataClient.connect();
    }
});

// Example usage:
metadataClient.onQuantumStateUpdate((data) => {
    console.log('Quantum state update:', data);
});

metadataClient.onSubsystemStateUpdate((data) => {
    console.log('Subsystem state update:', data);
});

metadataClient.onConnectionChange((connected) => {
    console.log('Connection change:', connected);
});
