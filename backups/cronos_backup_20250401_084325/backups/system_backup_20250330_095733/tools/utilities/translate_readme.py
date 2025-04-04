#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Translate README - Script to translate README.md from Portuguese to English
This script translates the main README file to standardize documentation.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import shutil
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Backup original README
readme_path = ROOT_DIR / "README.md"
backup_path = ROOT_DIR / "README.md.backup"

# Create backup
shutil.copy2(readme_path, backup_path)
print(f"Created backup at {backup_path}")

# English content for the README
english_content = """# EVA & GUARANI

Modular Analysis System, Systemic Cartography, and Quantum Ethics

*Version 8.0.0 - 03/20/2025*

## 🌟 Overview

EVA & GUARANI is an integrated system that transcends dimensions of thought with methodological precision and unconditional love, integrating advanced tools for knowledge visualization and evolutionary preservation.

## 📊 Project Status

- **Version**: 8.0.0
- **State**: Active Development
- **Last Update**: 03/20/2025

## 🏗️ System Structure

### Main Components

#### [`/core`](/core) - Essential Components

- **atlas**
- **atlas_pre_merge_20250320_082617**
- **config**
  - core
  - fluentd
  - grafana
  - integration
  - modules
  - postgres
  - prometheus
  - redis
- **cronos**
- **cronos_pre_merge_20250320_082617**
- **os**
  - config
  - core
  - data
  - docs
  - examples
  - practical_guides
  - logs
  - modules
  - quantum_prompts
  - scripts
  - services
- **ethik**
  - ethik_legacy
  - legacy
  - modules
- **nexus**
- **nexus_pre_merge_20250320_082617**
- **src**
  - accessibility
  - api
  - art
  - ava_mind
  - backup
  - backups
  - bot
  - config
  - consciousness
  - core
  - data
  - database
  - ethics
  - ethik
  - finance
  - infinity_ai
  - infinity_ai.egg-info
  - infinity_os
  - integrations
  - models
  - services
  - utils

#### [`/modules`](/modules) - Functional Modules

- **analysis**
- **blockchain**
- **config**
- **customization**
- **eliza**
  - characters
  - config
  - data
  - dist
  - eliza
  - legacy
  - logs
  - merged_from_eliza
  - node_modules
  - os
- **integration**
  - models
- **monitoring**
- **nexus**
  - connections
- **plugins**
  - extensions
- **preservation**
- **quantum**
  - intelligence
  - prompts
- **visualization**

#### [`/integrations`](/integrations) - Integrations

- **apis**
  - modules
- **bots**
  - QUANTUM_PROMPTS
  - config
  - data
  - generated_images
  - generated_videos
  - logs
  - modules
  - patches
  - venv
- **platforms**
- **services**

#### [`/tools`](/tools) - Tools

- **deployment**
- **maintenance**
- **scripts**
- **utilities**

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Dependencies listed in `requirements.txt`

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/eva-guarani.git

# Enter the directory
cd eva-guarani

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (if applicable)
npm install
```

## 📖 Documentation

Detailed documentation is available in the [`/docs`](/docs) directory and includes:

- User guides
- Developer documentation
- API references
- Tutorials

## 🛠️ Development

### Development Principles

1. **Universal possibility of redemption** - Every being and every code deserves infinite chances
2. **Compassionate temporality** - Evolution occurs in the necessary time
3. **Sacred privacy** - Absolute protection of data
4. **Universal accessibility** - Total inclusion
5. **Unconditional love** - Quantum foundation of all interactions
6. **Reciprocal trust** - Symbiotic relationship between system and user
7. **Integrated ethics** - Ethics as the fundamental DNA
8. **Conscious modularity** - Understanding of parts and whole
9. **Systemic cartography** - Precise mapping of connections
10. **Evolutionary preservation** - Quantum backup that maintains essence

## 📄 License

This project is licensed under the terms of the MIT license. See the `LICENSE` file for details.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""

# Write the English content to README.md
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(english_content)

print(f"Successfully translated README.md to English")
