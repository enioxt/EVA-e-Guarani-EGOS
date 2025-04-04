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
# Payment System for EVA & GUARANI Telegram Bot

This document describes the payment system implemented for the EVA & GUARANI Telegram bot (@avatechartbot), which allows receiving donations via PIX and cryptocurrencies.

## Overview

The payment system was designed to:

1. Allow users to make voluntary donations to support the development and maintenance of the bot

2. Offer multiple payment options (PIX and cryptocurrencies)

3. Implement a tier system that offers additional benefits for donors

4. Manage usage limits to control API costs

## System Structure

The payment system consists of the following components:

- **payment_gateway.py**: Main module that manages payments, user tiers, and limits

- **config/payment_config.json**: Configuration file with payment details and limits

- **data/payments/payments.json**: Database of payments and user information

## Bot Commands

Two new commands have been added to the bot:

- **/donate**: Displays information on how to make a donation, including PIX details and cryptocurrency addresses

- **/donation**: Allows the user to register a donation made (format: `/donation <amount> <method>`)

## User Tiers

The system implements three user tiers:

1. **Free Tier**:

   - Limit of 20 messages per day

   - Limit of 10 API calls per day

2. **Donor Tier**:

   - Requires a minimum donation of R$ 5.00

   - Limit of 100 messages per day

   - Limit of 50 API calls per day

3. **Premium Tier**:

   - Requires a minimum donation of R$ 20.00

   - Limit of 500 messages per day

   - Limit of 250 API calls per day

## Payment Methods

### PIX

- **Key**: 10689169663

- **Name**: Enio Batista Fernandes Rocha

### Cryptocurrencies

- **Bitcoin (Segwit)**: bc1qy9vr32f2hsjyapt3jz7fen6g0lxrehrqahwj3m

- **Solana**: 2iWboZwTkJ5ofCB2wXApa5ReeyJwUFRXrBgHyFRSy6a1

- **Ethereum (BASE chain)**: 0xa858F22c8C1f3D5059D101C0c7666Ed0C2BF53ac

## Payment Flow

1. The user requests donation information using the `/donate` command

2. The bot displays payment options and benefits

3. The user makes the donation through the chosen method

4. The user registers the donation using the `/donation <amount> <method>` command

5. The system updates the user's tier based on the donated amount

6. Administrators are notified about the new donation

## Technical Implementation

### Payment Registration

Payments are recorded in the `data/payments/payments.json` file with the following structure:

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
  "transactions": [
    {
      "id": "abcdef1234567890",
      "user_id": 123456789,
      "amount": 5.0,
      "currency": "BRL",
      "payment_method": "pix",
      "timestamp": "2024-03-01T10:15:30.123456",
      "status": "completed"
    },
    {
      "id": "ghijkl9876543210",
      "user_id": 123456789,
      "amount": 20.0,
      "currency": "BRL",
      "payment_method": "pix",
      "timestamp": "2024-03-03T15:30:45.123456",
      "status": "completed"
    }
  ]
}


### Limit Verification

The system checks usage limits before processing each user's message. If the user has reached their daily limit, the bot sends a message informing them about the limit and suggesting a donation to increase the limits.

## Future Considerations

For a more robust production implementation, consider:

1. Implementing automatic payment verification via cryptocurrency APIs

2. Adding integration with payment gateways like Stripe or PayPal

3. Implementing a recurring subscription system

4. Adding an administrative panel to manage payments and users

5. Implementing a refund system for specific cases

## Important Notes

- This system is based on voluntary donations, not mandatory payments

- Users are clearly informed about the voluntary nature of the donations

- The system keeps the bot accessible to everyone, even without donations

- Donations help cover API costs and maintain bot development

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
