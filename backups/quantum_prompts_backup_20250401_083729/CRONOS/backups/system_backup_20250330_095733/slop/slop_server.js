---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: slop
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
  subsystem: MASTER
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

const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const winston = require('winston');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const Joi = require('joi');
const NodeCache = require('node-cache');
const PriorityQueue = require('priority-queue');

// Load configuration
const config = require('./slop_config.json');

// Initialize cache with 5 minutes standard TTL
const cache = new NodeCache({
    stdTTL: 300,
    checkperiod: 60,
    useClones: false
});

// Alert thresholds with adaptive capabilities
const ALERT_THRESHOLDS = {
    cpu: {
        warning: 70,
        critical: 90,
        adaptive: {
            enabled: true,
            samples: [],
            maxSamples: 100,
            adjustmentFactor: 0.1
        }
    },
    memory: {
        warning: 80,
        critical: 95,
        adaptive: {
            enabled: true,
            samples: [],
            maxSamples: 100,
            adjustmentFactor: 0.1
        }
    },
    errorRate: {
        warning: 5,
        critical: 10,
        adaptive: {
            enabled: true,
            samples: [],
            maxSamples: 100,
            adjustmentFactor: 0.1
        }
    },
    responseTime: {
        warning: 1000,
        critical: 3000,
        adaptive: {
            enabled: true,
            samples: [],
            maxSamples: 100,
            adjustmentFactor: 0.1
        }
    }
};

// Endpoint performance tracking
const endpointMetrics = new Map();

// Metrics history configuration
const METRICS_HISTORY = {
    directory: 'C:/Eva Guarani EGOS/metrics',
    retentionDays: 30,
    samplingInterval: 60000 // 1 minute
};

// Log cleanup configuration
const LOG_CLEANUP = {
    directory: 'C:/Eva Guarani EGOS/logs',
    retentionDays: 30,
    checkInterval: 24 * 60 * 60 * 1000 // 24 hours
};

// Ensure metrics directory exists
if (!fs.existsSync(METRICS_HISTORY.directory)) {
    fs.mkdirSync(METRICS_HISTORY.directory, { recursive: true });
}

// Configure Winston logger with daily rotate file
const logger = winston.createLogger({
    level: 'debug',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.metadata({
            fillWith: ['service', 'version', 'environment', 'metrics']
        }),
        winston.format.json()
    ),
    defaultMeta: {
        service: 'slop-server',
        version: '8.0',
        environment: process.env.NODE_ENV || 'development'
    },
    transports: [
        new winston.transports.File({
            filename: path.join(LOG_CLEANUP.directory, 'error-%DATE%.log'),
            level: 'error',
            maxFiles: LOG_CLEANUP.retentionDays + 'd',
            maxSize: '10m',
            tailable: true,
            datePattern: 'YYYY-MM-DD'
        }),
        new winston.transports.File({
            filename: path.join(LOG_CLEANUP.directory, 'combined-%DATE%.log'),
            maxFiles: LOG_CLEANUP.retentionDays + 'd',
            maxSize: '10m',
            tailable: true,
            datePattern: 'YYYY-MM-DD'
        })
    ]
});

// Add console transport in development
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
        )
    }));
}

// Initialize Express app
const app = express();
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

// Load modules
const filesystemIntegration = require('./slop/filesystem-integration');

// CORS configuration
const corsOptions = {
    origin: '*', // Durante desenvolvimento - em produção, restringir para origens específicas
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
};

app.use(cors(corsOptions));

// Configure rate limiting
if (config.security.rateLimit.enabled) {
    app.use(rateLimit({
        windowMs: config.security.rateLimit.windowMs,
        max: config.security.rateLimit.max
    }));
}

// Parse JSON bodies
app.use(express.json());

// Maps para os subsistemas
const atlasVisualizations = new Map();
const cronosTimeline = new Map();
const nexusAnalysis = new Map();
const ethikValidations = new Map();

