# Mycelium Network Subsystem

**Version:** 0.3 # Updated version
**Last Updated:** 2025-04-02

## Core Vision

The Mycelium Network is the core communication and integration fabric of the EGOS system. Inspired by natural mycelial networks, it enables seamless, adaptive, and resilient information flow between all subsystems, fostering emergent collaboration and collective intelligence.

## Key Objectives

-   Provide a unified communication bus for all subsystems.
-   Support various communication patterns (request/response, pub/sub, events).
-   Enable dynamic discovery and routing between subsystems.
-   Facilitate state synchronization and resource sharing where appropriate.
-   Ensure resilient and fault-tolerant communication.

## Existing Implementation (within SLOP Server)

An initial implementation of Mycelium Network concepts exists within the SLOP server (`src/services/slop/src/server/slop_server.js.backup`). This includes REST APIs and basic sync logic, serving as a reference.

## Status

-   **Core Implementation (Python/Asyncio):** Completed and unit tested (`network.py`, `node.py`, `interface.py`). Provides basic registration, connection management, and message routing (Req/Res, Pub/Sub).
-   **Design:** Consolidated design documented in `docs/protocol_design.md`.
-   **Next Steps:** Focus on integrating this core implementation with BIOS-Q and piloting subsystem connections (see main `ROADMAP.md`). Phase 2 features (advanced health, sync, routing) planned after initial integration.

Refer to the detailed protocol design in `docs/protocol_design.md` and the main project `ROADMAP.md` for current priorities.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 