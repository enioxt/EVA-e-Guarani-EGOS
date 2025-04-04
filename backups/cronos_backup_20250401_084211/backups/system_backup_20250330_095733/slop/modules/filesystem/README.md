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
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
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
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
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
```

# EVA & GUARANI Filesystem Module

Version: 1.0.0
Date: 2025-03-29

## Overview

The Filesystem Module provides file and directory operations for the EVA & GUARANI system through the SLOP (Simple Language Open Protocol) server. It allows secure and controlled access to the filesystem with configurable permissions and limits.

## Features

- **Secure Access Control**: Only access directories explicitly allowed in configuration
- **Core Operations**: Read, write, list, search, and delete files and directories
- **Recursive Operations**: Support for recursive directory listing and searching
- **Pattern Matching**: Filter files by name pattern during listing and searching
- **Content Search**: Search for text within files
- **Size Limitations**: Configurable maximum file size for read/write operations
- **Comprehensive Error Handling**: Clear error messages with appropriate HTTP status codes
- **Detailed Logging**: Optional debug and error logging
- **WebSocket Support**: Real-time updates via WebSocket connection
- **Client Adapter**: Browser and Node.js compatible client adapter

## Installation

The module is designed to be integrated with the EVA & GUARANI SLOP server:

```javascript
// In your SLOP server configuration
const filesystemIntegration = require('./modules/filesystem/integration');

// Register with the SLOP server
filesystemIntegration.register(slopServer, {
    allowedDirectories: [
        'C:/Eva Guarani EGOS',
        'C:/Eva Guarani EGOS/QUANTUM_PROMPTS'
    ],
    maxFileSize: 20 * 1024 * 1024, // 20MB
    maxResults: 1000,
    logLevel: 'info'
});
```

## API Endpoints

### Read File

```
GET /filesystem/read
```

**Parameters**:

- `path` (required): Path to the file to read

**Response**:

```json
{
  "status": "success",
  "message": "File read successfully",
  "data": {
    "path": "C:/path/to/file.txt",
    "content": "File content here",
    "fileId": "md5hash",
    "stats": {
      "size": 42,
      "created": "2025-03-29T12:00:00.000Z",
      "modified": "2025-03-29T12:00:00.000Z",
      "accessed": "2025-03-29T12:00:00.000Z"
    }
  }
}
```

### Write File

```
POST /filesystem/write
```

**Body**:

```json
{
  "path": "C:/path/to/file.txt",
  "content": "New content",
  "createDirectories": true
}
```

**Response**:

```json
{
  "status": "success",
  "message": "File written successfully",
  "data": {
    "path": "C:/path/to/file.txt",
    "fileId": "md5hash",
    "stats": {
      "size": 42,
      "created": "2025-03-29T12:00:00.000Z",
      "modified": "2025-03-29T12:00:00.000Z"
    }
  }
}
```

### List Directory

```
GET /filesystem/list
```

**Parameters**:

- `path` (required): Path to the directory to list
- `recursive` (optional): 'true' to list recursively
- `pattern` (optional): Regex pattern to filter files

**Response**:

```json
{
  "status": "success",
  "message": "Directory listed successfully",
  "data": {
    "path": "C:/path/to/directory",
    "files": [
      {
        "name": "file.txt",
        "path": "C:/path/to/directory/file.txt",
        "type": "file",
        "fileId": "md5hash",
        "size": 42,
        "created": "2025-03-29T12:00:00.000Z",
        "modified": "2025-03-29T12:00:00.000Z"
      }
    ],
    "directories": [
      {
        "name": "subdirectory",
        "path": "C:/path/to/directory/subdirectory",
        "type": "directory"
      }
    ],
    "totalCount": 2
  }
}
```

### Search Files

```
GET /filesystem/search
```

**Parameters**:

- `path` (required): Path to the directory to search
- `query` (required): Text to search for in filenames and content
- `recursive` (optional): 'true' to search recursively
- `limit` (optional): Maximum number of results to return

**Response**:

```json
{
  "status": "success",
  "message": "Search completed successfully",
  "data": {
    "query": "searchterm",
    "path": "C:/path/to/directory",
    "nameMatches": [
      {
        "name": "searchterm.txt",
        "path": "C:/path/to/directory/searchterm.txt",
        "type": "file",
        "fileId": "md5hash",
        "size": 42,
        "created": "2025-03-29T12:00:00.000Z",
        "modified": "2025-03-29T12:00:00.000Z"
      }
    ],
    "contentMatches": [
      {
        "name": "document.txt",
        "path": "C:/path/to/directory/document.txt",
        "type": "file",
        "fileId": "md5hash",
        "size": 120,
        "created": "2025-03-29T12:00:00.000Z",
        "modified": "2025-03-29T12:00:00.000Z",
        "matches": [
          {
            "line": 5,
            "context": "This is the searchterm in context"
          }
        ]
      }
    ],
    "totalMatches": 2,
    "limitReached": false
  }
}
```

### Delete File/Directory

```
DELETE /filesystem/delete
```

**Parameters**:

- `path` (required): Path to the file or directory to delete
- `recursive` (optional): 'true' to delete directories recursively

**Response**:

```json
{
  "status": "success",
  "message": "File deleted successfully",
  "data": {
    "path": "C:/path/to/file.txt",
    "type": "file"
  }
}
```

### Module Info

```
GET /filesystem/info
```

**Response**:

```json
{
  "status": "success",
  "data": {
    "name": "filesystem",
    "version": "1.0.0",
    "stats": {
      "reads": 10,
      "writes": 5,
      "deletes": 2,
      "lists": 8,
      "searches": 3,
      "errors": 0,
      "lastOperation": {
        "type": "read",
        "path": "C:/path/to/file.txt",
        "timestamp": "2025-03-29T12:00:00.000Z"
      }
    },
    "routes": [
      {
        "method": "GET",
        "path": "/filesystem/read",
        "description": "Read file contents"
      },
      // ...other routes
    ],
    "config": {
      "allowedDirectories": ["C:/Eva Guarani EGOS"],
      "maxFileSize": 10485760,
      "maxResults": 1000
    }
  }
}
```

## Client Adapter

The module includes a client adapter that can be used in both browser and Node.js environments:

```javascript
// Node.js
const { createAdapter } = require('./adapter');