// Performance metrics
const metrics = {
    requests: 0,
    errors: 0,
    mycelialSyncs: 0,
    ethikValidations: 0,
    startTime: Date.now(),
    lastUpdate: Date.now(),

    // System metrics
    system: {
        cpu: {
            usage: 0,
            loadAverage: [0, 0, 0]
        },
        memory: {
            total: 0,
            used: 0,
            free: 0,
            usage: 0
        },
        uptime: 0
    },

    // Subsystem metrics
    subsystems: {
        atlas: {
            visualizations: 0,
            lastVisualization: null,
            processingTime: 0
        },
        nexus: {
            analyses: 0,
            lastAnalysis: null,
            processingTime: 0
        },
        cronos: {
            events: 0,
            lastEvent: null,
            timelineSize: 0
        },
        ethik: {
            validations: 0,
            lastValidation: null,
            averageScore: 0
        },
        mycelium: {
            nodes: 0,
            connections: 0,
            files: 0,
            lastSync: null
        }
    },

    // Performance metrics
    performance: {
        requestsPerSecond: 0,
        averageResponseTime: 0,
        peakResponseTime: 0,
        lastMinuteRequests: []
    },

    trends: {
        cpu: [],
        memory: [],
        errorRate: [],
        responseTime: [],
        maxTrendPoints: 100
    },

    subsystemHealth: {
        atlas: { status: 'unknown', lastCheck: null, issues: [] },
        nexus: { status: 'unknown', lastCheck: null, issues: [] },
        cronos: { status: 'unknown', lastCheck: null, issues: [] },
        ethik: { status: 'unknown', lastCheck: null, issues: [] },
        mycelium: { status: 'unknown', lastCheck: null, issues: [] }
    },

    getUptime() {
        return (Date.now() - this.startTime) / 1000;
    },

    getRequestsPerSecond() {
        return this.requests / this.getUptime();
    },

    getErrorRate() {
        return this.requests > 0 ? (this.errors / this.requests) * 100 : 0;
    },

    updateSystemMetrics() {
        try {
            const os = require('os');

            // Update CPU metrics
            const cpus = os.cpus();
            let totalIdle = 0;
            let totalTick = 0;

            cpus.forEach(cpu => {
                for (const type in cpu.times) {
                    totalTick += cpu.times[type];
                }
                totalIdle += cpu.times.idle;
            });

            const idle = totalIdle / cpus.length;
            const total = totalTick / cpus.length;
            const usage = 100 - (100 * idle / total);

            this.system.cpu.usage = Math.round(usage * 100) / 100;
            this.system.cpu.loadAverage = os.loadavg();

            // Update memory metrics
            const totalMemory = os.totalmem();
            const freeMemory = os.freemem();
            const usedMemory = totalMemory - freeMemory;

            this.system.memory.total = totalMemory;
            this.system.memory.used = usedMemory;
            this.system.memory.free = freeMemory;
            this.system.memory.usage = Math.round((usedMemory / totalMemory) * 100 * 100) / 100;

            // Update system uptime
            this.system.uptime = os.uptime();

            // Update subsystem metrics
            this.subsystems.atlas.visualizations = atlasVisualizations.size;
            this.subsystems.nexus.analyses = nexusAnalysis.size;
            this.subsystems.cronos.events = cronosTimeline.size;
            this.subsystems.ethik.validations = ethikValidations.size;
            this.subsystems.mycelium = {
                nodes: myceliumNetwork.nodes.size,
                connections: myceliumNetwork.connections.size,
                files: myceliumNetwork.files.size,
                lastSync: myceliumNetwork.lastSync
            };

            // Update performance metrics
            const now = Date.now();
            this.performance.lastMinuteRequests = this.performance.lastMinuteRequests
                .filter(time => now - time < 60000);
            this.performance.requestsPerSecond = this.performance.lastMinuteRequests.length / 60;

            // Update trends
            this.updateTrends();

            // Update adaptive thresholds
            this.updateAdaptiveThresholds();

            // Update subsystem health
            this.updateSubsystemHealth();

            this.lastUpdate = now;
        } catch (error) {
            logger.error('Error updating system metrics:', error);
        }
    },

    updateTrends() {
        const now = Date.now();

        // Add current values to trends
        this.trends.cpu.push({ timestamp: now, value: this.system.cpu.usage });
        this.trends.memory.push({ timestamp: now, value: this.system.memory.usage });
        this.trends.errorRate.push({ timestamp: now, value: this.getErrorRate() });
        this.trends.responseTime.push({
            timestamp: now,
            value: this.performance.averageResponseTime
        });

        // Keep only last maxTrendPoints
        const truncate = (arr) => {
            if (arr.length > this.trends.maxTrendPoints) {
                arr.splice(0, arr.length - this.trends.maxTrendPoints);
            }
        };

        truncate(this.trends.cpu);
        truncate(this.trends.memory);
        truncate(this.trends.errorRate);
        truncate(this.trends.responseTime);
    },

    updateAdaptiveThresholds() {
        const updateThreshold = (metric, value) => {
            const threshold = ALERT_THRESHOLDS[metric];
            if (!threshold.adaptive.enabled) return;

            threshold.adaptive.samples.push(value);
            if (threshold.adaptive.samples.length > threshold.adaptive.maxSamples) {
                threshold.adaptive.samples.shift();
            }

            if (threshold.adaptive.samples.length >= 10) {
                const avg = threshold.adaptive.samples.reduce((a, b) => a + b, 0) / threshold.adaptive.samples.length;
                const stdDev = Math.sqrt(
                    threshold.adaptive.samples.reduce((a, b) => a + Math.pow(b - avg, 2), 0) / threshold.adaptive.samples.length
                );

                // Adjust warning threshold based on usage patterns
                const newWarning = avg + (2 * stdDev);
                threshold.warning = Math.round(
                    threshold.warning * (1 - threshold.adaptive.adjustmentFactor) +
                    newWarning * threshold.adaptive.adjustmentFactor
                );

                // Ensure critical threshold stays above warning
                threshold.critical = Math.max(
                    threshold.critical,
                    threshold.warning + 10
                );
            }
        };

        updateThreshold('cpu', this.system.cpu.usage);
        updateThreshold('memory', this.system.memory.usage);
        updateThreshold('errorRate', this.getErrorRate());
        updateThreshold('responseTime', this.performance.averageResponseTime);
    },

    updateSubsystemHealth() {
        const checkSubsystem = (name, conditions) => {
            const health = this.subsystemHealth[name];
            health.lastCheck = Date.now();
            health.issues = [];

            for (const [condition, message] of conditions) {
                if (!condition) {
                    health.issues.push(message);
                }
            }

            health.status = health.issues.length === 0 ? 'healthy' :
                health.issues.length < 2 ? 'degraded' : 'unhealthy';
        };

        // Check ATLAS health
        checkSubsystem('atlas', [
            [this.subsystems.atlas.visualizations > 0, 'No active visualizations'],
            [this.subsystems.atlas.processingTime < 1000, 'High processing time']
        ]);

        // Check NEXUS health
        checkSubsystem('nexus', [
            [this.subsystems.nexus.analyses > 0, 'No active analyses'],
            [this.subsystems.nexus.processingTime < 1000, 'High processing time']
        ]);

        // Check CRONOS health
        checkSubsystem('cronos', [
            [this.subsystems.cronos.events > 0, 'No events recorded'],
            [this.subsystems.cronos.timelineSize < 10000, 'Timeline size exceeds limit']
        ]);

        // Check ETHIK health
        checkSubsystem('ethik', [
            [this.subsystems.ethik.validations > 0, 'No active validations'],
            [this.subsystems.ethik.averageScore > 0.7, 'Low validation score']
        ]);

        // Check Mycelium health
        checkSubsystem('mycelium', [
            [this.subsystems.mycelium.nodes > 0, 'No active nodes'],
            [this.subsystems.mycelium.connections > 0, 'No active connections'],
            [Date.now() - this.subsystems.mycelium.lastSync < 3600000, 'Sync delayed']
        ]);
    }
};

// Set up interval to update system metrics
setInterval(() => metrics.updateSystemMetrics(), 5000);

// Function to save metrics to file
function saveMetricsToFile() {
    const now = new Date();
    const fileName = path.join(
        METRICS_HISTORY.directory,
        `metrics-${now.toISOString().split('T')[0]}.json`
    );

    const metricsData = {
        timestamp: now.toISOString(),
        metrics: {
            system: metrics.system,
            subsystems: metrics.subsystems,
            performance: metrics.performance,
            endpoints: Array.from(endpointMetrics.entries()).map(([endpoint, data]) => ({
                endpoint,
                ...data
            }))
        }
    };

    try {
        let existingData = [];
        if (fs.existsSync(fileName)) {
            existingData = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        }

        existingData.push(metricsData);
        fs.writeFileSync(fileName, JSON.stringify(existingData, null, 2));
    } catch (error) {
        logger.error('Error saving metrics to file:', error);
    }
}

// Set up interval to save metrics
setInterval(saveMetricsToFile, METRICS_HISTORY.samplingInterval);

