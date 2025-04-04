# EVA & GUARANI EGOS - Metadata System v1.0

Version: 1.0
Last Updated: 2025-04-01
Status: Active
Priority: HIGH

## Overview

The EVA & GUARANI EGOS Metadata System provides a centralized approach to managing file metadata across the entire project. This system ensures clean code while maintaining rich metadata information for all files.

## Core Components

### 1. Metadata Database

- **Location**: `.metadata/metadata_db.json`
- **Format**: JSON
- **Purpose**: Central storage for all file metadata
- **Features**:
  - Standardized schema
  - Version tracking
  - File hash verification
  - Change history
  - Cross-reference support

### 2. Management Tools

#### Metadata Manager
- **Script**: `tools/scripts/metadata_manager.py`
- **Purpose**: Core metadata management tool
- **Features**:
  - Extract metadata from files
  - Clean file content
  - Update metadata database
  - Track file changes
  - Process entire workspace

#### Metadata Access
- **Script**: `tools/scripts/get_metadata.py`
- **Purpose**: Retrieve file metadata
- **Features**:
  - Multiple path formats
  - Formatted output
  - JSON export
  - Cross-platform compatibility

#### Metadata Updates
- **Script**: `tools/scripts/update_metadata.py`
- **Purpose**: Update file metadata
- **Features**:
  - Field-specific updates
  - Automatic hash calculation
  - Change tracking
  - Validation checks

## Metadata Schema

### Core Fields

```json
{
  "type": "string",          // File type (e.g., "python", "markdown")
  "category": "string",      // File category
  "version": "string",       // File version
  "author": "string",        // File author
  "description": "string",   // File description
  "last_updated": "string",  // ISO timestamp
  "status": "string"         // File status
}
```

### System Fields

```json
{
  "file_hash": "string",     // MD5 hash of file content
  "last_processed": "string", // ISO timestamp
  "file_path": "string",     // Relative path in workspace
  "backup_required": "bool",  // Backup flag
  "security_level": "float"  // Security rating (0-1)
}
```

### Optional Fields

```json
{
  "dependencies": "array",    // File dependencies
  "api_endpoints": "array",   // Associated API endpoints
  "test_coverage": "float",   // Test coverage ratio
  "documentation_quality": "float", // Doc quality score
  "related_files": "array",   // Related file paths
  "changelog": "array",       // Change history
  "translation_status": "string", // Translation state
  "ethical_validation": "bool" // Ethics check status
}
```

## Usage Guide

### 1. Viewing Metadata

```bash
# Basic usage
python tools/scripts/get_metadata.py path/to/file.py

# JSON output
python tools/scripts/get_metadata.py path/to/file.py --json
```

### 2. Updating Metadata

```bash
# Update single field
python tools/scripts/update_metadata.py path/to/file.py --update "version=2.0"

# Update multiple fields
python tools/scripts/update_metadata.py path/to/file.py --update "version=2.0,status=active"
```

### 3. Processing Files

```bash
# Process all files
python tools/scripts/metadata_manager.py

# View processing logs
cat logs/metadata_manager.log
```

## Integration Points

### 1. BIOS-Q Integration

- Metadata system initialization during BIOS-Q startup
- Automatic metadata verification
- State preservation across sessions

### 2. CRONOS Integration

- Backup management
- Version control
- Change tracking
- State preservation

### 3. ETHIK Integration

- Ethical validation tracking
- Compliance verification
- Security level assessment

### 4. ATLAS Integration

- System mapping support
- Relationship tracking
- Dependency management

## Best Practices

1. **Metadata Updates**
   - Keep metadata current
   - Update on significant changes
   - Validate before commits
   - Track dependencies

2. **File Management**
   - Use provided tools
   - Maintain clean files
   - Regular verification
   - Backup important data

3. **System Integration**
   - Follow initialization sequence
   - Verify integrity regularly
   - Monitor system logs
   - Update documentation

## Error Handling

### Common Issues

1. **File Not Found**
   - Verify file path
   - Check workspace root
   - Validate relative paths

2. **Invalid Metadata**
   - Check schema compliance
   - Validate field types
   - Fix formatting issues

3. **Database Issues**
   - Check file permissions
   - Verify JSON integrity
   - Backup before changes

### Resolution Steps

1. **Metadata Corruption**
   ```bash
   # Backup database
   cp .metadata/metadata_db.json .metadata/metadata_db.backup.json

   # Reprocess files
   python tools/scripts/metadata_manager.py
   ```

2. **Sync Issues**
   ```bash
   # Verify file hash
   python tools/scripts/get_metadata.py file.py --json | grep file_hash

   # Update metadata
   python tools/scripts/update_metadata.py file.py --update "key=value"
   ```

## Monitoring and Maintenance

### Regular Tasks

1. **Daily**
   - Check processing logs
   - Verify recent changes
   - Update changed files

2. **Weekly**
   - Full system verification
   - Backup metadata database
   - Clean obsolete entries

3. **Monthly**
   - Schema validation
   - Performance optimization
   - Documentation updates

### Metrics

1. **Coverage**
   - Files with metadata
   - Fields per file
   - Required fields

2. **Quality**
   - Metadata accuracy
   - Update frequency
   - Validation success

3. **Performance**
   - Processing time
   - Database size
   - Query response time

## Future Enhancements

1. **Phase 1 (Current)**
   - Basic metadata management ✓
   - File processing system ✓
   - Integration points ✓

2. **Phase 2 (Planned)**
   - Advanced validation
   - Automated updates
   - Performance optimization

3. **Phase 3 (Future)**
   - AI-assisted metadata
   - Real-time sync
   - Advanced analytics

## Updates Log

- [2025-04-01] Initial implementation
- [2025-04-01] Added BIOS-Q integration
- [2025-04-01] Implemented core tools
- [2025-04-01] Created documentation

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
