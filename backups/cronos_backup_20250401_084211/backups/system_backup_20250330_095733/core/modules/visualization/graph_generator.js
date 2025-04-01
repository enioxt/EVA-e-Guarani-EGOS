---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: modules
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

javascript
/**
 * EVA & GUARANI - Graph Generation Utilities (ATLAS)
 * ==========================================================
 * 
 * This module provides utilities for generating visualization data
 * for different types of graphs used by the ATLAS subsystem.
 * 
 * @context EVA_GUARANI_ATLAS_UTILS
 * @version 1.0.0
 * @author EVA & GUARANI Team
 */

/**
 * Generates data for dependency graph in a format compatible with Cytoscape. * @param {Array<Object>} nodes - List of nodes
 * @param {Array<Object>} edges - List of edges
 * @param {Object} options - Customization options
 * @returns {Object} Data formatted for Cytoscape.js
 */
function generateCytoscapeData(nodes, edges, options = {}) {
    // Default options
    const defaultOptions = {
        includeMetrics: true,
        includeEthicalWarnings: true,
        theme: 'light',
        colorBy: 'type', // 'type', 'metrics', 'warnings'
        nodeSize: 'fixed' // 'fixed', 'degree', 'centrality'
    };
    
    // Merge options
    const graphOptions = { ...defaultOptions, ...options };
    
    // Format nodes for Cytoscape
    const cytoscapeNodes = nodes.map(node => {
        // Base node data
        const nodeData = {
            id: node.id,
            label: node.label || node.id,
            fullPath: node.fullPath || '',
            type: node.type || 'unknown'
        };
        
        // Add metrics if requested
        if (graphOptions.includeMetrics && node.metrics) {
            nodeData.metrics = node.metrics;
        }
        
        // Add ethical markings if requested
        if (graphOptions.includeEthicalWarnings) {
            if (node.ethical_warning) nodeData.ethical_warning = true;
            if (node.ethical_note) nodeData.ethical_note = true;
            if (node.inCycle) nodeData.inCycle = true;
            if (node.isolated) nodeData.isolated = true;
            if (node.highlight) nodeData.highlight = true;
        }
        
        // Set node size based on option
        if (graphOptions.nodeSize === 'degree' && node.metrics) {
            const inDegree = node.metrics.inboundDeps || 0;
            const outDegree = node.metrics.outboundDeps || 0;
            nodeData.size = Math.max(10, Math.min(30, 10 + (inDegree + outDegree) * 1.5));
        } else if (graphOptions.nodeSize === 'centrality' && node.metrics && node.metrics.centrality) {
            nodeData.size = Math.max(10, Math.min(30, 10 + node.metrics.centrality * 3));
        }
        
        // Add custom color
        if (node.color) {
            nodeData.color = node.color;
        }
        
        return {
            data: nodeData
        };
    });
    
    // Format edges for Cytoscape
    const cytoscapeEdges = edges.map(edge => {
        // Base edge data
        const edgeData = {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            type: edge.type || 'default'
        };
        
        // Add weight if available
        if (edge.weight) {
            edgeData.weight = edge.weight;
        }
        
        return {
            data: edgeData
        };
    });
    
    return {
        nodes: cytoscapeNodes,
        edges: cytoscapeEdges
    };
}

/**
 * Generates data for heatmap in a format compatible with heatmap.js
 * @param {Array<Object>} nodes - List of nodes with complexity metrics
 * @param {Object} options - Customization options
 * @returns {Object} Data formatted for heatmap
 */
function generateHeatmapData(nodes, options = {}) {
    // Default options
    const defaultOptions = {
        metric: 'complexity', // Metric to use for heat
        maxValue: 10, // Maximum value for normalization
        colorScale: [
            { value: 0, color: '#edf8fb' },
            { value: 0.2, color: '#b2e2e2' },
            { value: 0.4, color: '#66c2a4' },
            { value: 0.6, color: '#2ca25f' },
            { value: 0.8, color: '#006d2c' },
            { value: 1, color: '#00441b' }
        ]
    };
    
    // Merge options
    const heatmapOptions = { ...defaultOptions, ...options };
    
    // Extract values of the selected metric
    const metricValues = nodes
        .filter(node => node.metrics && node.metrics[heatmapOptions.metric] !== undefined)
        .map(node => {
            return {
                id: node.id,
                label: node.label || node.id,
                path: node.path || '',
                value: node.metrics[heatmapOptions.metric],
                normalized: Math.min(1, node.metrics[heatmapOptions.metric] / heatmapOptions.maxValue)
            };
        });
    
    // Associate colors based on the scale and normalized values
    metricValues.forEach(item => {
        const scale = heatmapOptions.colorScale;
        
        // Find position on the color scale
        for (let i = 0; i < scale.length - 1; i++) {
            const lower = scale[i];
            const upper = scale[i + 1];
            
            if (item.normalized >= lower.value && item.normalized <= upper.value) {
                // Calculate interpolated color
                const ratio = (item.normalized - lower.value) / (upper.value - lower.value);
                item.color = interpolateColor(lower.color, upper.color, ratio);
                break;
            }
        }
        
        // If no interval found, use the last color
        if (!item.color) {
            item.color = scale[scale.length - 1].color;
        }
    });
    
    return {
        items: metricValues,
        options: heatmapOptions
    };
}

/**
 * Color interpolation between two hexadecimal values
 * @private
 * @param {string} color1 - Start color (hex)
 * @param {string} color2 - End color (hex)
 * @param {number} ratio - Ratio between 0 and 1
 * @returns {string} Interpolated color (hex)
 */