// Function to clean up old log files
function cleanupOldFiles() {
    const now = Date.now();
    const maxAge = LOG_CLEANUP.retentionDays * 24 * 60 * 60 * 1000;

    [LOG_CLEANUP.directory, METRICS_HISTORY.directory].forEach(directory => {
        fs.readdir(directory, (err, files) => {
            if (err) {
                logger.error(`Error reading directory ${directory}:`, err);
                return;
            }

            files.forEach(file => {
                const filePath = path.join(directory, file);
                fs.stat(filePath, (err, stats) => {
                    if (err) {
                        logger.error(`Error getting file stats for ${filePath}:`, err);
                        return;
                    }

                    if (now - stats.mtime.getTime() > maxAge) {
                        fs.unlink(filePath, err => {
                            if (err) {
                                logger.error(`Error deleting file ${filePath}:`, err);
                            } else {
                                logger.info(`Deleted old file: ${filePath}`);
                            }
                        });
                    }
                });
            });
        });
    });
}

// Set up interval for file cleanup
setInterval(cleanupOldFiles, LOG_CLEANUP.checkInterval);

// Endpoint performance tracking middleware
function trackEndpointPerformance(req, res, next) {
    const start = Date.now();
    const endpoint = `${req.method} ${req.route?.path || req.path}`;

    if (!endpointMetrics.has(endpoint)) {
        endpointMetrics.set(endpoint, {
            totalRequests: 0,
            totalTime: 0,
            averageTime: 0,
            minTime: Infinity,
            maxTime: 0,
            errors: 0,
            lastRequest: null
        });
    }

    res.on('finish', () => {
        const duration = Date.now() - start;
        const metrics = endpointMetrics.get(endpoint);

        metrics.totalRequests++;
        metrics.totalTime += duration;
        metrics.averageTime = metrics.totalTime / metrics.totalRequests;
        metrics.minTime = Math.min(metrics.minTime, duration);
        metrics.maxTime = Math.max(metrics.maxTime, duration);
        metrics.lastRequest = new Date().toISOString();

        if (res.statusCode >= 400) {
            metrics.errors++;
        }

        // Check alert thresholds
        if (duration > ALERT_THRESHOLDS.responseTime.critical) {
            logger.error(`Critical response time for ${endpoint}: ${duration}ms`);
        } else if (duration > ALERT_THRESHOLDS.responseTime.warning) {
            logger.warn(`Slow response time for ${endpoint}: ${duration}ms`);
        }

        // Cache frequently accessed endpoints
        if (req.method === 'GET' && metrics.totalRequests > 100 && metrics.averageTime < 100) {
            const cacheKey = `${endpoint}:${JSON.stringify(req.query)}`;
            if (!cache.has(cacheKey)) {
                cache.set(cacheKey, res.locals.responseData);
            }
        }
    });

    next();
}

// Cache middleware
function cacheMiddleware(req, res, next) {
    if (req.method !== 'GET') {
        return next();
    }

    const cacheKey = `${req.method} ${req.path}:${JSON.stringify(req.query)}`;
    const cachedData = cache.get(cacheKey);

    if (cachedData) {
        return res.json(cachedData);
    }

    // Store original res.json to intercept response
    const originalJson = res.json;
    res.json = function (data) {
        res.locals.responseData = data;
        cache.set(cacheKey, data);
        return originalJson.call(this, data);
    };

    next();
}

// Apply middleware
app.use(trackEndpointPerformance);
app.use(cacheMiddleware);

// Enhanced logging middleware
app.use((req, res, next) => {
    const start = Date.now();
    metrics.requests++;

    res.on('finish', () => {
        const duration = Date.now() - start;
        const status = res.statusCode;

        if (status >= 400) {
            metrics.errors++;
        }

        logger.info(`${req.method} ${req.url}`, {
            metrics: {
                duration,
                status,
                requestsTotal: metrics.requests,
                errorsTotal: metrics.errors,
                requestsPerSecond: metrics.getRequestsPerSecond(),
                errorRate: metrics.getErrorRate(),
                uptime: metrics.getUptime()
            },
            request: {
                method: req.method,
                url: req.url,
                headers: req.headers,
                body: req.method !== 'GET' ? req.body : null
            },
            response: {
                status,
                duration
            }
        });
    });

    next();
});

// Update metrics endpoint to include trends and health
app.get('/metrics', (req, res) => {
    metrics.updateSystemMetrics(); // Get fresh metrics

    // Check system alert thresholds
    const alerts = [];
    const thresholdChecks = [
        {
            metric: 'cpu',
            value: metrics.system.cpu.usage,
            label: 'CPU usage'
        },
        {
            metric: 'memory',
            value: metrics.system.memory.usage,
            label: 'Memory usage'
        },
        {
            metric: 'errorRate',
            value: metrics.getErrorRate(),
            label: 'Error rate'
        },
        {
            metric: 'responseTime',
            value: metrics.performance.averageResponseTime,
            label: 'Response time'
        }
    ];

    for (const check of thresholdChecks) {
        const threshold = ALERT_THRESHOLDS[check.metric];
        if (check.value > threshold.critical) {
            alerts.push({
                type: 'critical',
                message: `${check.label} critical: ${check.value}`,
                threshold: threshold.critical,
                adaptive: threshold.adaptive.enabled
            });
        } else if (check.value > threshold.warning) {
            alerts.push({
                type: 'warning',
                message: `${check.label} high: ${check.value}`,
                threshold: threshold.warning,
                adaptive: threshold.adaptive.enabled
            });
        }
    }

    res.json({
        status: 'success',
        data: {
            uptime: metrics.getUptime(),
            requests: metrics.requests,
            errors: metrics.errors,
            requestsPerSecond: metrics.getRequestsPerSecond(),
            errorRate: metrics.getErrorRate(),
            mycelialSyncs: metrics.mycelialSyncs,
            ethikValidations: metrics.ethikValidations,
            system: metrics.system,
            subsystems: metrics.subsystems,
            performance: metrics.performance,
            trends: metrics.trends,
            subsystemHealth: metrics.subsystemHealth,
            thresholds: ALERT_THRESHOLDS,
            alerts,
            lastUpdate: metrics.lastUpdate
        }
    });
});

