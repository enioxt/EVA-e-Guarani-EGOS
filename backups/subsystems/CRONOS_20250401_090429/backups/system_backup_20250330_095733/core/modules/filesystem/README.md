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

# EVA & GUARANI - SLOP Filesystem Module

Version: 1.0.0
Date: 2025-03-29

## Overview

The Filesystem module extends the SLOP (Simple Language Open Protocol) server with secure filesystem operations. It provides a RESTful API for reading, writing, listing, searching, and deleting files, with built-in security features to prevent unauthorized access outside allowed directories.

## Security Features

- **Path Validation**: All file operations are restricted to allowed directories.
- **Size Limits**: Maximum file size enforced for both reading and writing.
- **Results Limits**: Maximum number of results enforced for directory listings and search.
- **Detailed Logging**: All file operations are logged for audit purposes.

## API Endpoints

### Read File

Reads a file from the filesystem.

- **Endpoint**: `/api/fs/read`
- **Method**: POST
- **Request Body**:

  ```json
  {
    "path": "C:/Eva Guarani EGOS/test.txt",
    "encoding": "utf8"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "path": "C:/Eva Guarani EGOS/test.txt",
    "content": "File content here",
    "encoding": "utf8",
    "stats": {
      "size": 123,
      "modified": "2025-03-29T12:34:56.789Z",
      "created": "2025-03-29T12:34:56.789Z"
    },
    "id": "a1b2c3d4e5f6g7h8i9j0"
  }
  ```

### Write File

Writes content to a file. Can create directories if they don't exist.

- **Endpoint**: `/api/fs/write`
- **Method**: POST
- **Request Body**:

  ```json
  {
    "path": "C:/Eva Guarani EGOS/test.txt",
    "content": "New file content",
    "encoding": "utf8",
    "createDirectories": true
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "path": "C:/Eva Guarani EGOS/test.txt",
    "size": 16,
    "id": "a1b2c3d4e5f6g7h8i9j0"
  }
  ```

### List Directory

Lists files and directories in a specified directory.

- **Endpoint**: `/api/fs/list`
- **Method**: POST
- **Request Body**:

  ```json
  {
    "path": "C:/Eva Guarani EGOS",
    "recursive": false,
    "pattern": ".*\\.txt"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "path": "C:/Eva Guarani EGOS",
    "files": [
      {
        "name": "test.txt",
        "path": "C:/Eva Guarani EGOS/test.txt",
        "isDirectory": false,
        "id": "a1b2c3d4e5f6g7h8i9j0"
      },
      {
        "name": "docs",
        "path": "C:/Eva Guarani EGOS/docs",
        "isDirectory": true,
        "id": "b2c3d4e5f6g7h8i9j0k1"
      }
    ],
    "count": 2,
    "limited": false
  }
  ```

### Search Files

Searches for files by name or content pattern.

- **Endpoint**: `/api/fs/search`
- **Method**: POST
- **Request Body**:

  ```json
  {
    "path": "C:/Eva Guarani EGOS",
    "namePattern": ".*\\.txt",
    "contentPattern": "example",
    "recursive": true,
    "maxResults": 100
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "path": "C:/Eva Guarani EGOS",
    "matches": [
      {
        "name": "test.txt",
        "path": "C:/Eva Guarani EGOS/test.txt",
        "isDirectory": false,
        "id": "a1b2c3d4e5f6g7h8i9j0",
        "matchesContent": true
      }
    ],
    "count": 1,
    "limited": false
  }
  ```

### Delete File

Deletes a file or directory.

- **Endpoint**: `/api/fs/delete`
- **Method**: POST
- **Request Body**:

  ```json
  {
    "path": "C:/Eva Guarani EGOS/test.txt",
    "recursive": true
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "path": "C:/Eva Guarani EGOS/test.txt",
    "isDirectory": false
  }
  ```

## Configuration

The module can be configured with the following options:

```javascript
const config = {
  // Directories that can be accessed by the module (all paths must be in these directories)
  allowedDirectories: ['C:/Eva Guarani EGOS'],

  // Maximum file size in bytes (default: 10MB)
  maxFileSize: 10 * 1024 * 1024,

  // Maximum number of results for listing and search operations
  maxResults: 1000,

  // Log level (debug, info, warn, error)
  logLevel: 'info'
};
```

## Integration with SLOP Server

The module automatically registers with the SLOP server through the integration file:

```javascript
// In your SLOP server startup file
const express = require('express');
const app = express();

// Require the filesystem module integration
const filesystemModule = require('./modules/filesystem/integration');

// Register the module with the SLOP server
const config = {
  filesystem: {
    allowedDirectories: ['C:/Eva Guarani EGOS'],
    maxFileSize: 10 * 1024 * 1024,
    maxResults: 1000
  }
};

const dependencies = {
  logger: yourLogger // Provide your logger instance
};

filesystemModule.register(app, config, dependencies);
```

## Security Best Practices

1. Limit allowed directories to only what is necessary
2. Use a dedicated user account with limited permissions
3. Regularly audit file access logs
4. Consider implementing additional authentication for sensitive operations
5. Monitor disk usage to prevent denial of service attacks

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Operation successful
- `400 Bad Request`: Missing parameters or invalid request
- `403 Forbidden`: Access denied to requested path
- `404 Not Found`: File or directory not found
- `413 Payload Too Large`: File or content too large
- `500 Internal Server Error`: Server-side error

Error responses include details about the error:

```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
