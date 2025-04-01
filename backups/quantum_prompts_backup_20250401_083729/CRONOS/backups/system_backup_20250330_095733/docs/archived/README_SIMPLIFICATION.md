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
# Simplification of the EVA & GUARANI Project



## Context



The EVA & GUARANI project was simplified to facilitate maintenance and reduce code complexity. The original architecture, which consisted of multiple interdependent files, was refactored into a more cohesive architecture, reducing the number of "hooks" between different components.



## Main Problems Solved



- **Circular Dependencies**: The original code contained several circular dependencies between modules, making error tracking difficult.

- **Incorrect Asynchronous Calls**: Asynchronous methods were being called without using `await`, causing unexpected behavior.

- **Fragmented Architecture**: Functionality was spread across many different files, making debugging complex.

- **Conversation Context Issues**: Frequent loss of context in conversations due to issues in history management.



## Implemented Solution



A unified file `unified_eva_guarani_bot.py` was created to centralize the logic of the Telegram bot and its integration with the EVA & GUARANI quantum system. This file implements:



1. **Unified Class EVAGuaraniBot**: Centralizes all bot logic

2. **Context Management**: Improved storage of conversation history

3. **Correct Asynchronous Handling**: Use of `asyncio.run()` to correctly execute asynchronous methods

4. **Robust Error Handling**: Better exception capture and logging

5. **Simplified Configuration**: Direct loading of configuration files



## How to Use



### Prerequisites



- Python 3.7+

- `python-telegram-bot` library (version 13.15 or higher)

- Configuration files in `/config/`



### Configuration



1. Ensure the file `config/telegram_config.json` exists and contains:

   json

   {

     "bot_token": "your_token_here",

     "allowed_users": [123456, 789012],

     "admin_users": [123456]

   }

   



2. Ensure the quantum system is configured in `config/quantum_config.json`



### Execution



Run the bot with the command:



bash

python unified_eva_guarani_bot.py





Additional options:

- `--config path/to/config.json`: Specifies an alternative path for the configuration file



### Bot Commands



- `/start`: Starts the conversation

- `/help`: Shows available commands

- `/status`: Checks the system status

- `/restart`: Restarts the integration with the quantum system (admin only)



## Architecture





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





## Maintenance



To keep the code simplified:



1. **Avoid adding additional files**: Try to keep the logic centralized in the unified file

2. **Document changes**: Add clear comments for any changes made

3. **Manage dependencies**: Avoid creating circular dependencies

4. **Test changes**: Ensure to test any changes in development environments



## Relation to Original Files



The unified file replaces and combines functionalities of:

- `start_telegram_eliza_bridge.py`

- Parts of `bot/quantum_integration.py`

- Parts of `bot/eva_guarani_main.py`



The original files have been kept for reference, but the execution flow is now directed by the unified file.



## Common Error Handling



### "Unexpected quantum response"

This error usually occurs when there is a problem with message processing by the quantum system. Check:

- If the `QuantumIntegration` class is working correctly

- If the returned data is in the expected format



### Connection Timeout Issues

If timeout issues occur, check:

- Your internet connection

- Increase timeout values in `request_kwargs`



---



Documentation prepared by ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