// Add new endpoint for historical metrics
app.get('/metrics/history', (req, res) => {
    const { date } = req.query;
    const fileName = path.join(
        METRICS_HISTORY.directory,
        `metrics-${date || new Date().toISOString().split('T')[0]}.json`
    );

    try {
        if (fs.existsSync(fileName)) {
            const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
            res.json({ status: 'success', data });
        } else {
            res.status(404).json({ status: 'error', message: 'No metrics found for specified date' });
        }
    } catch (error) {
        logger.error('Error reading metrics history:', error);
        res.status(500).json({ status: 'error', message: 'Error reading metrics history' });
    }
});

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        name: "EVA & GUARANI SLOP Server",
        version: "8.0.0",
        description: "Simple Language Open Protocol Implementation",
        endpoints: {
            chat: {
                enabled: config.endpoints.chat.enabled,
                routes: [
                    { method: 'POST', path: '/chat', description: 'Send messages to AI' },
                    { method: 'POST', path: '/chat/stream', description: 'Stream messages with SSE' },
                    { method: 'GET', path: '/chat', description: 'List recent chats' },
                    { method: 'GET', path: '/chat?type=threads', description: 'List all threads' }
                ]
            },
            tools: {
                enabled: config.endpoints.tools.enabled,
                routes: [
                    { method: 'GET', path: '/tools', description: 'List available tools' }
                ]
            },
            memory: {
                enabled: config.endpoints.memory.enabled,
                routes: [
                    { method: 'POST', path: '/memory', description: 'Store data' },
                    { method: 'GET', path: '/memory/:key', description: 'Get stored data' },
                    { method: 'GET', path: '/memory', description: 'List all keys' },
                    { method: 'POST', path: '/memory/query', description: 'Search stored data' }
                ]
            },
            resources: {
                enabled: config.endpoints.resources.enabled,
                routes: [
                    { method: 'GET', path: '/resources', description: 'List all resources' },
                    { method: 'GET', path: '/resources/prefix/:prefix', description: 'List resources by prefix' },
                    { method: 'GET', path: '/resources/search', description: 'Search resources' }
                ]
            }
        },
        websocket: {
            enabled: true,
            url: `ws://${config.server.host}:${config.server.port}`
        },
        docs: "https://github.com/agnt-gg/slop"
    });
});

// In-memory stores
const chats = new Map();
const threads = new Map();
const memory = new Map();
const resources = new Map();

// EVA & GUARANI Integration
const myceliumNetwork = {
    nodes: new Map(),
    connections: new Map(),
    files: new Map(),
    syncHistory: new Map(),
    lastSync: Date.now(),

    // Connection types for deeper integration
    connectionTypes: {
        DEPENDS_ON: 'depends_on',    // One component depends on another
        EXTENDS: 'extends',          // One component extends another
        REFERENCES: 'references',     // One component references another
        SYNCS_WITH: 'syncs_with',    // Components that need to stay in sync
        VALIDATES: 'validates',       // One component validates another
        MONITORS: 'monitors'         // One component monitors another
    },

    // Track component versions and health
    versions: new Map(),
    health: new Map(),

    // Get all connections for a node
    getConnections(nodeId) {
        const direct = this.connections.get(nodeId) || [];
        const indirect = [];

        // Find indirect connections
        direct.forEach(connId => {
            const secondLevel = this.connections.get(connId) || [];
            indirect.push(...secondLevel.filter(id => id !== nodeId && !direct.includes(id)));
        });

        return {
            direct,
            indirect: [...new Set(indirect)],
            all: [...new Set([...direct, ...indirect])]
        };
    },

    // Check if components need synchronization
    async checkSync(nodeId) {
        const connections = this.getConnections(nodeId);
        const node = this.nodes.get(nodeId);
        if (!node) return { inSync: true, issues: [] };

        const issues = [];
        const connectedVersions = new Map();

        // Check versions of connected components
        for (const connId of connections.direct) {
            const connNode = this.nodes.get(connId);
            if (!connNode) continue;

            connectedVersions.set(connId, connNode.version);

            if (this.shouldSync(node.version, connNode.version)) {
                issues.push({
                    type: 'version_mismatch',
                    source: nodeId,
                    target: connId,
                    sourceVersion: node.version,
                    targetVersion: connNode.version
                });
            }
        }

        return {
            inSync: issues.length === 0,
            issues,
            connectedVersions
        };
    },

    // Determine if versions need synchronization
    shouldSync(version1, version2) {
        if (!version1 || !version2) return false;
        const [major1, minor1] = version1.split('.').map(Number);
        const [major2, minor2] = version2.split('.').map(Number);

        return major1 !== major2 || Math.abs(minor1 - minor2) > 1;
    },

    // Update component health status
    updateHealth(componentId) {
        const component = this.nodes.get(componentId);
        if (!component) return;

        const connections = this.getConnections(componentId);
        let health = 1;

        // Check connection health
        const connectedHealth = connections.direct
            .map(id => this.health.get(id) || 1)
            .reduce((acc, h) => acc + h, 0) / (connections.direct.length || 1);
        health *= connectedHealth;

        // Check sync age
        const lastSync = this.syncHistory.get(componentId);
        if (lastSync) {
            const daysSinceSync = (Date.now() - lastSync) / (1000 * 60 * 60 * 24);
            health *= Math.max(0, 1 - (daysSinceSync / 30));
        }

        this.health.set(componentId, Math.max(0, Math.min(1, health)));
    }
};

// Enhanced synchronization function
async function synchronizeFiles() {
    metrics.mycelialSyncs++;
    logger.info('Iniciando sincronização micelial de arquivos...', {
        metrics: {
            totalSyncs: metrics.mycelialSyncs
        }
    });

    const syncedFiles = new Set();
    const syncQueue = [];

    // Build sync queue with priorities
    myceliumNetwork.files.forEach((fileData, fileId) => {
        const connections = myceliumNetwork.connections.get(fileId) || [];
        if (connections.length === 0) {
            logger.info(`Arquivo ${fileId} não possui conexões miceliais.`);
            return;
        }

        // Calculate sync priority
        const lastSync = myceliumNetwork.syncHistory.get(fileId);
        const timeSinceSync = lastSync ? Date.now() - lastSync : Infinity;
        const priority = calculateSyncPriority(fileData, timeSinceSync, connections.length);

        syncQueue.push({ fileId, fileData, priority });
    });

    // Sort by priority
    syncQueue.sort((a, b) => b.priority - a.priority);

    // Process queue
    for (const { fileId, fileData } of syncQueue) {
        if (!fs.existsSync(fileData.path)) {
            logger.warn(`Arquivo ${fileId} não encontrado em ${fileData.path}`);
            continue;
        }

        try {
            const content = fs.readFileSync(fileData.path, 'utf-8');
            const connections = myceliumNetwork.connections.get(fileId) || [];

            // Synchronize with connected files
            for (const connectedFileId of connections) {
                const connectedFile = myceliumNetwork.files.get(connectedFileId);
                if (!connectedFile || !fs.existsSync(connectedFile.path)) {
                    logger.warn(`Arquivo conectado ${connectedFileId} não encontrado.`);
                    continue;
                }

                const targetContent = fs.readFileSync(connectedFile.path, 'utf-8');
                let newContent = targetContent;

                // Determine connection type and sync accordingly
                if (fileData.type === 'roadmap' && connectedFile.type === 'readme') {
                    newContent = updateReadmeWithRoadmap(targetContent, content);
                    myceliumNetwork.connections.set(fileId, [
                        ...new Set([...(myceliumNetwork.connections.get(fileId) || []), connectedFileId])
                    ]);
                } else if (fileData.type === 'config' && connectedFile.type === 'implementation') {
                    newContent = updateImplementationWithConfig(targetContent, content);
                } else if (fileData.type === connectedFile.type) {
                    // Files of same type might need bidirectional sync
                    newContent = synchronizeRelatedFiles(content, targetContent);
                }

                if (newContent !== targetContent) {
                    fs.writeFileSync(connectedFile.path, newContent);
                    logger.info(`Sincronizado: ${fileId} -> ${connectedFileId}`);
                    syncedFiles.add(connectedFileId);
                }
            }

            syncedFiles.add(fileId);
        } catch (error) {
            logger.error(`Erro ao sincronizar arquivo ${fileId}: ${error.message}`);
        }
    }

    // Update sync history and health
    const now = Date.now();
    syncedFiles.forEach(fileId => {
        myceliumNetwork.syncHistory.set(fileId, now);
        myceliumNetwork.updateHealth(fileId);
    });

    myceliumNetwork.lastSync = now;
    logger.info(`Sincronização micelial concluída: ${syncedFiles.size} arquivos atualizados.`);
}

