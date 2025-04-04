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
# 📚 Unified Documentation EVA & GUARANI v7.0

> "At the intersection of modular analysis, systemic cartography, and quantum ethics, we transcend dimensions of thought."

## 📋 Index

1. [Project Simplification](#1-project-simplification)

2. [Quantum Knowledge System](#2-quantum-knowledge-system)

3. [Freemium System](#3-freemium-system)

4. [Payment System](#4-payment-system)

5. [DALL-E Image Generation](#5-dall-e-image-generation)

6. [Multilingual Support](#6-multilingual-support)

7. [Technical Architecture](#7-technical-architecture)

8. [Setup and Installation](#8-setup-and-installation)

9. [Project Structure](#9-project-structure)

---

## 1. Project Simplification

### Context

The EVA & GUARANI project was simplified to facilitate maintenance and reduce code complexity. The original architecture was refactored into a more cohesive architecture, reducing the number of "hooks" between different components.

### Main Problems Solved

- **Circular Dependencies**: Elimination of circular dependencies between modules

- **Incorrect Asynchronous Calls**: Correction of `await` usage in asynchronous methods

- **Fragmented Architecture**: Centralization of functionality into fewer files

- **Conversation Context Issues**: Improved management of conversation history

### Implemented Solution

A unified file `unified_eva_guarani_bot.py` was created to centralize the logic of the Telegram bot and its integration with the EVA & GUARANI quantum system. This file implements:

1. **Unified Class EVAGuaraniBot**: Centralizes all bot logic

2. **Context Management**: Improved storage of conversation history

3. **Correct Asynchronous Handling**: Use of `asyncio.run()` to execute asynchronous methods

4. **Robust Error Handling**: Improved exception capture and logging

5. **Simplified Configuration**: Direct loading of configuration files

### Architecture


unified_eva_guarani_bot.py

│

├── EVAGuaraniBot

│   ├── __init__

│   ├── _load_config

│   ├── _setup_telegram_bot

│   ├── _setup_quantum_integration

│   ├── _handle_* (command handlers)

│   ├── _process_with_quantum

│   ├── start

│   └── stop

│

└── main



---

## 2. Quantum Knowledge System

### Overview

The Quantum Knowledge System is an extension of the unified EVA & GUARANI bot that allows the bot to use its own internal knowledge before resorting to more expensive external models, preserving its unique identity and reducing costs.

### Components

The system is composed of the following components:

1. **Quantum Knowledge Hub**: Knowledge center that stores, indexes, and retrieves relevant information.

2. **Quantum Knowledge Integrator**: Manages communication between the bot and the knowledge hub.

3. **Telegram Bot**: User interface that allows interaction with the system.

### Directory Structure

- `config/`: Configuration files

- `logs/`: System logs

- `data/`: Database and other data

- `quantum_prompts/`: Quantum prompts and base knowledge

- `ethics/`: Ethical guidelines

- `personas/`: System personas

- `story_elements/`: Elements for narratives and stories

### Main Files

- `quantum_knowledge_hub.py`: Implements the quantum knowledge hub

- `quantum_knowledge_integrator.py`: Manages integration between the bot and the hub

- `telegram_bot_with_knowledge.py`: Implements the Telegram bot

- `test_quantum_knowledge.py`: Utility to test the system

- `integrate_quantum_knowledge.py`: Script to integrate the system into the existing bot

---

## 3. Freemium System

### Overview

The FREEMIUM system of EVA & GUARANI was designed to offer free access to the bot's basic functionalities while maintaining a sustainable model through payments and recharges for advanced features.

### Available Plans

#### 1. Free Tier

- **Regular messages**: 20 per day

- **Special calls**: 5 per day

- **Internet calls**: 5 per day

- **Recharges**: Available from R$ 5.00

#### 2. Supporter Tier

- **Regular messages**: 100 per day (5x more than the free plan)

- **Special calls**: 25 per day (5x more than the free plan)

- **Internet calls**: 25 per day (5x more than the free plan)

- **Requirement**: Minimum payment of R$ 5.00

#### 3. Premium Tier

- **Regular messages**: 500 per day (25x more than the free plan)

- **Special calls**: 100 per day (25x more than the free plan)

- **Internet calls**: 100 per day (25x more than the free plan)

- **Requirement**: Minimum payment of R$ 20.00

### Credit System

In addition to daily limits, the bot uses a credit system to manage the use of advanced resources:

- **Special calls**: Consume 1 credit per use

- **Internet calls**: Consume 1 credit per use

- **Standard recharge**: Adds 10 credits for R$ 5.00

- **Recharges in higher plans**: Add credits proportional to the amount paid

### Commands to Manage Credits

- **/credits** - Displays detailed information about your available credits and daily limits

- **/upgrade** - Shows plan options and credit recharge

- **/payment <amount> <method>** - Registers a payment and adds corresponding credits

- **/language** - Changes the interaction language with the bot

---

## 4. Payment System

### Overview

The payment system was designed to:

1. Allow users to make voluntary donations to support the bot's development and maintenance

2. Offer multiple payment options (PIX and cryptocurrencies)

3. Implement a tier system that offers additional benefits for donors

4. Manage usage limits to control API costs

### System Structure

The payment system is composed of the following components:

- **payment_gateway.py**: Main module that manages payments, user tiers, and limits

- **config/payment_config.json**: Configuration file with payment details and limits

- **data/payments/payments.json**: Database of payments and user information

### Bot Commands

- **/donate**: Displays information on how to make a donation, including PIX details and cryptocurrency addresses

- **/donation**: Allows the user to register a donation made (format: `/donation <amount> <method>`)

### Payment Methods

#### PIX

- **Key**: 10689169663

- **Name**: Enio Batista Fernandes Rocha

#### Cryptocurrencies

- **Bitcoin (Segwit)**: bc1qy9vr32f2hsjyapt3jz7fen6g0lxrehrqahwj3m

- **Solana**: 2iWboZwTkJ5ofCB2wXApa5ReeyJwUFRXrBgHyFRSy6a1

- **Ethereum (BASE chain)**: 0xa858F22c8C1f3D5059D101C0c7666Ed0C2BF53ac

### Payment Registration

Payments are registered in the file `data/payments/payments.json` with the following structure:

json
{
  "users": {
    "123456789": {
      "total_donated": 25.0,
      "donations_count": 2,
      "last_donation": "2024-03-03T15:30:45.123456",
      "tier": "premium_tier"
    }
  },
  "transactions": [...]
}


---

## 5. DALL-E Image Generation

### Overview

Integration with OpenAI's DALL-E API allows the EVA & GUARANI bot to generate high-quality images from textual descriptions. This functionality:

- Supports DALL-E 2 and DALL-E 3 models

- Allows customization of size, quality, and style

- Saves generated images locally and provides URLs

- Integrates with the FREEMIUM system, consuming special call credits

### How to Use

#### Basic Command


/image [image description]


**Example:**


/image A cat astronaut floating in space, digital art style


#### Advanced Options

You can customize image generation with the following parameters:


/image [image description] --model [model] --size [size] --quality [quality] --style [style]


### Credit Cost

Image generation consumes special call credits, with costs varying according to model, size, and quality:

| Model | Size | Quality | Cost (credits) |

|--------|---------|-----------|------------------|

| DALL-E 2 | 256x256 | - | 1 |

| DALL-E 2 | 512x512 | - | 1 |

| DALL-E 2 | 1024x1024 | - | 2 |

| DALL-E 3 | 1024x1024 | standard | 2 |

| DALL-E 3 | 1024x1024 | hd | 3 |

| DALL-E 3 | 1792x1024 | standard | 3 |

| DALL-E 3 | 1792x1024 | hd | 4 |

| DALL-E 3 | 1024x1792 | standard | 3 |

| DALL-E 3 | 1024x1792 | hd | 4 |

### Tips for Good Results

1. **Be specific and detailed**: The more details you provide, the better the result.

2. **Specify the artistic style**: Mention the desired style for better results.

3. **Describe the lighting**: Lighting drastically affects the result.

4. **Mention perspective/angle**: Defines how the image will be composed.

---

## 6. Multilingual Support

EVA & GUARANI offers support for multiple languages:

- Upon starting, you can choose your preferred language

- Change language at any time with the `/language` command

- Practicing in a language other than your native one is encouraged as a learning tool

- Receive explanations and grammatical corrections when using the language assistant mode

### Available Languages

- 🇧🇷 Portuguese (Brazil)

- 🇺🇸 English

- 🇪🇸 Spanish

- 🇫🇷 French

### How to Change Language

Use the `/language` command followed by the language code:

- `/language pt` - For Portuguese

- `/language en` - For English

- `/language es` - For Spanish

- `/language fr` - For French

---

## 7. Technical Architecture

### Architecture Overview

The EVA & GUARANI system follows a modular architecture where each component has a specific responsibility:


EVA & GUARANI

├── Core

│   ├── Unified Bot (unified_eva_guarani_bot.py)

│   ├── Quantum Knowledge System (quantum_knowledge_hub.py)

│   └── Configuration Manager (config_manager.py)

│

├── Business Systems

│   ├── Freemium System (freemium_manager.py)

│   ├── Payment Gateway (payment_gateway.py)

│   └── Credit Manager (credit_manager.py)

│

├── External Integrations

│   ├── DALL-E Integration (dalle_integration.py)

│   ├── Web Search (web_search.py)

│   └── Perplexity API (perplexity_integration.py)

│

├── Support Systems

│   ├── Multilingual (language_support.py)

│   ├── Logging System (logging_system.py)

│   └── Monitoring (monitoring.py)

│

└── Interfaces

    ├── Telegram Bot (telegram_interface.py)

    └── Web API (web_api.py)



### Data Flow

1. The user sends a message through the Telegram interface

2. The Unified Bot receives the message and checks usage limits (Freemium)

3. The system attempts to process the message using internal Quantum Knowledge

4. If necessary, it resorts to external APIs (such as OpenAI or Perplexity)

5. The result is processed, logged, and sent back to the user

6. Credits and usage statistics are updated

### Technologies Used

- **Python 3.7+**: Main language

- **python-telegram-bot**: Interface with Telegram

- **OpenAI API**: For content and image generation

- **SQLite/Json**: Data storage

- **asyncio**: For asynchronous operations

---

## 8. Setup and Installation

### Prerequisites

- Python 3.7+

- pip (Python package manager)

- Telegram account (to obtain a bot token)

- OpenAI API key (optional, for advanced features)

- Perplexity API key (optional, for web searches)

### Basic Installation

1. Clone the repository:

   bash
   git clone https://github.com/your-username/eva-guarani.git

   cd eva-guarani



2. Install dependencies:

   bash
   pip install -r requirements.txt



3. Configure essential files:

   bash
   # On Windows

   copy config\config_template.json config\config.json



   # On Linux/Mac

   cp config/config_template.json config/config.json



4. Edit configuration files with your API keys and preferences

5. Start the bot:

   bash
   # Unified version

   python unified_eva_guarani_bot.py



   # Version with knowledge system

   python telegram_bot_with_knowledge.py



### Startup Scripts

To facilitate startup, you can use the included scripts:

- **Windows**: Run `start_bot.bat` or `start_eva_guarani_unified.bat`

- **Linux/Mac**: Run `start_bot.sh` or `start_eva_guarani_unified.sh`

### Common Troubleshooting

#### "Unable to connect to Telegram"

- Check your internet connection

- Confirm that the bot token in `config/telegram_config.json` is correct

#### "Error loading configurations"

- Ensure that configuration files exist and are valid

- Check file permissions

#### "API limit exceeded"

- Wait a few minutes and try again

- Check if your API keys are valid and have sufficient credits

---

## 9. Project Structure

### Complete Directory Structure


EVA & GUARANI

├── bot/                     # Main bot components

│   ├── handlers/            # Command handlers

│   └── core/                # Main bot functions

│

├── config/                  # System configurations

│   ├── telegram_config.json # Telegram configuration

│   ├── api_config.json      # External API configurations

│   ├── payment_config.json  # Payment system configurations

│   └── quantum_config.json  # Quantum component configurations

│

├── data/                    # System data

│   ├── knowledge/           # Knowledge base

│   ├── payments/            # Payment records

│   ├── users/               # User data

│   └── images/              # Images generated by DALL-E

│

├── docs/                    # Documentation

│   ├── UNIFIED_DOCUMENTATION.md  # Main documentation

│   ├── PROMETHEUS_GRAFANA_INTEGRATION.md  # Integration documentation

│   └── archived/            # Archived old READMEs

│

├── ethics/                  # Ethical guidelines implementation

│   ├── ethical_guidelines.py

│   └── moderation.py

│

├── logs/                    # System logs

│   ├── error_logs/

│   ├── usage_logs/

│   └── payment_logs/

│

├── modules/                 # Functional modules

│   ├── quantum/             # Quantum components

│   ├── mycelium/            # Mycelial network of connections

│   ├── integration/         # External system integrations

│   └── security/            # Security components

│

├── personas/                # System personas

│   ├── knowledge_guardian.py

│   ├── quantumArtist.py

│   └── ethicalNavigator.py

│

├── quantum_prompts/         # Quantum prompts for LLM

│   ├── eva_guarani_quantum_master.md

│   └── INTEGRATED_SYSTEM.md

│

├── story_elements/          # Narrative elements for RPG

│   ├── characters/

│   ├── locations/

│   └── quests/

│

├── tests/                   # Automated tests

│   ├── test_bot.py

│   ├── test_payment.py

│   └── test_quantum_knowledge.py

│

├── utils/                   # Utilities

│   ├── text_processing.py

│   ├── image_processing.py

│   └── security_utils.py

│

├── .cursor/                 # Cursor IDE configurations

│   └── rules/               # Rules for quantum prompt

│       ├── eva_guarani_quantum.mcp

│       ├── quantum_cursor.mcp

│       └── megaprompt.mdc

│

├── requirements.txt         # Project dependencies

├── README.md                # Main documentation

├── unified_eva_guarani_bot.py  # Main unified bot

└── telegram_bot_with_knowledge.py  # Bot with knowledge system



### Main Files

| File | Description |

|---------|-----------|

| `unified_eva_guarani_bot.py` | Main implementation of the unified bot |

| `quantum_knowledge_hub.py` | Central hub of quantum knowledge |

| `payment_gateway.py` | Payment system and credit management |

| `dalle_integration.py` | Integration with DALL-E API for image generation |

| `perplexity_integration.py` | Integration with Perplexity for web searches |

| `start_bot.bat/.sh` | Scripts to start the bot |

| `requirements.txt` | List of Python dependencies |

| `config/telegram_config.json` | Telegram bot configuration |

### Utility Scripts

The project includes several utility scripts for facilitating common operations:

- `check_dependencies.py`: Checks if all dependencies are installed

- `check_bot_status.py`: Checks the current status of the bot

- `setup_quantum_knowledge_system.py`: Sets up the quantum knowledge system

- `check_perplexity_key.py`: Checks the validity of the Perplexity API key

- `create_full_backup.ps1
