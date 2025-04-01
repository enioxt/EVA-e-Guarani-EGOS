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
# Usage Guide for Perplexity API Integration with EVA & GUARANI

## Introduction

The integration of the Perplexity API with the EVA & GUARANI system allows the quantum model to access up-to-date information from the internet in an ethical and secure manner. This guide explains how to set up and use this functionality.

## Initial Configuration

### 1. API Key
The Perplexity API key has already been configured in the system:

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


This key is securely stored in the configuration file `EGOS/config/api_keys.json`.

### 2. Configuration Verification

To verify if the API is configured correctly, run:

python
from services.config import config_manager

if config_manager.is_configured("perplexity"):
    print("Perplexity API successfully configured!")
    print(f"Key: {config_manager.get_key('perplexity')[:8]}...")
else:
    print("Perplexity API not configured.")


## How to Use

### Basic Usage

python
from modules.perplexity_integration import PerplexityIntegration

# Initialize the module
perplexity = PerplexityIntegration()

# Perform a simple query
results = perplexity.search("What are the main technological trends of 2024?")

# Display the results
print(results["content"])

# Check the sources
for source in results["sources"]:
    print(f"{source['title']} - {source['url']}")


### Validation Levels

The integration offers three validation levels for queries:

1. **basic**: Minimal validation, ideal for simple and non-sensitive queries
2. **standard** (default): Balance between rigor and performance
3. **strict**: Maximum validation, recommended for sensitive topics or those requiring high accuracy

python
# Query with strict validation
results = perplexity.search(
    "What are the main security risks in REST APIs?",
    validation_level="strict"
)


### Ethical Filter

By default, all queries go through an ethical filter that analyzes whether the content is appropriate. This filter can be disabled in specific cases:

python
# Disable the ethical filter (use with caution)
results = perplexity.search(
    "History of conflicts in the Middle East",
    ethical_filter=False
)


### Providing Context

You can provide additional context for better ethical analysis of the query:

python
# Query with context
context = "I am developing an academic paper on cybersecurity"
results = perplexity.search(
    "Common attack techniques on web systems",
    context=context
)


## Result Structure

Results are returned in a quantum format optimized for the EVA & GUARANI system:

json
{
  "status": "success",
  "query": "Original query",
  "content": "Response obtained from the Perplexity API",
  "metadata": {
    "timestamp": "2024-06-14T14:30:00Z",
    "validation_level": "standard",
    "confidence_score": 0.85,
    "sensitivity_warning": null
  },
  "sources": [
    {
      "title": "Source title",
      "url": "https://example.com",
      "reliability": 0.78
    }
  ],
  "potential_biases": [],
  "validation_note": ""
}


## Reliability Analysis

The system automatically estimates the reliability of sources using various criteria:

- Academic (.edu), governmental (.gov), and organizational (.org) domains receive higher scores
- Wikipedia receives a moderately high score
- Blogs, forums, and news sites receive a lower score
- Sensationalist titles reduce the score

## Query History

You can access the history of queries made:

python
# Get query history
history = perplexity.get_query_history()

# Display history
for entry in history:
    print(f"Query: {entry['query']}")
    print(f"Timestamp: {entry['timestamp']}")
    if entry.get('context'):
        print(f"Context: {entry['context']}")
    print("-" * 40)

# Clear history
perplexity.clear_history()


## Integration with EVA & GUARANI Subsystems

### Integration with ATLAS (Systemic Mapping)

Information obtained from the internet can be mapped and connected to existing knowledge:

python
# Conceptual example of integration with ATLAS
query = "Recent advances in machine learning"
results = perplexity.search(query)

# The result would be automatically integrated into the systemic mapping
# performed by the ATLAS module, connecting new knowledge
# with the existing base.


### Integration with NEXUS (Modular Analysis)

Information can be analyzed modularly to identify essential components:

python
# Conceptual example of integration with NEXUS
query = "Microservices architecture in 2024"
results = perplexity.search(query)

# NEXUS would analyze each component of the architecture
# described in the results.


### Integration with CRONOS (Evolutionary Preservation)

The history of queries and results is preserved for future reference:

python
# Conceptual example of integration with CRONOS
# All query history is automatically preserved
# by the CRONOS subsystem, maintaining the context and evolution
# of information over time.


## Complete Example

python
from modules.perplexity_integration import PerplexityIntegration

# Initialize the module
perplexity = PerplexityIntegration()

try:
    # Perform search with strict validation
    results = perplexity.search(
        "Impacts of generative artificial intelligence on society",
        validation_level="strict",
        context="Academic research on ethics and technology"
    )
    
    if results["status"] == "success":
        print("\n=== SEARCH RESULTS ===\n")
        print(results["content"])
        
        print("\n=== SOURCES ===\n")
        for i, source in enumerate(results["sources"], 1):
            print(f"{i}. {source['title']}")
            print(f"   URL: {source['url']}")
            print(f"   Reliability: {source['reliability']:.2f}")
        
        print("\n=== METADATA ===\n")
        print(f"Validation level: {results['metadata']['validation_level']}")
        print(f"Confidence score: {results['metadata']['confidence_score']:.2f}")
        
        if results['potential_biases']:
            print("\n=== POTENTIAL BIASES ===\n")
            for bias in results['potential_biases']:
                print(f"- {bias}")
    else:
        print(f"Error: {results.get('reason', 'Unknown failure')}")
        
except Exception as e:
    print(f"Error during search: {e}")


## Troubleshooting

### Invalid API Key

If the API returns an authentication error, check if the key is configured correctly:

python
from services.config import config_manager

# Check the current key
print(config_manager.get_key("perplexity"))

# Set a new key
config_manager.set_key("perplexity", "your-new-key-here")


### API Limits

The Perplexity API has usage limits. If you receive errors related to exceeded limits, consider:

1. Reducing the frequency of queries
2. Implementing a cache system for frequent queries
3. Contacting Perplexity to increase your limits

### Connection Failures

In case of connection failures:

1. Check your internet connection
2. Confirm that the Perplexity service is online
3. Implement retry logic with exponential backoff to handle temporary failures

## Ethical Considerations

When using the integration with the Perplexity API, always keep in mind:

1. **Respect for privacy**: Do not use the API to query private or sensitive information
2. **Information verification**: Always validate information obtained with multiple sources
3. **Responsible use**: Do not use for illegal or unethical activities
4. **Biases and limitations**: Be aware of potential biases in the information obtained
5. **Transparency**: Be transparent about the origin of information when sharing it

## Conclusion

The integration with the Perplexity API significantly enhances the capabilities of the EVA & GUARANI system, allowing access to up-to-date internet information while maintaining the fundamental ethical and philosophical principles of the quantum system.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