# EVA & GUARANI EGOS - Quantum Prompts

Version: 8.1
Last Updated: 2025-04-01
Status: Active

## Overview

This directory contains the quantum prompts and configurations for the EVA & GUARANI EGOS system. These prompts define the behavior, capabilities, and interactions of our subsystems, which are implemented in the `C:/Eva Guarani EGOS/subsystems` directory.

## Directory Structure

```
QUANTUM_PROMPTS/
├── MASTER/             # Master prompt configurations
├── ATLAS/              # Cartography prompt definitions
├── NEXUS/              # Analysis prompt definitions
├── CRONOS/             # Preservation prompt definitions
├── ETHIK/              # Ethics prompt definitions
├── HARMONY/            # Integration prompt definitions
├── KOIOS/              # Process prompt definitions
└── BIOS-Q/             # Initialization prompt definitions
```

## Important Note

The actual subsystem implementations are located in `C:/Eva Guarani EGOS/subsystems/`. This directory only contains the quantum prompts that guide their behavior. Do not place implementation code here.

## Relationship with Subsystems

Each directory here corresponds to a subsystem implementation in the main subsystems directory:

| Prompt Directory | Implementation Directory |
|-----------------|-------------------------|
| QUANTUM_PROMPTS/MASTER | subsystems/MASTER |
| QUANTUM_PROMPTS/ATLAS | subsystems/ATLAS |
| QUANTUM_PROMPTS/NEXUS | subsystems/NEXUS |
| QUANTUM_PROMPTS/CRONOS | subsystems/CRONOS |
| QUANTUM_PROMPTS/ETHIK | subsystems/ETHIK |
| QUANTUM_PROMPTS/HARMONY | subsystems/HARMONY |
| QUANTUM_PROMPTS/KOIOS | subsystems/KOIOS |
| QUANTUM_PROMPTS/BIOS-Q | subsystems/BIOS-Q |

## Usage

1. Prompt files should be in markdown format
2. Each prompt should have clear version information
3. Prompts should reference correct subsystem paths
4. Keep implementation details in subsystems directory
5. Use relative paths when referencing other prompts

## Initialization

The BIOS-Q system will automatically load these prompts during initialization. Ensure all paths and references are correct before initialization.

## Maintenance

1. Regular verification of prompt integrity
2. Version control of prompt changes
3. Synchronization with subsystem implementations
4. Documentation of prompt updates
5. Backup of critical prompts

## Integration

These prompts integrate with:
- BIOS-Q initialization
- Subsystem implementations
- MCP framework
- ETHIK point system
- Metadata management

## Best Practices

1. Keep prompts focused on behavior definition
2. Maintain clear separation from implementation
3. Use consistent formatting
4. Include version information
5. Document changes

## Support

For assistance or to report issues:
1. Check documentation
2. Review logs
3. Submit issue
4. Contact maintainers

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
