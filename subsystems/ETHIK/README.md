# ETHIK Subsystem

**Version:** 8.0.0
**Status:** Active (Core Logic Recovered & Tested)

## Overview

ETHIK is the ethical framework and validation subsystem for the EVA GUARANI - EGOS project. Its purpose is to ensure that all system operations, data handling, and AI interactions adhere to predefined ethical principles and standards.

## Core Components

*   **`EthikValidator` (`core/validator.py`):** Responsible for validating actions, data, or configurations against a set of ethical rules and principles.
    *   Loads rules from a configuration file (`config/ethik_rules.json`).
    *   Provides `validate()` method to check input data against rules.
    *   Integrates with Mycelium to listen for validation requests (`request.ethik.validate`) and publish results (`response.validation.<request_id>`).
*   **`EthikSanitizer` (`core/sanitizer.py`):** Responsible for sanitizing content (e.g., text, code) to remove or flag ethically problematic elements based on defined rules.
    *   Loads sanitization rules (including regex patterns and replacements) from `config/sanitization_rules.json`.
    *   Provides `sanitize_content()` method (and async version).
    *   Uses a cache (`content_cache`) and priority queue for performance.
    *   Maintains a history of sanitization actions.
    *   Integrates with Mycelium to listen for sanitization requests (`request.ethik.sanitize`) and publish results (`response.sanitization.<request_id>`).
*   **`EthikService` (`service.py`):** Wraps the Validator and Sanitizer, manages their lifecycle, handles configuration loading, and initializes the Mycelium interface for them.
    *   Provides `start()` and `stop()` methods to manage the service and its components.
    *   Coordinates the interaction between core logic components and the Mycelium network.
*   **`config/`:** Contains configuration files:
    *   `ethik_config.json`: Main configuration for the EthikService, including Mycelium topics, component settings, etc.
    *   `ethik_rules.json`: Defines the rules used by the `EthikValidator`.
    *   `sanitization_rules.json`: Defines the rules used by the `EthikSanitizer`.
*   **`tests/`:** Contains unit tests for the validator, sanitizer, and service.

## Key Features

*   **Rule-Based Validation:** Allows defining flexible ethical rules in JSON format.
*   **Content Sanitization:** Provides automated detection and replacement of content based on configurable rules.
*   **Mycelium Integration:** Enables decentralized validation and sanitization requests/responses across the EGOS system.
*   **Caching & History:** Optimizes performance for repeated sanitization requests and maintains an auditable history.
*   **Configurable:** Rules and service behavior can be adjusted via configuration files.

## Integration

*   **Mycelium:** ETHIK heavily relies on Mycelium for communication. Other subsystems can request validation or sanitization by publishing messages to the appropriate topics (defined in `ethik_config.json`).
*   **KOIOS:** Uses `KoiosLogger`. ETHIK rules and configurations should adhere to KOIOS standards.
*   **Other Subsystems:** Any subsystem performing actions or handling data that requires ethical review should integrate with ETHIK by sending requests via Mycelium.

## Current Status & Next Steps

*   Core logic for Validator and Sanitizer recovered from backups.
*   Mycelium integration implemented and tested via `EthikService`.
*   Unit tests provide substantial coverage.
*   Next steps involve:
    *   Refining documentation (this README, docstrings).
    *   Potentially implementing gamification/RPG mechanics as outlined in the main roadmap (Phase 4+).
    *   Expanding rule sets (`ethik_rules.json`, `sanitization_rules.json`) as needed.

## Usage (Conceptual via Mycelium)

1.  **Requesting Validation:**
    *   Publish a message to the `request.ethik.validate` topic.
    *   Payload should contain the data to be validated, e.g., `{"action": "delete_user", "user_level": "admin"}`.
    *   Include a unique request ID.
    *   Listen on `response.validation.<request_id>` for the result (`{"is_valid": true/false, "details": [...]}`).

2.  **Requesting Sanitization:**
    *   Publish a message to the `request.ethik.sanitize` topic.
    *   Payload should contain `{"content": "Text to sanitize...", "context": {...}}`.
    *   Include a unique request ID.
    *   Listen on `response.sanitization.<request_id>` for the `SanitizationResult` (or error).

*(Refer to `EthikService` and core components for specific payload structures)*

## Contributing

Please follow KOIOS standards. Contributions to the ethical rule sets require careful consideration and review.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 