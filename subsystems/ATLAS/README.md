---
metadata:
  # ... (keep existing metadata)
  last_updated: '2025-04-02' # Update date
  status: active_development # Update status
  test_coverage: 0.85 # Update coverage estimate
  # ... (keep existing metadata)
---

# 🗺️ ATLAS Subsystem - System Cartography & Visualization

**Version:** 1.0.0
**Status:** Active (Core Logic Stable, Tests Passing)
**Subsystem Lead:** EVA & GUARANI
**Dependencies:** Mycelium (for message bus), KOIOS (for logging - currently mocked), potentially NEXUS (for deeper analysis)
**Test Coverage:** ~85% (Core Cartographer Logic)
**Windows Compatibility:** Yes

## 📜 Overview

ATLAS is the systemic cartography and visualization subsystem for the EVA GUARANI - EGOS project. Its purpose is to map the relationships and structures within the EGOS system (or other complex data) and provide methods to visualize these maps.

## ✨ Core Features

*   **System Mapping:** Dynamically generates maps of system components and their relationships.
*   **Relationship Tracking:** Records and manages various types of relationships (e.g., `depends_on`, `imports`, `calls`).
*   **Metadata Management:** Stores and retrieves metadata associated with system components.
*   **Mycelium Integration:** Listens for updates and requests via the Mycelium message bus.
*   **Caching:** Caches generated maps for improved performance.
*   **(Future) Visualization:** Generate various visual representations (e.g., Mermaid diagrams, DOT graphs).
*   **(Future) Analysis:** Perform basic structural analysis (e.g., identifying orphans, circular dependencies).

## 🏗️ Architecture

*   **`AtlasService` (`service.py`):** Main entry point, manages lifecycle and Mycelium interactions.
*   **`AtlasCartographer` (`core/cartographer.py`):** Core logic for mapping, relationship management, metadata storage, and caching.
*   **Configuration (`config/atlas_config.json`):** Defines Mycelium topics, mapping parameters (e.g., max depth), cache settings.
*   **Mycelium Topics:**
    *   `atlas.map.request`: Request a system map.
    *   `atlas.map.result`: Published map results or errors.
    *   `atlas.metadata.update`: Request to update component metadata.
    *   `atlas.metadata.status`: Status of metadata update request.
    *   `atlas.relationship.update`: Request to update a relationship.
    *   `atlas.relationship.status`: Status of relationship update request.
    *   `atlas.alert`: System alerts related to mapping (e.g., depth limits).

## 💻 Usage

ATLAS primarily interacts with other subsystems via the Mycelium network. Subsystems can publish update messages or request maps.

**Example Mycelium Messages:**

*   **Request Map:**
    ```json
    {
        "topic": "atlas.map.request",
        "data": {
            "target": "subsystems.NEXUS",
            "depth": 3,
            "include_metadata": true
        }
    }
    ```
*   **Update Metadata:**
    ```json
    {
        "topic": "atlas.metadata.update",
        "data": {
            "component": "subsystems.CRONOS.core.backup",
            "metadata": {"version": "1.2", "last_tested": "2025-04-01"}
        }
    }
    ```
*   **Update Relationship:**
    ```json
    {
        "topic": "atlas.relationship.update",
        "data": {
            "source": "subsystems.ATLAS.service",
            "target": "subsystems.KOIOS.logger",
            "type": "uses",
            "metadata": {"context": "error_logging"}
        }
    }
    ```

## 🚀 Recovery & Next Steps

1.  **[DONE] Locate Backups:** Identified relevant code/docs in historical backups.
2.  **[DONE] Analyze Components:** Reviewed backup structure (`atlas_core.py`, service logic, tests).
3.  **[DONE] Migrate & Integrate Core Logic:** Integrated `cartographer.py` logic into the `subsystems/ATLAS/core` directory. Created `AtlasService`.
4.  **[DONE] Add Configuration & Basic Tests:** Implemented configuration loading and comprehensive tests for `AtlasCartographer`.
5.  **[DONE] Resolve Test Dependencies:** Created mock Mycelium, used standard logging, fixed import paths, and ensured all `test_cartographer.py` tests pass.
6.  **Refine Documentation:** Improve this README and add inline code documentation.
7.  **Refine Core Logic (If Needed):** Review `cartographer.py` for any potential optimizations or edge cases missed by tests.
8.  **Implement Visualization:** Add methods to generate different map formats (Mermaid, DOT).
9.  **Integrate with KOIOS Logger:** Replace standard logging with the actual KOIOS logger once available.
10. **Full Mycelium Integration:** Test end-to-end interaction via the Mycelium network.

## ✅ Testing

Comprehensive unit tests for the `AtlasCartographer` core logic are located in `subsystems/ATLAS/tests/test_cartographer.py`.

A PowerShell script is provided in the project root to run these tests:

