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
# EVA & GUARANI - Telegram Integration with ElizaOS



✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧



## Overview



This framework implements an integration between the EVA & GUARANI Telegram bot and the ElizaOS framework, allowing the separation between the connection layer and business logic. This enables the bot to remain online while the development of new features continues.



## Architecture



The architecture was designed with the following principles:



1. **Separation of Responsibilities**:

   - Telegram connection code separated from business logic

   - ElizaOS as an abstraction layer for message processing

   - Bridge as a component for communication between systems



2. **Resilience**:

   - Automatic failure recovery

   - Continuous monitoring

   - Detailed logging system



3. **Modularity**:

   - Independent and replaceable components

   - Clear interfaces between modules

   - Easy extension and maintenance



## Directory Structure





/

├── bot/

│   ├── eliza_integration.py      # ElizaOS integration module

│   └── ...

├── config/

│   ├── telegram_config.json      # Telegram bot configuration

│   ├── eliza_config.json         # ElizaOS configuration

│   └── ...

├── eliza/                        # Directory where ElizaOS will be installed

├── logs/                         # Directory for log storage

├── install_eliza_integration.ps1 # ElizaOS installation script

├── start_telegram_eliza_bridge.py # Main bridge script

├── start_telegram_eliza_bridge.bat # Batch file to start the bridge

└── ...





## Main Components



### 1. ElizaOS Integration Module (`bot/eliza_integration.py`)



This module provides the necessary classes and functions to integrate ElizaOS with our EVA & GUARANI ecosystem.



**Key components**:

- `ElizaIntegration`: Manages communication with ElizaOS

- `ElizaBot`: Adapter for processing Telegram messages

- `setup_eliza()`: Configures and starts the integration



### 2. Telegram-ElizaOS Bridge (`start_telegram_eliza_bridge.py`)



Responsible for receiving messages from Telegram, sending them for processing in ElizaOS, and returning the responses.



**Main functionalities**:

- User authentication management

- Message routing

- Command handling

- State monitoring

- Failure recovery



### 3. ElizaOS Installer (`install_eliza_integration.ps1`)



PowerShell script that automates the installation and configuration of ElizaOS for integration with the Telegram bot.



**Functions**:

- Requirements check (Node.js, npm, pnpm, Python, Git)

- Cloning the ElizaOS repository

- Dependency installation

- Environment configuration

- Creation of startup scripts



## Installation Guide



### Prerequisites



- Windows 10 or higher (for PowerShell scripts)

- Python 3.6+

- Node.js 23+

- Git

- Internet connection



### Installation Steps



1. **Configure the bot token**:

   

   Edit the file `config/telegram_config.json` and add the bot token:

   

   json

   {

     "bot_token": "7642662485:AAHqu2VIY2sCLKMNvqO5o8thbjhyr1aimiw",

     "admin_users": [171767219],

     "allowed_users": []

   }

   



2. **Install ElizaOS**:

   

   Run the installation script:

   

   powershell

   .\install_eliza_integration.ps1

   



3. **Start the Bridge**:

   

   Run the batch file to start the bridge:

   

   

   start_telegram_eliza_bridge.bat

   



## Usage



### Bot Commands



- `/start` - Starts the conversation and checks permissions

- `/help` - Shows help about available commands

- `/status` - Checks the system status (bot, ElizaOS, bridge)

- `/restart` - Restarts the integration with ElizaOS (admins only)



### User Management



The system supports two access levels:



1. **Administrators** (`admin_users`):

   - Full access to the bot

   - Can use administrative commands

   - Receive notifications of errors and important events



2. **Allowed Users** (`allowed_users`):

   - Can interact with the bot

   - Restricted access to non-administrative commands



If the `allowed_users` list is empty, only administrators will be able to use the bot.



## Maintenance



### Logs



Logs are stored in the `logs/` directory and include:



- `logs/telegram_eliza_bridge.log` - Logs of the Telegram-ElizaOS bridge

- `logs/eliza_integration.log` - Logs of the ElizaOS integration

- `logs/eliza_install.log` - Logs of the ElizaOS installation



### Restarting the System



To restart the system in case of issues:



1. Close any running instance of the bridge

2. Run the restart command:





start_telegram_eliza_bridge.bat





Or send the `/restart` command to the bot (as an administrator).



## Development



### System Extension



To add new features:



1. **Custom Handlers**:

   

   Add new handlers in the `TelegramElizaBridge` class in the `start_telegram_eliza_bridge.py` file:

   

   python

   dispatcher.add_handler(CommandHandler("mycommand", self._handle_mycommand))

   

   def _handle_mycommand(self, update: Update, context: CallbackContext) -> None:

       # Handler implementation

   



2. **Integration with ElizaOS**:

   

   Extend the `ElizaBot` class in `bot/eliza_integration.py` to add specific functionalities.



### Message Format



The bridge converts Telegram messages to a format compatible with ElizaOS:



python

eliza_update = {

    "update_id": update.update_id,

    "message": {

        "message_id": update.effective_message.message_id,

        "from": {

            "id": update.effective_user.id,

            # ...

        },

        "chat": {

            "id": update.effective_chat.id,

            # ...

        },

        "text": update.effective_message.text,

        # ...

    }

}





## References



- [ElizaOS GitHub](https://github.com/elizaOS/eliza)

- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)

- [Telegram Bot API](https://core.telegram.org/bots/api)



## License



This project is part of the EVA & GUARANI ecosystem and follows the ethical principles established in the integrated consciousness quantum matrix.



---



Developed as part of the EVA & GUARANI system with ethical awareness, unconditional love, and focus on evolutionary preservation.



✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