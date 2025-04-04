---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: docs
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

# Perplexity API Integration for EVA & GUARANI

## Overview

This document describes the integration of the Perplexity API with the EVA & GUARANI system, enabling real-time, AI-powered search capabilities that enhance the knowledge base with up-to-date information.

The Perplexity API integration allows EVA & GUARANI to:

1. Perform real-time internet searches with natural language queries
2. Adapt searches based on active personas
3. Apply ethical filtering to search results
4. Preserve knowledge in the system's memory
5. Maintain source attribution for transparency

## Architecture

The integration consists of three main components:

1. **PerplexityClient** (`tools/integration/perplexity_client.py`) - Handles direct API communication
2. **PerplexityIntegration** (`tools/integration/perplexity_integration.py`) - Connects Perplexity with EVA & GUARANI
3. **Test Utilities** (`tools/integration/test_perplexity.py`) - Provides testing capabilities

### Integration with EVA & GUARANI Core Modules

The Perplexity integration connects with:

- **ETHIK** - For ethical evaluation of search results
- **CRONOS** - For preserving knowledge obtained from searches
- **Persona System** - For persona-specific search queries

## Setup

### Prerequisites

- Python 3.9+
- Perplexity API key

### Configuration

1. Add your Perplexity API key to the `.env` file:

```
PERPLEXITY_API_KEY=your_api_key_here
PERPLEXITY_DEFAULT_MODEL=sonar-medium-online
```

2. Install required dependencies:

```bash
pip install requests python-dotenv
```

## Usage

### Command Line Interface

Use the provided launcher scripts:

#### Windows

```
tools\launchers\perplexity_search.bat "your search query" --persona philosopher
```

#### Linux/Mac

```
./tools/launchers/perplexity_search.sh "your search query" --persona scientist
```

### Python API

```python
from tools.integration.perplexity_integration import PerplexityIntegration

# Initialize the integration
integration = PerplexityIntegration()

# Perform a search
result = await integration.enhance_knowledge(
    query="What is the latest development in quantum computing?",
    persona="scientist"
)

# Access the results
content = result['knowledge']['content']
sources = result['knowledge']['sources']
```

## Persona-Specific Searches

The integration adapts queries based on the active persona:

- **Philosopher**: Focuses on ethical, epistemological, and metaphysical aspects
- **Scientist**: Emphasizes empirical evidence, theories, and research
- **Gamer**: Considers game mechanics, player experience, and gaming culture
- **Economist**: Analyzes market dynamics, economic theories, and financial implications

## Ethical Considerations

Search results are processed through the ETHIK module when available, which:

1. Evaluates content for ethical concerns
2. Filters problematic content
3. Provides warnings when content has been modified

## Knowledge Preservation

The integration uses CRONOS to preserve valuable knowledge:

1. Search results are stored with metadata
2. Results are tagged with the originating query and persona
3. Timestamps ensure proper chronological context

## Technical Details

### API Parameters

- **model**: The Perplexity model to use (default: sonar-medium-online)
- **max_tokens**: Maximum tokens in the response (default: 800)
- **temperature**: Creativity temperature (default: 0.7)

### Caching

Results are cached to:

- Reduce API usage
- Improve response times
- Preserve attribution information

### Error Handling

The integration includes robust error handling for:

- API connection issues
- Rate limiting
- Invalid queries
- Authentication errors

## Future Enhancements

1. **Advanced Filtering**: More sophisticated content filtering options
2. **Knowledge Integration**: Deeper integration with EVA & GUARANI's knowledge base
3. **Multilingual Support**: Support for non-English queries and results
4. **Query Refinement**: Automatic query improvement based on context

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