function interpolateColor(color1, color2, ratio) {
    // Convert colors to RGB
    const rgb1 = hexToRgb(color1);
    const rgb2 = hexToRgb(color2);
    
    // Linear interpolation
    const r = Math.round(rgb1.r + (rgb2.r - rgb1.r) * ratio);
    const g = Math.round(rgb1.g + (rgb2.g - rgb1.g) * ratio);
    const b = Math.round(rgb1.b + (rgb2.b - rgb1.b) * ratio);
    
    // Convert back to hex
    return rgbToHex(r, g, b);
}

/**
 * Converts a hex color to RGB
 * @private
 * @param {string} hex - Color in hexadecimal format
 * @returns {Object} Object with r, g, b components
 */
function hexToRgb(hex) {
    // Remove # if present
    hex = hex.replace(/^#/, '');
    
    // Handle shorthand formats (e.g., #fff)
    if (hex.length === 3) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    
    // Convert to decimal components
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    
    return { r, g, b };
}

/**
 * Converts RGB components to hexadecimal
 * @private
 * @param {number} r - Red component (0-255)
 * @param {number} g - Green component (0-255)
 * @param {number} b - Blue component (0-255)
 * @returns {string} Color in hexadecimal format
 */
function rgbToHex(r, g, b) {
    return '#' + 
        (r < 16 ? '0' : '') + r.toString(16) +
        (g < 16 ? '0' : '') + g.toString(16) +
        (b < 16 ? '0' : '') + b.toString(16);
}

/**
 * Generates layout for organizing nodes in a hierarchical format
 * Useful for visualizing module and package structures
 * @param {Array<Object>} nodes - List of nodes
 * @param {Array<Object>} edges - List of edges
 * @param {Object} options - Customization options
 * @returns {Object} Positions for hierarchical layout
 */
function generateHierarchicalLayout(nodes, edges, options = {}) {
    // Default options
    const defaultOptions = {
        direction: 'TB', // 'TB' (top-bottom), 'LR' (left-right)
        levelSeparation: 100,
        nodeSeparation: 50,
        edgeMinimization: true
    };
    
    // Merge options
    const layoutOptions = { ...defaultOptions, ...options };
    
    // Data structure to represent directed graph
    const graph = {
        nodes: new Map(),
        children: new Map(),
        parents: new Map()
    };
    
    // Initialize structures
    nodes.forEach(node => {
        graph.nodes.set(node.id, node);
        graph.children.set(node.id, []);
        graph.parents.set(node.id, []);
    });
    
    // Fill parent-child relationships
    edges.forEach(edge => {
        const source = edge.source;
        const target = edge.target;
        
        if (graph.children.has(source) && graph.parents.has(target)) {
            graph.children.get(source).push(target);
            graph.parents.get(target).push(source);
        }
    });
    
    // Simplified topological sorting algorithm
    const visited = new Set();
    const levels = new Map();
    
    // Find nodes without parents (roots)
    const roots = Array.from(graph.nodes.keys())
        .filter(nodeId => graph.parents.get(nodeId).length === 0);
    
    // Initialize roots at level 0
    roots.forEach(root => {
        levels.set(root, 0);
    });
    
    // Function to assign levels recursively
    const assignLevels = (nodeId, level) => {
        if (visited.has(nodeId)) {
            // If already visited, update to the maximum level
            levels.set(nodeId, Math.max(levels.get(nodeId) || 0, level));
            return;
        }
        
        visited.add(nodeId);
        levels.set(nodeId, level);
        
        // Process children
        graph.children.get(nodeId).forEach(childId => {
            assignLevels(childId, level + 1);
        });
    };
    
    // Assign levels starting from the roots
    roots.forEach(root => {
        assignLevels(root, 0);
    });
    
    // Handle cycles: unvisited nodes
    Array.from(graph.nodes.keys())
        .filter(nodeId => !visited.has(nodeId))
        .forEach(nodeId => {
            // Assign level based on parents, or default level
            const parentLevels = graph.parents.get(nodeId)
                .filter(parentId => levels.has(parentId))
                .map(parentId => levels.get(parentId));
            
            const level = parentLevels.length > 0 
                ? Math.max(...parentLevels) + 1
                : 0;
                
            assignLevels(nodeId, level);
        });
    
    // Calculate X and Y positions based on levels
    const positions = {};
    
    // Group nodes by level
    const nodesByLevel = new Map();
    for (const [nodeId, level] of levels.entries()) {
        if (!nodesByLevel.has(level)) {
            nodesByLevel.set(level, []);
        }
        nodesByLevel.get(level).push(nodeId);
    }
    
    // Calculate positions
    for (const [level, nodeIds] of nodesByLevel.entries()) {
        const count = nodeIds.length;
        
        nodeIds.forEach((nodeId, index) => {
            const x = layoutOptions.direction === 'TB'
                ? layoutOptions.nodeSeparation * (index - (count - 1) / 2)
                : layoutOptions.levelSeparation * level;
                
            const y = layoutOptions.direction === 'TB'
                ? layoutOptions.levelSeparation * level
                : layoutOptions.nodeSeparation * (index - (count - 1) / 2);
                
            positions[nodeId] = { x, y };
        });
    }
    
    return positions;
}

module.exports = {
    generateCytoscapeData,
    generateHeatmapData,
    generateHierarchicalLayout
};