```powershell
# Run tests
.\test_atlas.ps1

# Run tests with verbose output
.\test_atlas.ps1 -Verbose

# Run tests with coverage report (output to coverage_reports/atlas_coverage)
.\test_atlas.ps1 -Coverage
```

## 📚 Additional Documentation

*   **Core Components:**
    *   **`ATLASCore` (`core/atlas_core.py`):** Implements the core graph management and analysis logic.
        *   Uses `networkx` library to represent the system as a directed graph (`nx.DiGraph`).
        *   `map_system()`: Builds the graph based on input data defining nodes and edges.
        *   `visualize()`: Generates a visual representation of the graph using `matplotlib` and saves it to a file. Supports different layout algorithms.
        *   `_save_mapping()` / `load_mapping()`: Saves and loads the graph structure (including metadata) to/from JSON files.
        *   `analyze_system()`: Calculates various graph metrics (density, connectivity, centrality measures).
        *   `export_to_obsidian()`: Generates Markdown content and an embedded visualization image suitable for use in Obsidian notes.
    *   **`AtlasCartographer` (`core/cartographer.py`):** Acts as an interface or higher-level controller, potentially managing different mapping strategies or sources.
        *   Initializes with `MyceliumClient` for communication.
        *   Provides methods like `map_system_from_data` which likely delegates to `ATLASCore`.
        *   Includes caching (`analysis_cache`) for analysis results.
        *   Handles Mycelium subscriptions (e.g., `atlas.request.map`) to trigger mapping operations.
    *   **`AtlasService` (`service.py`):** Wraps `ATLASCore` (and potentially `AtlasCartographer`) into a service.
        *   Initializes core components with configuration and logging.
        *   Manages Mycelium interaction, subscribing to request topics (`atlas.request.map`, `atlas.request.analyze`, etc.) and publishing responses.
        *   Provides `start()` and `stop()` methods.
    *   **`config/`:** Likely holds configuration for visualization defaults, analysis options, Mycelium topics, etc.
    *   **`tests/`:** Contains unit tests for `ATLASCore`, `AtlasCartographer`, and `AtlasService`.
    *   **`data/`:** Default directory (within the instance's data path) where generated maps (JSON) and visualizations (images) are stored.

## 🔍 Key Features

*   **Graph-Based Representation:** Models systems using `networkx` directed graphs.
*   **Data-Driven Mapping:** Builds graphs from structured input data (nodes and edges with attributes).
*   **Configurable Visualization:** Generates graph visualizations using `matplotlib` with options for layout, styling, etc.
*   **Persistence:** Saves and loads graph mappings to/from JSON files.
*   **Graph Analysis:** Calculates standard network metrics.
*   **Obsidian Export:** Facilitates integration with knowledge management tools like Obsidian.
*   **Mycelium Integration:** Allows mapping and analysis to be triggered via network messages.

## 🔗 Integration

*   **Mycelium:** Listens for requests and publishes results/status updates via Mycelium topics.
*   **KOIOS:** Uses `KoiosLogger`. Configuration and data formats should align with KOIOS standards.
*   **NEXUS:** Dependency information generated by NEXUS is a key input for ATLAS to map code structures.
*   **Other Subsystems:** Can provide data (e.g., component relationships, workflow steps) to ATLAS for mapping via Mycelium requests.

## 📋 Current Status & Next Steps

*   Core logic for graph management, analysis, saving/loading, and basic visualization/export recovered and tested.
*   Mycelium integration via `AtlasService` is implemented.
*   All unit tests are passing.
*   Next steps involve:
    *   Refining visualization options and aesthetics.
    *   Implementing more advanced graph analysis features if needed.
    *   Ensuring robust handling of different data inputs for `map_system`.
    *   Adding more comprehensive documentation and examples.

## 📋 Usage (Conceptual via Mycelium)

1.  **Requesting System Mapping:**
    *   Publish a message to `atlas.request.map` topic.
    *   Payload should include `{"system_data": {...}, "map_name": "my_system_map"}` where `system_data` follows the expected node/edge structure.
    *   Listen on `response.atlas.<request_id>` for success/failure status.

2.  **Requesting Analysis:**
    *   Ensure a map has been loaded or generated.
    *   Publish a message to `atlas.request.analyze` topic.
    *   Payload can be minimal, e.g., `{}`.
    *   Listen on `response.atlas.<request_id>` for the analysis results dictionary.

3.  **Requesting Obsidian Export:**
    *   Ensure a map exists.
    *   Publish a message to `atlas.request.obsidian` topic.
    *   Payload can be minimal.
    *   Listen on `response.atlas.<request_id>` for the result containing markdown content path and image path.

*(Refer to `AtlasService` for specific topic names and payload details)*

## 🤝 Contributing

Please adhere to KOIOS standards.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
