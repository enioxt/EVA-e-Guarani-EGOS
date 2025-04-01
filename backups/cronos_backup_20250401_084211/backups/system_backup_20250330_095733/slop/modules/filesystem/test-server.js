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
  type: test
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
 * EVA & GUARANI - SLOP Filesystem Module Test Server
 * Version: 1.0.0
 * Date: 2025-03-29
 * 
 * This script creates a minimal SLOP-compatible server to test the filesystem module.
 * It simulates the SLOP server structure and registers the filesystem module.
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const integration = require('./integration');

// Create a mock SLOP server
const mockSlopServer = {
  app: express(),
  routes: [],
  config: {
    logLevel: 'debug',
    port: 3000
  },
  logger: {
    info: (...args) => console.log('\x1b[36m[INFO]\x1b[0m', ...args),
    warn: (...args) => console.log('\x1b[33m[WARN]\x1b[0m', ...args),
    error: (...args) => console.log('\x1b[31m[ERROR]\x1b[0m', ...args),
    debug: (...args) => console.log('\x1b[90m[DEBUG]\x1b[0m', ...args)
  },

  // Add route to the server
  addRoute(route) {
    this.routes.push(route);
    this.logger.debug(`Route added: ${route.method} ${route.path}`);

    // Register the route with Express
    this.app[route.method.toLowerCase()](route.path, route.handler);
  }
};

// Initialize Express middleware
mockSlopServer.app.use(express.json());
mockSlopServer.app.use(express.urlencoded({ extended: true }));

// Log all requests
mockSlopServer.app.use((req, res, next) => {
  mockSlopServer.logger.info(`${req.method} ${req.path}`);
  next();
});

// Register the filesystem module
integration.register(mockSlopServer, {
  allowedDirectories: [
    process.cwd(), // Current directory
    path.resolve(process.cwd(), '../../..') // Project root
  ],
  maxFileSize: 10 * 1024 * 1024, // 10MB
  maxResults: 1000,
  logLevel: 'debug'
});

// Add a simple root route
mockSlopServer.app.get('/', (req, res) => {
  res.json({
    name: 'SLOP Test Server',
    modules: ['filesystem'],
    routes: mockSlopServer.routes.map(r => `${r.method} ${r.path}`)
  });
});

