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
# 🌟 Image Generation with DALL-E - EVA & GUARANI

This document explains how to use the image generation feature with DALL-E integrated into the EVA & GUARANI bot.

## 📖 Overview

The integration with OpenAI's DALL-E API allows the EVA & GUARANI bot to generate high-quality images from textual descriptions. This feature:

- Supports DALL-E 2 and DALL-E 3 models
- Allows customization of size, quality, and style
- Saves generated images both locally and provides URLs
- Integrates with the FREEMIUM system, consuming special call credits

## 🛠️ How to Use

### Basic Command


/image [image description]


**Example:**


/image A cat astronaut floating in space, digital art style


### Advanced Options

You can customize image generation with the following parameters:


/image [image description] --model [model] --size [size] --quality [quality] --style [style]


**Available Parameters:**

| Parameter | Options | Default | Notes |
|-----------|--------|--------|-------------|
| `--model` | `dall-e-2`, `dall-e-3` | `dall-e-3` | DALL-E 3 produces higher quality images |
| `--size` | For DALL-E 3: `1024x1024`, `1792x1024`, `1024x1792`<br>For DALL-E 2: `256x256`, `512x512`, `1024x1024` | `1024x1024` | Different sizes have different costs |
| `--quality` | `standard`, `hd` | `standard` | HD has a higher cost and only works with DALL-E 3 |
| `--style` | `vivid`, `natural` | `vivid` | Only works with DALL-E 3 |

**Examples:**


/image Futuristic landscape with floating cities --model dall-e-3 --size 1792x1024 --quality hd --style natural



/image Portrait of a robot in Renaissance style --style natural


## 💰 Credit Cost

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

Make sure you have enough credits before requesting image generation. Use the `/credits` command to check your current balance and `/upgrade` to recharge credits.

## 💡 Tips for Good Results

### Writing Effective Prompts

1. **Be specific and detailed**: The more details you provide, the better the result will be.


   ❌ "A cat"
   ✅ "An orange Persian cat sitting on a window looking out, sunset light, photographic style"


2. **Specify the artistic style**: Mention the desired style for better results.


   "Mountain landscape in Van Gogh style"
   "Portrait of a woman in cyberpunk style"
   "Urban scene in watercolor"


3. **Describe the lighting**: Lighting drastically affects the result.


   "Dense forest with light filtering through the trees"
   "Portrait with studio lighting"
   "Night scene illuminated by neon"


4. **Mention perspective/angle**: Defines how the image will be composed.


   "Futuristic city seen from above"
   "Close-up of a flower with dew drops"
   "Panoramic view of a beach at sunset"


### Popular Styles to Experiment With

- Photorealism
- Oil painting
- Watercolor
- Pixel art
- Digital art
- Cyberpunk
- Vaporwave
- Impressionism
- Surrealism
- Minimalism

## ⚙️ Technical Configuration

The DALL-E functionality is configured in the `config/api_config.json` file, where you can define:

- OpenAI API key
- Default model
- Default image size
- Default quality and style
- Request rate limits
- Directory to save images

Administrators need to configure a valid OpenAI API key for the functionality to work.

## ❓ Frequently Asked Questions

**Q: Can I edit the generated images?**
A: Yes, the generated images are your property and can be freely edited.

**Q: Can I generate images of adult or violent content?**
A: No. The DALL-E API has content filters that reject violent, adult, or politically sensitive prompts.

**Q: Why wasn't my image generated?**
A: It could be due to:

1. Lack of sufficient credits
2. Connection issues with the OpenAI API
3. Your prompt contains prohibited content
4. Request limit exceeded

**Q: Are the images saved in the bot?**
A: Yes, the images are saved both locally on the server and provided as URLs.

**Q: What is the difference between 'vivid' and 'natural' styles?**
A: 'Vivid' produces more colorful and dramatic images, while 'natural' creates more subtle and realistic images.

---

🌟✨ EVA & GUARANI ✨🌟
