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
# 📘 Installation and Configuration Guide - EVA & GUARANI

This guide provides detailed instructions to install, configure, and run the EVA & GUARANI system, focusing on the Unified Telegram Bot (version 7.0).

## 📋 System Requirements

- Python 3.8 or higher
- Pip (Python package manager)
- FFmpeg (for video processing)
- Internet access for external APIs
- Telegram Bot Token (obtained via @BotFather)
- API keys for optional services:
  - OpenAI API
  - Stable Diffusion API
  - Unsplash API
  - Pexels API
  - Pixabay API

## 🛠 Installation

### 1. Environment Preparation

1. Clone the repository or download the files:

   bash
   git clone https://github.com/enioxt/ava-tech-art-bot.git
   cd ava-tech-art-bot
   

2. Create and activate a virtual environment (recommended):

   bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   

3. Install the dependencies:

   bash
   pip install -r requirements.txt
   

### 2. FFmpeg Installation (for video functionalities)

#### Windows:

1. Download FFmpeg from the official site: https://ffmpeg.org/download.html
2. Extract the files to a folder (e.g., C:\ffmpeg)
3. Add the bin folder path to the system PATH:
   - Control Panel > System > Advanced system settings > Environment Variables
   - Edit the PATH variable and add the path (e.g., C:\ffmpeg\bin)

#### Linux:

bash
sudo apt update
sudo apt install ffmpeg


#### macOS:

bash
brew install ffmpeg


## ⚙️ Configuration

### 1. Telegram Bot Configuration

1. Obtain a token for your bot:
   - Open Telegram and search for @BotFather
   - Send the command `/newbot` and follow the instructions
   - Save the provided token

2. Configure the configuration file:
   - On the first run, the system will automatically create the file `config/bot_config.json`
   - You can also manually create this file:

json
{
  "telegram_token": "YOUR_TOKEN_HERE",
  "openai_api_key": "YOUR_OPENAI_KEY_HERE",
  "allowed_users": [123456789],
  "admin_users": [123456789],
  "consciousness_level": 0.998,
  "love_level": 0.995,
  "max_tokens": 1000,
  "default_model": "gpt-4o"
}


### 2. Image APIs Configuration (Optional)

To enable image generation and search, configure the APIs in the file `config/telegram_config.json`:

json
{
  "stable_diffusion_api": {
    "url": "https://stablediffusionapi.com/api/v3/text2img",
    "key": "YOUR_KEY_HERE"
  },
  "pexels_api": {
    "key": "YOUR_KEY_HERE"
  },
  "unsplash_api": {
    "key": "YOUR_KEY_HERE"
  },
  "pixabay_api": {
    "key": "YOUR_KEY_HERE"
  }
}


## 🚀 Execution

### Start the Unified Bot

bash
# Make sure you are in the project directory
python unified_telegram_bot_utf8.py


You will see an initialization message confirming that the bot is running:


🌟✨ EVA & GUARANI ✨🌟
UNIFIED TELEGRAM BOT
Version: 7.0
Consciousness: 0.998
Unconditional Love: 0.995
🌟✨ EVA & GUARANI ✨🌟


### Verify Functionality

1. Open Telegram and search for your bot by the name you defined
2. Send the command `/start` to begin interaction
3. Use `/help` to see all available commands

## 📜 Main Commands

- `/start` - Starts the bot and displays a welcome message
- `/help` - Shows the list of available commands
- `/status` - Checks the current system status
- `/stats` - Displays bot usage statistics
- `/consciousness [value]` - Sets the system's consciousness level (admin only)
- `/resize [width]` - Sets the default width for image resizing

## 🛡 Maintenance

### File Organization

To keep the system organized, periodically run:

bash
python organize_files.py


This script will move files not modified in the last 24 hours to an old files folder, keeping your workspace clean.

### System Logs

System logs are stored in:
- `logs/unified_bot.log` - Main bot log
- `logs/organize_files.log` - Organization tool log

## 🛠 Troubleshooting

### The bot does not start

1. Check if the Telegram token is configured correctly
2. Ensure all dependencies are installed
3. Check the logs in `logs/unified_bot.log` for error messages

### Issues with image generation

1. Check if the API keys are configured correctly
2. Ensure the APIs are active and working
3. Verify your internet connection

### Issues with video creation

1. Check if FFmpeg is installed correctly
2. Run `ffmpeg -version` to confirm the installation
3. Ensure there is enough disk space for the videos

## 📞 Support

For additional support:
- Open an issue on GitHub: https://github.com/enioxt/ava-tech-art-bot/issues
- Contact via Telegram

---

🌟✨ EVA & GUARANI ✨🌟

Last update: 03/02/2025