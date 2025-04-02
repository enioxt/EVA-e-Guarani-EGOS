# CRONOS Subsystem Documentation

## Overview

CRONOS is the backup and state preservation subsystem of the EGOS project. It provides robust functionality for creating, managing, and restoring backups of the entire project or specific modules.

## Core Components

### BackupManager

The `BackupManager` class is responsible for handling backup operations:

- Creating backups of project state
- Listing available backups
- Restoring from backups using different strategies
- Managing backup retention and cleanup

### CronosService

The `CronosService` provides a Mycelium-based interface for backup operations:

- Handling backup requests
- Managing restore operations
- Providing backup status information
- Coordinating with other subsystems

## Features

### Backup Creation
- Automatic backup scheduling
- Manual backup triggers
- Configurable backup retention
- Backup metadata preservation

### Backup Listing
- List available backups
- Sort by date/time
- Filter by type or content
- Metadata inspection

### Backup Restoration
- Multiple restore strategies:
  - `replace`: Complete replacement of target directory
  - `merge`: Selective merge of backup contents
- Restore validation
- Error handling and rollback
- Progress tracking

## Usage

### Creating a Backup

```python
from cronos.service import CronosService

service = CronosService()
await service.create_backup(
    target_modules=["ETHIK", "ATLAS"],
    metadata={"description": "Pre-deployment backup"}
)
```

### Listing Backups

```python
backups = await service.list_backups()
for backup in backups:
    print(f"Backup: {backup}")
```

### Restoring from Backup

```python
await service.restore_backup(
    backup_identifier="backup_20250401_001.zip",
    restore_target_path="/path/to/restore",
    strategy="merge"
)
```

## Configuration

The CRONOS subsystem can be configured through environment variables or configuration files:

```yaml
CRONOS_BACKUP_DIR: /path/to/backups
CRONOS_RETENTION_DAYS: 30
CRONOS_MAX_BACKUPS: 100
```

## Error Handling

CRONOS implements comprehensive error handling:

- Validation of backup files
- Integrity checks during restore
- Rollback capabilities
- Detailed error reporting

## Integration with Other Subsystems

CRONOS integrates with:

- ETHIK for validation of backup/restore operations
- ATLAS for backup metadata mapping
- NEXUS for module dependency tracking
- KoiosLogger for operation logging

## Testing

Run the test suite:

```bash
cd subsystems/CRONOS
pytest tests/
```

## Best Practices

1. Regular Backups
   - Schedule automatic backups
   - Maintain multiple backup points
   - Document significant changes

2. Restore Testing
   - Regularly test restore functionality
   - Validate restored state
   - Document restore procedures

3. Backup Management
   - Monitor backup storage usage
   - Clean old backups regularly
   - Verify backup integrity

## Troubleshooting

Common issues and solutions:

1. Backup Creation Fails
   - Check disk space
   - Verify write permissions
   - Check file locks

2. Restore Fails
   - Verify backup file exists
   - Check target directory permissions
   - Validate backup file integrity

3. Performance Issues
   - Monitor backup size
   - Check compression settings
   - Review backup frequency

## Contributing

When contributing to CRONOS:

1. Follow coding standards
2. Add tests for new features
3. Update documentation
4. Test backup/restore functionality
5. Review error handling

## Version History

- v1.0.0 - Initial release
- v1.1.0 - Added merge strategy
- v1.2.0 - Enhanced error handling
- v1.3.0 - Added backup metadata
- v2.0.0 - Integrated with Mycelium

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 