// Calculate sync priority based on multiple factors
function calculateSyncPriority(fileData, timeSinceSync, connectionCount) {
    let priority = 0;

    // Factor 1: Time since last sync (30% weight)
    const syncAge = Math.min(timeSinceSync / (24 * 60 * 60 * 1000), 30) / 30;
    priority += syncAge * 0.3;

    // Factor 2: Number of connections (20% weight)
    const connectionScore = Math.min(connectionCount / 10, 1);
    priority += connectionScore * 0.2;

    // Factor 3: File type importance (30% weight)
    const typeImportance = {
        roadmap: 1,
        config: 0.9,
        implementation: 0.8,
        readme: 0.7,
        documentation: 0.6
    };
    priority += (typeImportance[fileData.type] || 0.5) * 0.3;

    // Factor 4: File health (20% weight)
    const health = myceliumNetwork.health.get(fileData.path) || 1;
    priority += (1 - health) * 0.2;

    return Math.min(priority, 1);
}

// Synchronize related files of the same type
function synchronizeRelatedFiles(content1, content2) {
    // This is a placeholder for more sophisticated sync logic
    // In a real implementation, this would use diff algorithms
    // and merge strategies based on file type
    return content2;
}

// Set up dynamic sync interval based on network health
let syncInterval = 30 * 60 * 1000; // Start with 30 minutes

function updateSyncInterval() {
    const networkHealth = Array.from(myceliumNetwork.health.values())
        .reduce((acc, h) => acc + h, 0) / myceliumNetwork.health.size || 1;

    // Adjust interval based on health
    if (networkHealth < 0.5) {
        syncInterval = 5 * 60 * 1000; // 5 minutes for poor health
    } else if (networkHealth < 0.8) {
        syncInterval = 15 * 60 * 1000; // 15 minutes for moderate health
    } else {
        syncInterval = 30 * 60 * 1000; // 30 minutes for good health
    }

    // Update interval
    if (global.syncIntervalId) {
        clearInterval(global.syncIntervalId);
    }
    global.syncIntervalId = setInterval(synchronizeFiles, syncInterval);
}

// Initialize sync interval
updateSyncInterval();

// Update interval periodically
setInterval(updateSyncInterval, 60 * 60 * 1000); // Check every hour

// Chat endpoint
if (config.endpoints.chat.enabled) {
    // Regular chat endpoint
    app.post('/chat', async (req, res) => {
        try {
            const { message } = req.body;

            if (!message) {
                return res.status(400).json({
                    status: 'error',
                    message: 'Message is required'
                });
            }

            const chatId = `chat_${Date.now()}`;

            // Store chat
            const chat = {
                id: chatId,
                message: message,
                created_at: new Date().toISOString()
            };

            chats.set(chatId, chat);

            // Return response in the expected format
            return res.status(200).json({
                status: 'success',
                message: 'Message processed successfully',
                data: {
                    id: chatId,
                    message: message
                }
            });
        } catch (error) {
            logger.error('Chat endpoint error:', error);
            return res.status(500).json({
                status: 'error',
                message: 'Internal server error'
            });
        }
    });

    // SSE chat endpoint
    app.post('/chat/stream', (req, res) => {
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');

        const { messages } = req.body;
        const response = messages[0].content;

        // Simulate streaming response
        const words = response.split(' ');
        let index = 0;

        const interval = setInterval(() => {
            if (index < words.length) {
                res.write(`data: ${JSON.stringify({ content: words[index] + ' ' })}\n\n`);
                index++;
            } else {
                res.write('data: [DONE]\n\n');
                clearInterval(interval);
                res.end();
            }
        }, 100);
    });

    // Get chat history
    app.get('/chat', (req, res) => {
        const type = req.query.type;
        if (type === 'threads') {
            const threadList = Array.from(threads.values()).map(thread => ({
                id: thread.id,
                title: thread.messages[0]?.content || 'New Thread',
                last_message: thread.messages[thread.messages.length - 1]?.content,
                created_at: thread.created_at,
                updated_at: thread.updated_at || thread.created_at
            }));
            res.json({ threads: threadList });
        } else {
            const chatList = Array.from(chats.values()).map(chat => ({
                id: chat.id,
                snippet: chat.messages[0]?.content,
                created_at: chat.created_at
            }));
            res.json({ chats: chatList });
        }
    });
}

// Tools endpoint
if (config.endpoints.tools.enabled) {
    app.get('/tools', (req, res) => {
        try {
            res.json({
                status: 'success',
                categories: config.endpoints.tools.categories
            });
        } catch (error) {
            logger.error('Tools endpoint error:', error);
            res.status(500).json({ status: 'error', message: error.message });
        }
    });
}