// Browser
const { createAdapter } = window.EVAFilesystem;

// Create adapter
const filesystem = createAdapter({
    baseUrl: 'http://localhost:3000'
});

// Use the adapter
async function example() {
    // Read a file
    const file = await filesystem.readFile('C:/path/to/file.txt');

    // Write a file
    await filesystem.writeFile('C:/path/to/new-file.txt', 'Hello, world!', true);

    // List a directory
    const listing = await filesystem.listDirectory('C:/path/to/directory', true);

    // Search for files
    const results = await filesystem.searchFiles('C:/path/to/directory', 'searchterm', true, 100);

    // Delete a file
    await filesystem.deleteFile('C:/path/to/file.txt');
}
```

## CLI Testing Tool

The module includes a command-line testing tool for developers:

```bash
# Show help
node cli-test.js help

# Start a test server
node cli-test.js server

# Read a file
node cli-test.js read C:/path/to/file.txt

# Write to a file
node cli-test.js write C:/path/to/file.txt "File content"

# List a directory
node cli-test.js list C:/path/to/directory --recursive

# Search for files
node cli-test.js search C:/path/to/directory searchterm --limit 50

# Delete a file
node cli-test.js delete C:/path/to/file.txt
```

## Security Considerations

- Only directories listed in `allowedDirectories` configuration are accessible
- File size limitations prevent excessive memory usage
- Result limits prevent excessive processing time
- Path normalization prevents directory traversal attacks
- Error handling avoids leaking sensitive information

## Integration with SLOP Server

This module is designed to be integrated with the EVA & GUARANI SLOP server. See the `filesystem-integration.js` file in the SLOP server directory for integration details.

## License

MIT

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
