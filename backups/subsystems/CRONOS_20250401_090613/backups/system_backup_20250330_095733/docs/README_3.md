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

# Eliza



## Edit the character files



Open `src/character.ts` to modify the default character. Uncomment and edit.



### Custom characters



To load custom characters instead:

- Use `pnpm start --characters="path/to/your/character.json"`

- Multiple character files can be loaded simultaneously



### Add clients

```

# in character.ts

clients: [Clients.TWITTER, Clients.DISCORD],



# in character.json

clients: ["twitter", "discord"]

```



## Duplicate the .env.example template



```bash

cp .env.example .env

```



\* Fill out the .env file with your own values.



### Add login credentials and keys to .env

```

DISCORD_APPLICATION_ID="discord-application-id"

DISCORD_API_TOKEN="discord-api-token"

...

OPENROUTER_API_KEY="sk-xx-xx-xxx"

...

TWITTER_USERNAME="username"

TWITTER_PASSWORD="password"

TWITTER_EMAIL="your@email.com"

```



## Install dependencies and start your agent



```bash

pnpm i && pnpm start

```

Note: this requires node to be at least version 22 when you install packages and run the agent.



## Run with Docker



### Build and run Docker Compose (For x86_64 architecture)



#### Edit the docker-compose.yaml file with your environment variables



```yaml

services:

    eliza:

        environment:

            - OPENROUTER_API_KEY=blahdeeblahblahblah

```



#### Run the image



```bash

docker compose up

```



### Build the image with Mac M-Series or aarch64



Make sure docker is running.



```bash

# The --load flag ensures the built image is available locally

docker buildx build --platform linux/amd64 -t eliza-starter:v1 --load .

```



#### Edit the docker-compose-image.yaml file with your environment variables



```yaml

services:

    eliza:

        environment:

            - OPENROUTER_API_KEY=blahdeeblahblahblah

```



#### Run the image



```bash

docker compose -f docker-compose-image.yaml up

```



# Deploy with Railway



[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/aW47_j)
