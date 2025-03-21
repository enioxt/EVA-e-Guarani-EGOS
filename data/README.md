# EVA & GUARANI - Data Directory

This directory stores data files used by various components of the EVA & GUARANI ecosystem.

## Structure

```
data/
├── models/         # Pre-trained models and model weights
├── config/         # Configuration files and presets
├── cache/          # Cached data for improved performance
├── terminology/    # Technical terminology and specialized vocabularies
└── examples/       # Example datasets for testing and demonstration
```

## Note for Contributors

The data directory is included in `.gitignore` to prevent large files from being pushed to the repository. However, the directory structure is maintained with `.gitkeep` files.

## Getting Started

When installing the system, some modules may require downloading additional data files. These will be downloaded automatically or instructions will be provided for manual installation.

### Translator Module Data

The translator module requires model files that are not included in the repository due to their size. When using the translator for the first time, it will automatically download the required model files from HuggingFace.

## Data Privacy

All data in this directory should be treated according to the ethical principles of EVA & GUARANI, with respect for privacy and confidentiality.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
