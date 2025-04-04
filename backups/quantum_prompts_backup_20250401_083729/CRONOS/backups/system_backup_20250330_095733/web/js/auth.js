class QuantumAuth {
    constructor() {
        this.authModal = new bootstrap.Modal(document.getElementById('authModal'));
        this.authForm = document.getElementById('authForm');
        this.clientIdInput = document.getElementById('clientId');
        this.subsystemSelect = document.getElementById('subsystem');
        this.token = null;
        this.authenticated = false;

        this.setupEventListeners();
        this.showAuthModal();
    }

    setupEventListeners() {
        this.authForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.authenticate();
        });

        // Handle token expiration
        metadataClient.onConnectionChange((connected) => {
            if (!connected && this.authenticated) {
                this.handleTokenExpiration();
            }
        });
    }

    showAuthModal() {
        // Generate a unique client ID if not present
        if (!this.clientIdInput.value) {
            this.clientIdInput.value = `client_${Math.random().toString(36).substr(2, 9)}`;
        }
        this.authModal.show();
    }

    async authenticate() {
        const clientId = this.clientIdInput.value;
        const subsystem = this.subsystemSelect.value;

        try {
            // Request authentication from server
            const response = await metadataClient.authenticate(clientId, subsystem);

            if (response.token) {
                this.token = response.token;
                this.authenticated = true;
                this.authModal.hide();

                // Add authentication event to timeline
                quantumTimeline.addEvent('security', `Authenticated with ${subsystem}`, {
                    clientId,
                    subsystem
                });

                // Update connection status
                document.querySelector('.websocket-status .status-text').textContent =
                    `Connected to ${subsystem} (${clientId})`;

                // Store auth info in session storage
                sessionStorage.setItem('quantum_auth', JSON.stringify({
                    clientId,
                    subsystem,
                    token: this.token
                }));
            }
        } catch (error) {
            this.handleAuthError(error);
        }
    }

    handleAuthError(error) {
        quantumTimeline.addEvent('error', 'Authentication failed', {
            message: error.message
        });

        // Show error in modal
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger mt-3';
        errorAlert.textContent = `Authentication failed: ${error.message}`;

        const existingAlert = this.authForm.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        this.authForm.appendChild(errorAlert);
    }

    handleTokenExpiration() {
        this.authenticated = false;
        this.token = null;

        quantumTimeline.addEvent('security', 'Authentication token expired');

        // Clear stored auth info
        sessionStorage.removeItem('quantum_auth');

        // Show auth modal
        this.showAuthModal();
    }

    getToken() {
        return this.token;
    }

    isAuthenticated() {
        return this.authenticated;
    }

    // Try to restore previous session
    async restoreSession() {
        const storedAuth = sessionStorage.getItem('quantum_auth');
        if (storedAuth) {
            const auth = JSON.parse(storedAuth);
            this.clientIdInput.value = auth.clientId;
            this.subsystemSelect.value = auth.subsystem;

            try {
                await this.authenticate();
                return true;
            } catch (error) {
                console.error('Failed to restore session:', error);
                return false;
            }
        }
        return false;
    }
}

// Initialize authentication
const quantumAuth = new QuantumAuth();

// Try to restore previous session
quantumAuth.restoreSession().then(restored => {
    if (!restored) {
        quantumAuth.showAuthModal();
    }
});