// Create a simple HTML page to test the API
mockSlopServer.app.get('/test-ui', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>SLOP Filesystem Test</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .container { display: flex; }
        .panel { flex: 1; margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { margin: 5px; padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #45a049; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
        #result { background: #f5f5f5; padding: 10px; border-radius: 3px; white-space: pre-wrap; max-height: 400px; overflow: auto; }
      </style>
    </head>
    <body>
      <h1>SLOP Filesystem Test UI</h1>
      <div class="container">
        <div class="panel">
          <h2>Operations</h2>
          <div>
            <input id="path" placeholder="Enter file/directory path" value="${process.cwd()}" />
          </div>
          <div>
            <button onclick="readFile()">Read File</button>
            <button onclick="writeFile()">Write File</button>
            <button onclick="listDirectory(false)">List Directory</button>
            <button onclick="listDirectory(true)">List Recursively</button>
            <button onclick="searchFiles()">Search Files</button>
            <button onclick="deleteFile()">Delete File</button>
          </div>
          <div id="additionalInputs">
            <!-- Dynamic inputs will appear here based on operation -->
          </div>
        </div>
        <div class="panel">
          <h2>Result</h2>
          <div id="result"></div>
        </div>
      </div>
      
      <script>
        // Helper function to display results
        function displayResult(data) {
          document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        }
        
        // Helper function to display error
        function displayError(error) {
          document.getElementById('result').innerHTML = '<span style="color: red">Error: ' + error.message + '</span>';
          console.error(error);
        }
        
        // Helper function to make API requests
        async function apiRequest(endpoint, data) {
          try {
            const response = await fetch(endpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
              throw new Error(result.error || 'Unknown error');
            }
            
            return result;
          } catch (error) {
            displayError(error);
            throw error;
          }
        }
        
        // Prepare additional inputs based on operation
        function prepareAdditionalInputs(inputsHtml) {
          document.getElementById('additionalInputs').innerHTML = inputsHtml;
        }
        
        // Read file operation
        async function readFile() {
          prepareAdditionalInputs(`
    < div >
              <label>Encoding:</label>
              <input id="encoding" value="utf8" />
            </div >
    `);
          
          const path = document.getElementById('path').value;
          const encoding = document.getElementById('encoding')?.value || 'utf8';
          
          try {
            const result = await apiRequest('/fs/read', {
              path,
              encoding
            });
            
            displayResult(result);
          } catch (error) {
            // Error is already displayed by apiRequest
          }
        }
        
        // Write file operation
        async function writeFile() {
          prepareAdditionalInputs(`
    < div >
              <label>Content:</label>
              <textarea id="content" rows="5">Test content created by the SLOP Filesystem Test UI</textarea>
            </div >
            <div>
              <label>Encoding:</label>
              <input id="encoding" value="utf8" />
            </div>
            <div>
              <label>
                <input type="checkbox" id="createDirectories" />
                Create parent directories if needed
              </label>
            </div>
            <div>
              <button id="runWrite">Write File</button>
            </div>
          `);
          
          // Wait for user to enter content
          document.getElementById('runWrite').onclick = async function() {
            const path = document.getElementById('path').value;
            const content = document.getElementById('content').value;
            const encoding = document.getElementById('encoding').value;
            const createDirectories = document.getElementById('createDirectories').checked;
            
            try {
              const result = await apiRequest('/fs/write', {
                path,
                content,
                encoding,
                createDirectories
              });
              
              displayResult(result);
            } catch (error) {
              // Error is already displayed by apiRequest
            }
          };
        }
        
        // List directory operation
        async function listDirectory(recursive) {
          prepareAdditionalInputs(`
    < div >
              <label>Pattern (regex):</label>
              <input id="pattern" placeholder="Optional pattern to filter files" />
            </div >
    `);
          
          const path = document.getElementById('path').value;
          const pattern = document.getElementById('pattern')?.value || null;
          
          try {
            const result = await apiRequest('/fs/list', {
              path,
              recursive,
              pattern
            });
            
            displayResult(result);
          } catch (error) {
            // Error is already displayed by apiRequest
          }
        }
        
        // Search files operation
        async function searchFiles() {
          prepareAdditionalInputs(`
    < div >
              <label>Name Pattern (regex):</label>
              <input id="namePattern" placeholder="Pattern to match file names" />
            </div >
            <div>
              <label>Content Pattern (regex):</label>
              <input id="contentPattern" placeholder="Pattern to match file contents" />
            </div>
            <div>
              <label>
                <input type="checkbox" id="recursive" checked />
                Search recursively
              </label>
            </div>
            <div>
              <label>Max Results:</label>
              <input id="maxResults" type="number" value="100" />
            </div>
            <div>
              <button id="runSearch">Search</button>
            </div>
          `);
          
          document.getElementById('runSearch').onclick = async function() {
            const path = document.getElementById('path').value;
            const namePattern = document.getElementById('namePattern').value || null;
            const contentPattern = document.getElementById('contentPattern').value || null;
            const recursive = document.getElementById('recursive').checked;
            const maxResults = parseInt(document.getElementById('maxResults').value, 10);
            
            if (!namePattern && !contentPattern) {
              return displayError(new Error('At least one pattern (name or content) is required'));
            }
            
            try {
              const result = await apiRequest('/fs/search', {
                path,
                namePattern,
                contentPattern,
                recursive,
                maxResults
              });
              
              displayResult(result);
            } catch (error) {
              // Error is already displayed by apiRequest
            }
          };
        }
        
        // Delete file operation
        async function deleteFile() {
          prepareAdditionalInputs(`
    < div >
    <label>
      <input type="checkbox" id="recursive" />
      Delete recursively (required for directories)
    </label>
            </div >
            <div>
              <label>
                <input type="checkbox" id="confirm" />
                I confirm I want to delete this file/directory
              </label>
            </div>
            <div>
              <button id="runDelete" disabled>Confirm Delete</button>
            </div>
          `);
          
          // Enable the delete button only when confirmed
          document.getElementById('confirm').onchange = function() {
            document.getElementById('runDelete').disabled = !this.checked;
          };
          
          document.getElementById('runDelete').onclick = async function() {
            if (!document.getElementById('confirm').checked) {
              return;
            }
            
            const path = document.getElementById('path').value;
            const recursive = document.getElementById('recursive').checked;
            
            try {
              const result = await apiRequest('/fs/delete', {
                path,
                recursive
              });
              
              displayResult(result);
            } catch (error) {
              // Error is already displayed by apiRequest
            }
          };
        }
      </script>
    </body>
    </html>
  `);
});

// Start the server
const port = process.env.PORT || mockSlopServer.config.port;
mockSlopServer.app.listen(port, () => {
  mockSlopServer.logger.info(`SLOP Test Server listening on port ${port}`);
  mockSlopServer.logger.info(`Test UI available at http://localhost:${port}/test-ui`);
  mockSlopServer.logger.info(`API endpoints:`);

  // Log all registered routes
  mockSlopServer.routes.forEach(route => {
    mockSlopServer.logger.info(`  ${route.method} ${route.path} - ${route.description}`);
  });
});

// Handle errors
process.on('uncaughtException', (error) => {
  mockSlopServer.logger.error('Uncaught exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  mockSlopServer.logger.error('Unhandled rejection at:', promise, 'reason:', reason);
}); 