---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: test-filesystem-simple.js
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
 * EVA & GUARANI - Simple Filesystem Module Test
 * Version: 1.0.0
 * Date: 2025-03-29
 */

const express = require('express');
const app = express();
const port = 3002;

// Configure Express
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

console.log('Setting up simple filesystem test...');

// Create routes for direct testing
app.get('/', (req, res) => {
    res.send(`
    <html>
      <head>
        <title>EVA & GUARANI Filesystem Simple Test</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
          h1 { color: #333; }
          pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow: auto; }
        </style>
      </head>
      <body>
        <h1>EVA & GUARANI Filesystem Simple Test</h1>
        <p>This is a simple test page for the filesystem module.</p>
        <p>Available endpoints:</p>
        <ul>
          <li><a href="/test-read">/test-read</a> - Tests reading a file</li>
          <li><a href="/test-list">/test-list</a> - Tests listing directory contents</li>
        </ul>
      </body>
    </html>
  `);
});

// Test read operation
app.get('/test-read', async (req, res) => {
    try {
        const fs = require('fs').promises;
        const path = require('path');

        // Test reading a file
        const testFilePath = path.join(__dirname, 'slop', 'modules', 'filesystem', 'test-file.txt');

        console.log(`Reading file: ${testFilePath}`);
        const data = await fs.readFile(testFilePath, 'utf8');

        res.send(`
      <html>
        <head>
          <title>File Read Test</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow: auto; }
          </style>
        </head>
        <body>
          <h1>File Read Test</h1>
          <p>Successfully read file: ${testFilePath}</p>
          <h2>File Content:</h2>
          <pre>${data}</pre>
          <p><a href="/">Back to home</a></p>
        </body>
      </html>
    `);
    } catch (error) {
        console.error('Error reading file:', error);
        res.status(500).send(`
      <html>
        <head>
          <title>File Read Test - Error</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            .error { color: red; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow: auto; }
          </style>
        </head>
        <body>
          <h1>File Read Test - Error</h1>
          <p class="error">Error reading file: ${error.message}</p>
          <pre>${error.stack}</pre>
          <p><a href="/">Back to home</a></p>
        </body>
      </html>
    `);
    }
});

// Test list operation
app.get('/test-list', async (req, res) => {
    try {
        const fs = require('fs').promises;
        const path = require('path');

        // Test listing directory contents
        const dirPath = path.join(__dirname, 'slop', 'modules', 'filesystem');

        console.log(`Listing directory: ${dirPath}`);
        const files = await fs.readdir(dirPath);

        // Get details for each file
        const fileDetails = await Promise.all(
            files.map(async (file) => {
                const filePath = path.join(dirPath, file);
                const stats = await fs.stat(filePath);
                return {
                    name: file,
                    path: filePath,
                    size: stats.size,
                    isDirectory: stats.isDirectory(),
                    created: stats.birthtime,
                    modified: stats.mtime
                };
            })
        );

        res.send(`
      <html>
        <head>
          <title>Directory List Test</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
          </style>
        </head>
        <body>
          <h1>Directory List Test</h1>
          <p>Successfully listed directory: ${dirPath}</p>
          <h2>Files:</h2>
          <table>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Size</th>
              <th>Modified</th>
            </tr>
            ${fileDetails.map(file => `
              <tr>
                <td>${file.name}</td>
                <td>${file.isDirectory ? 'Directory' : 'File'}</td>
                <td>${file.size} bytes</td>
                <td>${file.modified.toISOString()}</td>
              </tr>
            `).join('')}
          </table>
          <p><a href="/">Back to home</a></p>
        </body>
      </html>
    `);
    } catch (error) {
        console.error('Error listing directory:', error);
        res.status(500).send(`
      <html>
        <head>
          <title>Directory List Test - Error</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            .error { color: red; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow: auto; }
          </style>
        </head>
        <body>
          <h1>Directory List Test - Error</h1>
          <p class="error">Error listing directory: ${error.message}</p>
          <pre>${error.stack}</pre>
          <p><a href="/">Back to home</a></p>
        </body>
      </html>
    `);
    }
});

// Start server
app.listen(port, () => {
    console.log(`Simple filesystem test server running at http://localhost:${port}`);
    console.log('Press Ctrl+C to stop');
});
