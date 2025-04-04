---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: core
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
  category: core
  subsystem: MASTER
  status: active
  required: true
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
  category: core
  subsystem: MASTER
  status: active
  required: true
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

markdown
# Perplexity API Usage Guide

This guide documents how to use the different models of the Perplexity API available in our account and implemented in the EVA & GUARANI system.

## Available Models

Based on the tests conducted (03/03/2025), the following models are available for our account:

| Model | Response Time | Recommended Use |
|-------|---------------|-----------------|
| sonar | 2.17 seconds | Quick queries, general use |
| sonar-pro | 3.64 seconds | Higher quality responses |
| sonar-reasoning | 2.31 seconds | Questions requiring reasoning |
| sonar-reasoning-pro | 2.73 seconds | Advanced reasoning, higher quality |
| r1-1776 | 3.67 seconds | Alternative reasoning model |
| sonar-deep-research | 41.05 seconds | In-depth research, detailed investigation |

## How to Choose the Right Model

### By Task Type

- **Quick Queries**: Use `sonar` for quick answers to simple questions.
- **High Quality**: Use `sonar-pro` when quality is more important than speed.
- **Reasoning**: Use `sonar-reasoning` or `sonar-reasoning-pro` for tasks that require analysis.
- **Deep Research**: Use `sonar-deep-research` when detailed investigation is needed (note the longer response time).

### Using the Fallback Strategy

The system implements an automatic fallback strategy that tries different models in order of preference if a specific model fails. This is controlled by the `try_models_in_order` function in the `perplexity_config.py` file.

## How to Use in Code

### Basic Example

python
from EGOS.services.perplexity_service import PerplexityService

# Initialize the service
perplexity = PerplexityService()

# Make a query with the default model (sonar)
results = perplexity.search("What is the importance of solar energy in Brazil?")

# Access the results
print(results["content"])  # Response text
print(results["sources"])  # Cited sources


### Specifying a Model

python
# Use a specific model
results = perplexity.search(
    "How is artificial intelligence impacting the job market?",
    model="sonar-reasoning"
)


### Validation Levels

python
# Use strict validation (more ethical controls and source verification)
results = perplexity.search(
    "What are the main causes of global warming?",
    validate_level="strict",
    model="sonar-deep-research"
)


## Configuration

The API configuration is centralized in the `perplexity_config.py` file, which includes:

- List of available models
- Default model for different task types
- Functions for model selection and fallback
- Obtaining the API key from different sources

## Testing the Connection

Use the `check_perplexity_key.py` script to verify if your API key is configured correctly:

bash
python check_perplexity_key.py


To test the availability of all models, use the `test_perplexity_models.py` script:

bash
python test_perplexity_models.py


## Troubleshooting

### Error 401 (Unauthorized)

- Check if the API key is correct and not expired
- Confirm if the key is being sent in the correct format (`Bearer {api_key}`)
- Verify if your account has available credits

### Model Not Found

- Check if the requested model is available for your account
- Use the fallback strategy to try alternative models
- Run `test_perplexity_models.py` to identify which models are available

### Rate Limit Exceeded (429)

- Reduce the frequency of requests
- Implement a retry system with exponential backoff
- Consider distributing queries among different models

## Metrics and Performance

Based on the tests conducted, we consider the following metrics for model selection:

- **Speed**: sonar > sonar-reasoning > sonar-reasoning-pro > sonar-pro > r1-1776 > sonar-deep-research
- **Quality**: sonar-deep-research > sonar-pro > sonar-reasoning-pro > r1-1776 > sonar-reasoning > sonar
- **Cost per Token**: All models have the same cost in our current account

---

Document updated based on tests from 03/03/2025.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
