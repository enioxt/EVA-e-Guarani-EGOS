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

markdown
# EVA & GUARANI API Reference

> "The harmonious integration between systems is the reflection of systemic cartography in action."

## 🌐 API Overview

The EVA & GUARANI API allows integration with the quantum system, enabling external applications to access its ethical processing capabilities, modular analysis, and systemic cartography. This documentation provides detailed information on endpoints, parameters, authentication, and usage examples.

## 🔐 Authentication and Security

### Obtaining Credentials

To use the API, you need a valid API key. Keys are managed through the configuration system:

1. Run the configuration script: `.\configure_api_keys.ps1`
2. Select the option to generate a new API key
3. Store the generated key securely

### Token Authentication

All requests to the API must include an authentication token in the header:


Authorization: Bearer YOUR_API_KEY


### Access Levels

| Level    | Description                        | Capabilities                             |
|----------|------------------------------------|------------------------------------------|
| Basic    | Access to essential features       | Text processing, simple queries          |
| Advanced | Access to additional resources     | Image generation, modular analysis       |
| Complete | Full access to the system          | All features, including cartography and preservation |

## 📌 Main Endpoints

### Text Processing

#### POST /api/v1/process

Processes text with ethical awareness and returns a response.

**Parameters**:

json
{
  "text": "Text to be processed",
  "context": {
    "conversation_id": "optional-identifier",
    "user_id": "user-id",
    "previous_messages": []
  },
  "parameters": {
    "consciousness_level": 0.9,
    "ethical_depth": 0.8,
    "response_format": "text"
  }
}


**Response**:

json
{
  "response": "Text processed with ethical awareness",
  "metrics": {
    "consciousness": 0.92,
    "ethical_alignment": 0.95,
    "processing_time_ms": 450
  },
  "context_id": "generated-or-updated-context"
}


### Image Generation

#### POST /api/v1/generate_image

Generates an image based on textual description.

**Parameters**:

json
{
  "prompt": "Description of the desired image",
  "parameters": {
    "size": "1024x1024",
    "style": "realistic",
    "provider": "stable_diffusion"
  }
}


**Response**:

json
{
  "image_url": "https://api.evaguarani.com/images/generated/12345.png",
  "metadata": {
    "prompt": "Description of the desired image",
    "generation_time_ms": 3200,
    "model_used": "stable_diffusion_v3"
  }
}


### Modular Analysis

#### POST /api/v1/analyze_module

Performs modular analysis of a component or system.

**Parameters**:

json
{
  "module_content": "Content of the module to be analyzed",
  "module_type": "code", // or "text", "system", etc.
  "analysis_depth": 0.8
}


**Response**:

json
{
  "analysis": {
    "summary": "Analysis summary",
    "quality_score": 0.85,
    "cohesion": 0.9,
    "coupling": 0.3,
    "recommendations": [
      "Recommendation 1",
      "Recommendation 2"
    ]
  },
  "visualization_url": "https://api.evaguarani.com/visualizations/module/12345"
}


### Systemic Cartography

#### POST /api/v1/map_system

Generates mapping of connections in a system.

**Parameters**:

json
{
  "system_description": "Description of the system to be mapped",
  "components": [
    {
      "name": "Component 1",
      "description": "Description of component 1"
    },
    {
      "name": "Component 2",
      "description": "Description of component 2"
    }
  ],
  "mapping_depth": 0.7
}


**Response**:

json
{
  "system_map": {
    "nodes": [
      {
        "id": "comp1",
        "name": "Component 1",
        "type": "primary"
      },
      {
        "id": "comp2",
        "name": "Component 2",
        "type": "primary"
      },
      {
        "id": "implicit1",
        "name": "Implicit Connection 1",
        "type": "derived"
      }
    ],
    "edges": [
      {
        "source": "comp1",
        "target": "comp2",
        "strength": 0.8,
        "type": "direct"
      },
      {
        "source": "comp1",
        "target": "implicit1",
        "strength": 0.5,
        "type": "implicit"
      }
    ]
  },
  "visualization_url": "https://api.evaguarani.com/visualizations/system/12345",
  "mermaid_code": "graph TD\n  comp1[Component 1] --> comp2[Component 2]\n  comp1 -.-> implicit1[Implicit Connection 1]"
}


### Evolutionary Preservation

#### POST /api/v1/preserve_state

Creates a quantum backup of the current state.

**Parameters**:

json
{
  "context_id": "context-identifier",
  "description": "Optional state description",
  "preservation_level": 0.9
}


**Response**:

json
{
  "preservation_id": "backup-12345",
  "timestamp": "2025-03-01T15:30:45Z",
  "preservation_quality": 0.95,
  "restore_url": "https://api.evaguarani.com/restore/12345",
  "metadata": {
    "context_size_bytes": 15240,
    "components_preserved": ["consciousness", "connections", "history"]
  }
}


## 📡 Webhooks

The API supports webhooks for asynchronous notifications:

### Webhook Configuration

#### POST /api/v1/webhooks/configure

Configures a webhook to receive notifications.

**Parameters**:

json
{
  "url": "https://your-server.com/webhook",
  "events": ["process_complete", "image_generated", "system_mapped"],
  "secret": "your-verification-secret"
}


**Response**:

