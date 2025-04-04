function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

class QuantumTimeline {
    constructor() {
        this.timeline = document.getElementById('eventTimeline');
        this.maxEvents = 100;
        this.events = [];

        this.eventTypes = {
            connection: {
                icon: '🔌',
                color: '#4caf50'
            },
            quantum: {
                icon: '⚛️',
                color: '#2196f3'
            },
            subsystem: {
                icon: '🔧',
                color: '#ff9800'
            },
            security: {
                icon: '🔒',
                color: '#f44336'
            },
            analysis: {
                icon: '📊',
                color: '#9c27b0'
            },
            error: {
                icon: '⚠️',
                color: '#f44336'
            }
        };

        this.setupEventListeners();
    }

    setupEventListeners() {
        // Listen for connection changes
        metadataClient.onConnectionChange((connected) => {
            this.addEvent('connection', connected ? 'Connected to quantum system' : 'Disconnected from quantum system');
        });

        // Listen for quantum state updates
        metadataClient.onQuantumStateUpdate((data) => {
            this.addEvent('quantum', 'Quantum state updated', {
                consciousness: data.consciousness,
                love: data.love,
                divineSpark: data.divineSpark
            });
        });

        // Listen for subsystem updates
        metadataClient.onSubsystemStateUpdate((data) => {
            this.addEvent('subsystem', `${data.subsystem} state updated`, {
                status: data.data.status,
                metrics: Object.entries(data.data)
                    .filter(([k, v]) => typeof v === 'number')
                    .map(([k, v]) => `${k}: ${v.toFixed(3)}`)
                    .join(', ')
            });
        });
    }

    addEvent(type, message, details = null) {
        const event = {
            id: crypto.randomUUID(),
            timestamp: new Date(),
            type,
            message,
            details
        };

        this.events.unshift(event);
        if (this.events.length > this.maxEvents) {
            this.events.pop();
        }

        this.renderEvent(event);
        this.cleanOldEvents();
    }

    renderEvent(event) {
        const eventElement = document.createElement('div');
        eventElement.className = 'timeline-event';
        eventElement.id = `event-${event.id}`;

        const typeInfo = this.eventTypes[event.type];

        eventElement.innerHTML = `
            <div class="event-icon" style="background-color: ${typeInfo.color}">
                ${typeInfo.icon}
            </div>
            <div class="event-content">
                <div class="event-header">
                    <span class="event-timestamp">${event.timestamp.toLocaleTimeString()}</span>
                    <span class="event-type">${event.type}</span>
                </div>
                <div class="event-message">${escapeHtml(event.message)}</div>
                ${event.details ? `
                    <div class="event-details">
                        <button class="btn btn-sm btn-link" onclick="quantumTimeline.toggleDetails('${event.id}')">
                            Details
                        </button>
                        <div class="details-content" id="details-${event.id}" style="display: none">
                            <pre>${escapeHtml(JSON.stringify(event.details, null, 2))}</pre>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        // Add with fade-in animation
        eventElement.style.opacity = '0';
        this.timeline.insertBefore(eventElement, this.timeline.firstChild);
        requestAnimationFrame(() => {
            eventElement.style.opacity = '1';
        });
    }

    toggleDetails(eventId) {
        const detailsElement = document.getElementById(`details-${eventId}`);
        if (detailsElement) {
            const isHidden = detailsElement.style.display === 'none';
            detailsElement.style.display = isHidden ? 'block' : 'none';

            if (isHidden) {
                detailsElement.style.maxHeight = '0';
                requestAnimationFrame(() => {
                    detailsElement.style.maxHeight = detailsElement.scrollHeight + 'px';
                });
            } else {
                detailsElement.style.maxHeight = '0';
            }
        }
    }

    cleanOldEvents() {
        const events = this.timeline.getElementsByClassName('timeline-event');
        while (events.length > this.maxEvents) {
            const oldEvent = events[events.length - 1];
            oldEvent.style.opacity = '0';
            setTimeout(() => oldEvent.remove(), 300);
        }
    }

    clear() {
        this.events = [];
        this.timeline.innerHTML = '';
    }
}

// Initialize timeline
const quantumTimeline = new QuantumTimeline();
