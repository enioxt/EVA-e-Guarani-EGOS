# ETHIK Implementation Guide

## Directory Structure

The ETHIK subsystem is structured across two directories:

1. **QUANTUM_PROMPTS/ETHIK** - Conceptual framework, roadmap, and configuration
2. **src/core/ethik** - Actual implementation with interfaces and code

## Implementation Status

- Core interfaces are implemented in `src/core/ethik/validator.py`
- These interfaces define the contract for the ETHIK validation framework
- Concrete implementations will be added in `src/modules/ethik/`

## Development Workflow

When working on the ETHIK subsystem:

1. **Reference** the roadmap and PRD in `QUANTUM_PROMPTS/ETHIK`
2. **Implement** code in the `src/core/ethik` and `src/modules/ethik` directories
3. **Update** the implementation status in both roadmaps when complete

## Alignment Maintenance

To avoid duplication and ensure consistency:

- Keep conceptual materials in QUANTUM_PROMPTS/ETHIK
- Keep implementation code in src/core/ethik and src/modules/ethik
- Update both directories' documentation when making changes

This structure ensures that the implementation follows the conceptual framework while keeping the code in a standard project structure.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