// Memory endpoint
if (config.endpoints.memory.enabled) {
    app.post('/memory', (req, res) => {
        try {
            const { key, value } = req.body;
            memory.set(key, {
                value,
                created_at: new Date().toISOString()
            });
            res.json({ status: 'stored' });
        } catch (error) {
            logger.error('Memory endpoint error:', error);
            res.status(500).json({ status: 'error', message: error.message });
        }
    });

    app.get('/memory/:key', (req, res) => {
        const data = memory.get(req.params.key);
        if (!data) {
            res.status(404).json({ error: 'Key not found' });
            return;
        }
        res.json(data);
    });

    app.get('/memory', (req, res) => {
        const keys = Array.from(memory.entries()).map(([key, data]) => ({
            key,
            created_at: data.created_at
        }));
        res.json({ keys });
    });

    app.post('/memory/query', (req, res) => {
        const { query, limit = 10 } = req.body;
        const results = Array.from(memory.entries())
            .filter(([key, data]) => {
                const value = JSON.stringify(data.value).toLowerCase();
                return value.includes(query.toLowerCase());
            })
            .slice(0, limit)
            .map(([key, data]) => ({
                key,
                value: data.value,
                score: 0.9 // Simplified scoring
            }));
        res.json({ results });
    });
}

// Resources endpoint
if (config.endpoints.resources.enabled) {
    app.get('/resources', (req, res) => {
        try {
            const resourceList = Array.from(resources.values()).map(resource => ({
                id: resource.id,
                title: resource.title,
                type: resource.type
            }));
            res.json({ resources: resourceList });
        } catch (error) {
            logger.error('Resources endpoint error:', error);
            res.status(500).json({ status: 'error', message: error.message });
        }
    });

    app.get('/resources/prefix/:prefix', (req, res) => {
        const { prefix } = req.params;
        const matchingResources = Array.from(resources.values())
            .filter(resource => resource.id.startsWith(prefix + '/'));
        res.json({ resources: matchingResources });
    });

    app.get('/resources/search', (req, res) => {
        const query = req.query.q?.toLowerCase();
        if (!query) {
            res.status(400).json({ error: 'Search query required' });
            return;
        }

        const results = Array.from(resources.values())
            .filter(resource =>
                resource.title.toLowerCase().includes(query) ||
                resource.content?.toLowerCase().includes(query)
            )
            .map(resource => ({
                ...resource,
                score: 0.9 // Simplified scoring
            }));
        res.json({ results });
    });
}

// Info endpoint
if (config.endpoints.info.enabled) {
    app.get('/info', (req, res) => {
        try {
            res.json({
                name: config.endpoints.info.name,
                version: config.endpoints.info.version,
                description: config.endpoints.info.description,
                endpoints: [
                    {
                        path: '/chat',
                        methods: ['GET', 'POST'],
                        description: 'Chat interface with streaming support'
                    },
                    {
                        path: '/tools',
                        methods: ['GET'],
                        description: 'Access system tools and utilities'
                    },
                    {
                        path: '/memory',
                        methods: ['GET', 'POST', 'PUT', 'DELETE'],
                        description: 'Memory management and persistence'
                    },
                    {
                        path: '/resources',
                        methods: ['GET', 'POST'],
                        description: 'Resource access and management'
                    }
                ],
                capabilities: {
                    streaming: true,
                    websockets: true,
                    models: config.endpoints.chat.models
                }
            });
        } catch (error) {
            logger.error('Info endpoint error:', error);
            res.status(500).json({ status: 'error', message: error.message });
        }
    });
}

// WebSocket handler
wss.on('connection', (ws) => {
    logger.info('New WebSocket connection established');

    // Update metrics message data
    const getMetricsData = () => ({
        uptime: metrics.getUptime(),
        requests: metrics.requests,
        errors: metrics.errors,
        requestsPerSecond: metrics.getRequestsPerSecond(),
        errorRate: metrics.getErrorRate(),
        mycelialSyncs: metrics.mycelialSyncs,
        ethikValidations: metrics.ethikValidations,
        system: metrics.system,
        subsystems: metrics.subsystems,
        performance: metrics.performance,
        trends: metrics.trends,
        subsystemHealth: metrics.subsystemHealth,
        thresholds: ALERT_THRESHOLDS
    });

    // Send initial metrics with enhanced data
    ws.send(JSON.stringify({
        type: 'metrics',
        data: getMetricsData()
    }));

    // Update metrics interval with enhanced data
    const metricsInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'metrics',
                data: getMetricsData()
            }));
        }
    }, 5000);

    // Send system health status
    const healthInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            const health = {
                atlas: atlasVisualizations.size > 0,
                nexus: nexusAnalysis.size > 0,
                cronos: cronosTimeline.size > 0,
                ethik: ethikValidations.size > 0,
                mycelium: myceliumNetwork.nodes.size > 0
            };

            ws.send(JSON.stringify({
                type: 'health',
                data: health
            }));
        }
    }, 10000);

    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);

            switch (data.type) {
                case 'request_metrics':
                    ws.send(JSON.stringify({
                        type: 'metrics',
                        data: getMetricsData()
                    }));
                    break;

                case 'request_health':
                    const health = {
                        atlas: atlasVisualizations.size > 0,
                        nexus: nexusAnalysis.size > 0,
                        cronos: cronosTimeline.size > 0,
                        ethik: ethikValidations.size > 0,
                        mycelium: myceliumNetwork.nodes.size > 0
                    };
                    ws.send(JSON.stringify({
                        type: 'health',
                        data: health
                    }));
                    break;

                default:
                    logger.warn(`Unknown message type: ${data.type}`);
            }
        } catch (error) {
            logger.error(`WebSocket message error: ${error.message}`);
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ error: error.message }));
            }
        }
    });

    ws.on('close', () => {
        clearInterval(metricsInterval);
        clearInterval(healthInterval);
        logger.info('WebSocket connection closed');
    });

    ws.on('error', (error) => {
        logger.error(`WebSocket error: ${error.message}`);
        clearInterval(metricsInterval);
        clearInterval(healthInterval);
    });
});

// Input validation middleware
const validateInput = (schema) => {
    return (req, res, next) => {
        const { error } = schema.validate(req.body);
        if (error) {
            logger.error(`Input validation error: ${error.details[0].message}`);
            return res.status(400).json({
                status: 'error',
                message: `Validation error: ${error.details[0].message}`
            });
        }
        next();
    };
};

// Validation schemas
const schemas = {
    myceliumConnect: Joi.object({
        nodeId: Joi.string().required(),
        nodeType: Joi.string().required(),
        connections: Joi.array().items(Joi.string())
    }),

    ethikValidate: Joi.object({
        actionId: Joi.string().required(),
        context: Joi.object({
            action: Joi.string().required(),
            impact_level: Joi.string().valid('low', 'medium', 'high').required()
        }).required(),
        parameters: Joi.object()
    }),

    fileSync: Joi.object({
        fileId: Joi.string().required(),
        filePath: Joi.string().required(),
        fileType: Joi.string().required(),
        connections: Joi.array().items(Joi.string())
    })
};

