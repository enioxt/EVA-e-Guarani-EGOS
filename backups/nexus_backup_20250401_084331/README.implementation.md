# NEXUS Implementation Guide

## Directory Structure

The NEXUS subsystem is structured across two directories:

1. **QUANTUM_PROMPTS/NEXUS** - Conceptual framework, roadmap, and configuration
2. **src/core/nexus** - Actual implementation with interfaces and code

## Implementation Status

- Core interfaces are implemented in `src/core/nexus/analyzer.py`
- These interfaces define the contract for the NEXUS analysis framework
- Concrete implementations will be added in `src/modules/nexus/`

## Development Workflow

When working on the NEXUS subsystem:

1. **Reference** the roadmap and PRD in `QUANTUM_PROMPTS/NEXUS`
2. **Implement** code in the `src/core/nexus` and `src/modules/nexus` directories
3. **Update** the implementation status in both roadmaps when complete

## Alignment Maintenance

To avoid duplication and ensure consistency:

- Keep conceptual materials in QUANTUM_PROMPTS/NEXUS
- Keep implementation code in src/core/nexus and src/modules/nexus
- Update both directories' documentation when making changes

This structure ensures that the implementation follows the conceptual framework while keeping the code in a standard project structure.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
