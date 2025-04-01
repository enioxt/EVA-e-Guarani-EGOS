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
# 📊 EVA & GUARANI FREEMIUM System

This document explains the functionality of the FREEMIUM system implemented in the EVA & GUARANI bot, detailing the different plans, usage limits, credit system, and how users can manage their resources.

## 🌟 Overview

The EVA & GUARANI FREEMIUM system is designed to provide free access to the bot's basic features while maintaining a sustainable model through payments and top-ups for advanced resources. The system includes:

- **Different plans** with specific usage limits

- **Credit system** for special and internet calls

- **Top-up mechanism** to add more credits

- **Dedicated commands** to manage and check credits

- **Options to earn extra credits** through referrals and feedback (coming soon)

## 📋 Available Plans

The bot offers three different plans:

### 1️⃣ Free Plan (Free Tier)

- **Regular messages**: 20 per day

- **Special calls**: 5 per day

- **Internet calls**: 5 per day

- **Top-ups**: Available from R$ 5.00

### 2️⃣ Supporter Plan (Supporter Tier)

- **Regular messages**: 100 per day (5x more than the free plan)

- **Special calls**: 25 per day (5x more than the free plan)

- **Internet calls**: 25 per day (5x more than the free plan)

- **Requirement**: Minimum payment of R$ 5.00

### 3️⃣ Premium Plan (Premium Tier)

- **Regular messages**: 500 per day (25x more than the free plan)

- **Special calls**: 100 per day (25x more than the free plan)

- **Internet calls**: 100 per day (25x more than the free plan)

- **Requirement**: Minimum payment of R$ 20.00

## 💳 Credit System

In addition to daily limits, the bot uses a credit system to manage the use of advanced resources:

- **Special calls**: Consume 1 credit per use

- **Internet calls**: Consume 1 credit per use

- **Standard top-up**: Adds 10 credits for R$ 5.00

- **Top-ups in higher plans**: Add credits proportional to the amount paid

Credits are persistent and do not expire, allowing users to accumulate credits for future use.

## 🌍 Multilingual Support

EVA & GUARANI offers support for multiple languages:

- Upon starting, you can choose your preferred language

- Change language at any time with the `/language` command

- Practicing in a language different from your native one is encouraged as a learning tool

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

### Benefits of Language Learning

- Practice a new language daily

- Get grammatical corrections and vocabulary tips

- Develop conversational skills in real contexts

- Enhance your understanding of cultural nuances

## 🔍 Types of Calls

### Regular Messages

Normal conversations with the bot that do not involve special processing or internet access.

### Special Calls

Requests that require advanced processing, such as:

- Image generation (DALL-E)

- Code creation

- Detailed analyses

- Complete summaries

- Document translations

### Internet Calls

Requests that require internet access to obtain updated information, such as:

- Web searches

- Recent news

- Updated information

- Weather forecasts

- Current quotes and values

## 🤖 Commands to Manage Credits

The bot offers specific commands to manage and check credits:

- **/credits** - Displays detailed information about your available credits and daily limits

- **/upgrade** - Shows plan options and credit top-up

- **/payment <amount> <method>** - Registers a payment and adds corresponding credits

- **/language** - Changes the interaction language with the bot

## 💡 Tips to Save Credits

To maximize the use of available credits, we recommend:

1. **Be specific in your questions** to get direct answers

2. **Avoid requesting multiple tasks** in a single message

3. **Use special and internet calls** only when necessary

4. **Check your credits regularly** with the /credits command

5. **Group related questions** in a single message when possible

## 📱 How to Top-Up Credits

To top-up your credits:

1. Use the **/upgrade** command to see available payment options

2. Make the payment using PIX or cryptocurrencies

3. Register your payment using the **/payment <amount> <method>** command

4. Credits will be automatically added to your account

5. Check your updated credits with the **/credits** command

## 🎁 Earn Extra Credits

Soon, you will be able to earn extra credits through:

### Referral Program

- Invite friends to use EVA & GUARANI

- Earn credits when your referrals register

- Receive additional bonuses when your referrals upgrade

### Feedback Program

- Send improvement suggestions for the bot

- Report bugs or issues

- Participate in surveys and evaluations

- The more valuable your feedback, the more credits you receive

### Missions and Challenges

- Complete weekly challenges

- Participate in seasonal events

- Test new features before official release

- Each completed mission rewards you with credits

### Community Engagement

- Contribute to the EVA & GUARANI community

- Participate in forums and discussions

- Create content related to the bot

- Help other users make the most of the bot

## 🔄 Daily Limit Renewal

Daily limits for messages, special calls, and internet calls are automatically renewed every 24 hours. Unused credits remain in your account for future use.

## 📊 Usage Monitoring

The bot automatically monitors resource usage and notifies users when:

- They reach the daily message limit

- They do not have enough credits for special calls

- They do not have enough credits for internet calls

## 🛠️ Technical Configuration

The FREEMIUM system is configured through the `config/payment_config.json` file, which defines:

- Usage limits for each plan

- Prices for top-ups and credits

- Welcome messages

- Payment settings

## 📞 Support

If you have questions about the FREEMIUM system or encounter issues with your credits, contact the bot administrator for assistance.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