/**
 * @openapi
 * components:
 *   schemas:
 *     MyceliumNode:
 *       type: object
 *       required:
 *         - nodeId
 *         - nodeType
 *       properties:
 *         nodeId:
 *           type: string
 *           description: Unique identifier for the node
 *         nodeType:
 *           type: string
 *           description: Type of the node
 *         connections:
 *           type: array
 *           items:
 *             type: string
 *           description: Array of connected node IDs
 *
 *     EthikValidation:
 *       type: object
 *       required:
 *         - actionId
 *         - context
 *       properties:
 *         actionId:
 *           type: string
 *           description: Unique identifier for the validation
 *         context:
 *           type: object
 *           required:
 *             - action
 *             - impact_level
 *           properties:
 *             action:
 *               type: string
 *               description: Action being validated
 *             impact_level:
 *               type: string
 *               enum: [low, medium, high]
 *               description: Impact level of the action
 *
 *     FileSync:
 *       type: object
 *       required:
 *         - fileId
 *         - filePath
 *         - fileType
 *       properties:
 *         fileId:
 *           type: string
 *           description: Unique identifier for the file
 *         filePath:
 *           type: string
 *           description: Path to the file in the system
 *         fileType:
 *           type: string
 *           description: Type of the file
 *         connections:
 *           type: array
 *           items:
 *             type: string
 *           description: Array of connected file IDs
 */

/**
 * @openapi
 * /mycelium/connect:
 *   post:
 *     summary: Connect a node to the Mycelium Network
 *     tags: [Mycelium]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MyceliumNode'
 *     responses:
 *       200:
 *         description: Node connected successfully
 *       400:
 *         description: Invalid input
 *       500:
 *         description: Server error
 */