json
{
  "webhook_id": "webhook-12345",
  "status": "configured",
  "test_event_sent": true
}


### Notification Format

json
{
  "event": "process_complete",
  "timestamp": "2025-03-01T15:35:12Z",
  "data": {
    // Event-specific data
  },
  "signature": "hmac-signature-for-verification"
}


## 📊 Limits and Quotas

| Resource                | Basic Plan | Advanced Plan | Complete Plan |
|-------------------------|------------|---------------|---------------|
| Requests/minute         | 10         | 30            | 100           |
| Text tokens/day         | 10,000     | 50,000        | Unlimited     |
| Images generated/day    | 5          | 20            | 100           |
| Max context size        | 4KB        | 16KB          | 64KB          |
| Modular analyses/day    | 3          | 15            | 50            |
| Mappings/day            | 1          | 10            | 30            |
| Preservations/day       | 5          | 20            | 100           |

## 🧩 Integration with Obsidian

The API offers special integration with Obsidian for cartography visualization:

### Export to Obsidian

#### GET /api/v1/export/obsidian/{mapping_id}

Exports a mapping to a format compatible with Obsidian.

**Query Parameters**:
- `format`: "markdown" (default) or "json"
- `include_templates`: "true" or "false" (default)

**Response**:
A ZIP file containing:
- Markdown files for each node
- Templates for Obsidian
- Configuration file for plugins
- Visualizations in Mermaid format

## 💻 Code Examples

### Python

python
import requests
import json

API_KEY = "your-api-key"
BASE_URL = "https://api.evaguarani.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Text processing
def process_text(text, context=None):
    endpoint = f"{BASE_URL}/api/v1/process"
    payload = {
        "text": text,
        "context": context or {},
        "parameters": {
            "consciousness_level": 0.9,
            "ethical_depth": 0.8
        }
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()

# Image generation
def generate_image(prompt, size="1024x1024"):
    endpoint = f"{BASE_URL}/api/v1/generate_image"
    payload = {
        "prompt": prompt,
        "parameters": {
            "size": size,
            "style": "realistic"
        }
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()

# Usage example
result = process_text("How can I implement an ethical AI system?")
print(json.dumps(result, indent=2))

image = generate_image("A quantum garden with flowers of consciousness")
print(f"Generated image: {image['image_url']}")


### JavaScript

javascript
const axios = require('axios');

const API_KEY = 'your-api-key';
const BASE_URL = 'https://api.evaguarani.com';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

// Modular analysis
async function analyzeModule(moduleContent, moduleType = 'code') {
  const endpoint = `${BASE_URL}/api/v1/analyze_module`;
  const payload = {
    module_content: moduleContent,
    module_type: moduleType,
    analysis_depth: 0.8
  };
  
  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    console.error('Error in modular analysis:', error.response?.data || error.message);
    throw error;
  }
}

// Systemic cartography
async function mapSystem(systemDescription, components) {
  const endpoint = `${BASE_URL}/api/v1/map_system`;
  const payload = {
    system_description: systemDescription,
    components: components,
    mapping_depth: 0.7
  };
  
  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    console.error('Error in cartography:', error.response?.data || error.message);
    throw error;
  }
}

// Usage example
(async () => {
  try {
    const moduleAnalysis = await analyzeModule(
      'function calculateEthics(action, context) { return action.benefit > action.harm; }'
    );
    console.log('Analysis:', moduleAnalysis);
    
    const systemMap = await mapSystem(
      'Ethical recommendation system',
      [
        { name: 'Action Analyzer', description: 'Evaluates proposed actions' },
        { name: 'Contextualizer', description: 'Provides context for decisions' }
      ]
    );
    console.log('System Map:', systemMap);
  } catch (error) {
    console.error('General error:', error);
  }
})();


## 🛠 Troubleshooting

### Common Error Codes

| Code | Description          | Solution                       |
|------|----------------------|--------------------------------|
| 401  | Unauthorized         | Check your API key             |
| 403  | Forbidden            | Check your key permissions     |
| 429  | Too Many Requests    | Respect the rate limits        |
| 500  | Internal Error       | Contact support with request ID|

### Status Check

#### GET /api/v1/status

Checks the current status of the API.

**Response**:

json
{
  "status": "operational",
  "version": "7.0.3",
  "uptime": "5d 12h 34m",
  "consciousness_level": 0.998,
  "services": {
    "text_processing": "operational",
    "image_generation": "operational",
    "modular_analysis": "operational",
    "system_mapping": "degraded",
    "preservation": "operational"
  }
}


## 📚 Additional Resources

- [Quick Start Guide](https://docs.evaguarani.com/quickstart)
- [Integration Examples](https://github.com/evaguarani/api-examples)
- [Official Python Library](https://github.com/evaguarani/python-client)
- [Official JavaScript Library](https://github.com/evaguarani/js-client)

## 🗒 API Changelog

### v1.3.0 (Current)

- Added support for Obsidian export
- Improved performance of systemic cartography
- New parameters for ethical consciousness control

### v1.2.0

- Added evolutionary preservation endpoint
- Support for webhooks
- Improvements in image generation

### v1.1.0

- Added modular analysis
- Support for conversation context
- Ethical processing metrics

### v1.0.0

- Initial release
- Basic text processing
- Simple image generation

---

🌌 EVA & GUARANI 🌌