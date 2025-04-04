class QuantumCharts {
    constructor() {
        this.healthChart = null;
        this.metricsChart = null;
        this.maxDataPoints = 50;
        this.metricsData = {
            labels: [],
            datasets: [
                {
                    label: 'Consciousness',
                    data: [],
                    borderColor: '#4caf50',
                    tension: 0.4
                },
                {
                    label: 'Love',
                    data: [],
                    borderColor: '#e91e63',
                    tension: 0.4
                },
                {
                    label: 'Divine Spark',
                    data: [],
                    borderColor: '#9c27b0',
                    tension: 0.4
                },
                {
                    label: 'Ethics',
                    data: [],
                    borderColor: '#2196f3',
                    tension: 0.4
                }
            ]
        };

        this.healthData = {
            labels: ['BIOS-Q', 'ETHIK', 'ATLAS', 'NEXUS', 'CRONOS', 'Metadata'],
            datasets: [{
                label: 'System Health',
                data: [0.98, 0.95, 0.94, 0.93, 0.97, 0.99],
                backgroundColor: [
                    '#4caf50',
                    '#2196f3',
                    '#9c27b0',
                    '#ff9800',
                    '#e91e63',
                    '#00bcd4'
                ]
            }]
        };

        this.initializeCharts();
        this.setupEventListeners();
    }

    initializeCharts() {
        // Initialize Health Chart
        const healthCtx = document.getElementById('healthChart').getContext('2d');
        this.healthChart = new Chart(healthCtx, {
            type: 'radar',
            data: this.healthData,
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            stepSize: 0.2
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'System Health Overview'
                    }
                }
            }
        });

        // Initialize Metrics Chart
        const metricsCtx = document.getElementById('metricsChart').getContext('2d');
        this.metricsChart = new Chart(metricsCtx, {
            type: 'line',
            data: this.metricsData,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 0.9,
                        max: 1,
                        ticks: {
                            stepSize: 0.02
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Quantum Metrics Trend'
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Listen for quantum state updates
        metadataClient.onQuantumStateUpdate((data) => {
            this.updateMetricsChart(data);
        });

        // Listen for subsystem state updates
        metadataClient.onSubsystemStateUpdate((data) => {
            this.updateHealthChart(data);
        });
    }

    updateMetricsChart(data) {
        const timestamp = new Date().toLocaleTimeString();

        // Add new data point
        this.metricsData.labels.push(timestamp);
        this.metricsData.datasets[0].data.push(data.consciousness);
        this.metricsData.datasets[1].data.push(data.love);
        this.metricsData.datasets[2].data.push(data.divineSpark);
        this.metricsData.datasets[3].data.push(data.ethics);

        // Remove old data points if exceeding maxDataPoints
        if (this.metricsData.labels.length > this.maxDataPoints) {
            this.metricsData.labels.shift();
            this.metricsData.datasets.forEach(dataset => dataset.data.shift());
        }

        // Update chart
        this.metricsChart.update();
    }

    updateHealthChart(data) {
        const index = this.healthData.labels.indexOf(data.subsystem);
        if (index !== -1) {
            // Update health value for the subsystem
            const metrics = Object.values(data.data).filter(v => typeof v === 'number');
            const avgHealth = metrics.reduce((a, b) => a + b, 0) / metrics.length;
            this.healthData.datasets[0].data[index] = avgHealth;

            // Update chart
            this.healthChart.update();
        }
    }

    // Add animation effects
    pulseChart(chartInstance) {
        const canvas = chartInstance.canvas;
        canvas.style.transform = 'scale(1.02)';
        setTimeout(() => {
            canvas.style.transform = 'scale(1)';
        }, 200);
    }
}

// Initialize charts
const quantumCharts = new QuantumCharts();