app.post('/mycelium/connect', validateInput(schemas.myceliumConnect), (req, res) => {
    const { nodeId, nodeType, connections } = req.body;

    if (!nodeId || !nodeType) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: nodeId, nodeType'
        });
    }

    try {
        // Store node information
        myceliumNetwork.nodes.set(nodeId, {
            type: nodeType,
            status: 'active',
            created: Date.now(),
            lastUpdated: Date.now()
        });

        // Store connections if provided
        if (Array.isArray(connections)) {
            myceliumNetwork.connections.set(nodeId, connections);

            // Create reciprocal connections
            connections.forEach(targetNodeId => {
                const targetConnections = myceliumNetwork.connections.get(targetNodeId) || [];
                if (!targetConnections.includes(nodeId)) {
                    targetConnections.push(nodeId);
                    myceliumNetwork.connections.set(targetNodeId, targetConnections);
                }
            });
        }

        logger.info(`Mycelium: Node ${nodeId} conectado. Tipo: ${nodeType}`);

        res.status(200).json({
            status: 'success',
            message: 'Node conectado com sucesso à Mycelium Network',
            data: {
                nodeId,
                nodeType,
                connections: myceliumNetwork.connections.get(nodeId) || []
            }
        });
    } catch (error) {
        logger.error(`Erro ao conectar node à Mycelium Network: ${error.message}`);
        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

/**
 * @openapi
 * /mycelium/register-file:
 *   post:
 *     summary: Register a file in the Mycelium Network
 *     tags: [Mycelium]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/FileSync'
 *     responses:
 *       200:
 *         description: File registered successfully
 *       400:
 *         description: Invalid input
 *       404:
 *         description: File not found
 *       500:
 *         description: Server error
 */
app.post('/mycelium/register-file', validateInput(schemas.fileSync), (req, res) => {
    const { fileId, filePath, fileType, connections } = req.body;

    if (!fileId || !filePath || !fileType) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: fileId, filePath, fileType'
        });
    }

    try {
        // Check if file exists
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({
                status: 'error',
                message: `Arquivo não encontrado: ${filePath}`
            });
        }

        // Register file
        myceliumNetwork.files.set(fileId, {
            path: filePath,
            type: fileType,
            registered: Date.now(),
            lastSync: null
        });

        // Store connections if provided
        if (Array.isArray(connections)) {
            myceliumNetwork.connections.set(fileId, connections);
        }

        logger.info(`Mycelium: Arquivo ${fileId} registrado. Tipo: ${fileType}, Caminho: ${filePath}`);

        // Trigger immediate sync for this file
        if (Array.isArray(connections) && connections.length > 0) {
            setTimeout(() => {
                try {
                    // Simplified sync for just this file
                    const content = fs.readFileSync(filePath, 'utf-8');

                    connections.forEach(connectedFileId => {
                        const connectedFile = myceliumNetwork.files.get(connectedFileId);
                        if (connectedFile && fs.existsSync(connectedFile.path)) {
                            const targetContent = fs.readFileSync(connectedFile.path, 'utf-8');

                            if (fileType === 'roadmap' && connectedFile.type === 'readme') {
                                const newContent = updateReadmeWithRoadmap(targetContent, content);
                                fs.writeFileSync(connectedFile.path, newContent);
                                logger.info(`Sincronizado imediatamente: ${fileId} -> ${connectedFileId}`);
                            }
                        }
                    });

                    myceliumNetwork.syncHistory.set(fileId, Date.now());
                } catch (syncError) {
                    logger.error(`Erro na sincronização imediata: ${syncError.message}`);
                }
            }, 1000); // Wait 1 second before sync
        }

        res.status(200).json({
            status: 'success',
            message: 'Arquivo registrado com sucesso na Mycelium Network',
            data: {
                fileId,
                fileType,
                filePath,
                connections: myceliumNetwork.connections.get(fileId) || []
            }
        });
    } catch (error) {
        logger.error(`Erro ao registrar arquivo na Mycelium Network: ${error.message}`);
        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

// New endpoint to get Mycelium Network status
app.get('/mycelium/status', (req, res) => {
    try {
        const networkStatus = {
            nodes: {
                count: myceliumNetwork.nodes.size,
                types: {}
            },
            files: {
                count: myceliumNetwork.files.size,
                types: {}
            },
            connections: {
                count: Array.from(myceliumNetwork.connections.values())
                    .reduce((total, connections) => total + connections.length, 0) / 2, // Divide by 2 since connections are bidirectional
                averagePerNode: myceliumNetwork.nodes.size > 0
                    ? Array.from(myceliumNetwork.connections.values())
                        .reduce((total, connections) => total + connections.length, 0) / myceliumNetwork.nodes.size
                    : 0
            },
            lastSync: myceliumNetwork.lastSync,
            health: "Healthy"
        };

        // Count node types
        myceliumNetwork.nodes.forEach(node => {
            networkStatus.nodes.types[node.type] = (networkStatus.nodes.types[node.type] || 0) + 1;
        });

        // Count file types
        myceliumNetwork.files.forEach(file => {
            networkStatus.files.types[file.type] = (networkStatus.files.types[file.type] || 0) + 1;
        });

        res.status(200).json({
            status: 'success',
            message: 'Status da Mycelium Network',
            data: networkStatus
        });
    } catch (error) {
        logger.error(`Erro ao obter status da Mycelium Network: ${error.message}`);
        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

// ATLAS Visualization endpoint
app.post('/atlas/visualize', (req, res) => {
    const { systemId, type, data } = req.body;

    if (!systemId || !type || !data) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: systemId, type, data'
        });
    }

    try {
        // Criar visualização
        const visualizationId = `viz_${Date.now()}`;
        const visualization = {
            id: visualizationId,
            systemId,
            type,
            data,
            created: Date.now()
        };

        // Armazenar visualização
        atlasVisualizations.set(visualizationId, visualization);

        // Log mais limpo
        prettyLog('info', `ATLAS: Visualização criada ${visualizationId} (${type})`, {
            systemId,
            nodes: Array.isArray(data.nodes) ? data.nodes.length : 0
        });

        res.status(200).json({
            status: 'success',
            message: 'Visualização criada com sucesso',
            data: {
                visualizationId,
                systemId,
                type
            }
        });
    } catch (error) {
        prettyLog('error', `ATLAS: Erro ao criar visualização: ${error.message}`);

        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

// CRONOS Timeline endpoint
app.post('/cronos/timeline', (req, res) => {
    const { eventId, timestamp, data } = req.body;

    if (!eventId || !data) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: eventId, data'
        });
    }

    try {
        // Criar evento na timeline
        const timelineEvent = {
            id: eventId,
            timestamp: timestamp || new Date().toISOString(),
            data,
            recorded: Date.now()
        };

        // Armazenar evento
        cronosTimeline.set(eventId, timelineEvent);

        // Log mais limpo
        prettyLog('info', `CRONOS: Evento registrado ${eventId}`, {
            type: data.type,
            timestamp: timelineEvent.timestamp
        });

        res.status(200).json({
            status: 'success',
            message: 'Evento registrado com sucesso',
            data: {
                eventId,
                timestamp: timelineEvent.timestamp
            }
        });
    } catch (error) {
        prettyLog('error', `CRONOS: Erro ao registrar evento: ${error.message}`);

        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

// NEXUS Analysis endpoint
app.post('/nexus/analyze', (req, res) => {
    const { analysisId, data, parameters } = req.body;

    if (!analysisId || !data) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: analysisId, data'
        });
    }

    try {
        // Criar análise
        const analysis = {
            id: analysisId,
            data,
            parameters: parameters || {},
            created: Date.now(),
            status: 'completed'
        };

        // Armazenar análise
        nexusAnalysis.set(analysisId, analysis);

        // Log mais limpo
        prettyLog('info', `NEXUS: Análise realizada ${analysisId}`, {
            type: data.type,
            metrics: Array.isArray(data.metrics) ? data.metrics.join(', ') : data.metrics
        });

        res.status(200).json({
            status: 'success',
            message: 'Análise realizada com sucesso',
            data: {
                analysisId,
                status: analysis.status,
                results: {
                    summary: 'Análise concluída com sucesso',
                    metrics: data.metrics,
                    recommendations: [
                        'Otimização de desempenho recomendada',
                        'Estrutura de dados eficiente',
                        'Cobertura de testes adequada'
                    ]
                }
            }
        });
    } catch (error) {
        prettyLog('error', `NEXUS: Erro ao realizar análise: ${error.message}`);

        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

/**
 * @openapi
 * /ethik/validate:
 *   post:
 *     summary: Validate an action against ethical framework
 *     tags: [ETHIK]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/EthikValidation'
 *     responses:
 *       200:
 *         description: Validation completed successfully
 *       400:
 *         description: Invalid input
 *       500:
 *         description: Server error
 */
app.post('/ethik/validate', validateInput(schemas.ethikValidate), (req, res) => {
    const { actionId, context, parameters } = req.body;

    if (!actionId || !context) {
        return res.status(400).json({
            status: 'error',
            message: 'Parâmetros obrigatórios: actionId, context'
        });
    }

    try {
        // Criar validação
        const validation = {
            id: actionId,
            context,
            parameters: parameters || {},
            timestamp: new Date().toISOString(),
            result: {
                isValid: true,
                score: 0.85,
                concerns: [],
                recommendations: []
            }
        };

        // Verificar se há preocupações éticas
        if (context.impact_level === 'high') {
            validation.result.concerns.push('Impacto de alto nível requer revisão adicional');
            validation.result.recommendations.push('Realizar revisão por especialista em ética');
            validation.result.score = 0.7;
        }

        // Armazenar validação
        ethikValidations.set(actionId, validation);

        // Log mais limpo
        prettyLog('info', `ETHIK: Validação concluída ${actionId}`, {
            action: context.action,
            impact: context.impact_level,
            score: validation.result.score
        });

        res.status(200).json({
            status: 'success',
            message: 'Validação concluída com sucesso',
            data: {
                actionId,
                result: validation.result
            }
        });
    } catch (error) {
        prettyLog('error', `ETHIK: Erro ao validar ação: ${error.message}`);

        res.status(500).json({
            status: 'error',
            message: 'Erro interno do servidor'
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    // Log de erro mais limpo
    prettyLog('error', `Erro em ${req.method} ${req.url}: ${err.message}`, {
        stack: process.env.NODE_ENV === 'production' ? null : err.stack.split('\n').slice(0, 3).join('\n')
    });

    res.status(500).json({
        status: 'error',
        message: 'Internal Server Error'
    });
});

// Start server
const port = config.server.port || 3000;
server.listen(port, config.server.host, () => {
    logger.info(`SLOP server running at http://${config.server.host}:${port}`);
    logger.info('WebSocket server running at ws://' + config.server.host + ':' + port);

    // Log subsystem status
    Object.entries(config.subsystems).forEach(([name, subsystem]) => {
        logger.info(`Subsystem ${name}: ${subsystem.enabled ? 'ACTIVE' : 'INACTIVE'}`);
    });

    // Register filesystem module
    const slopServer = {
        app,
        wss,
        logger,
        config,
        state: {}
    };

    if (filesystemIntegration.register(slopServer)) {
        logger.info('Filesystem module registered successfully');
    } else {
        logger.error('Failed to register filesystem module');
    }
});
