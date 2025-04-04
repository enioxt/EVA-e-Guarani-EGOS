#!/usr/bin/env sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${YELLOW}🔧 Initializing Git hooks...${NC}"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "${YELLOW}📦 Installing dependencies...${NC}"
  npm install || {
    echo "${RED}❌ Failed to install dependencies${NC}"
    exit 1
  }
fi

# Install Husky
echo "${YELLOW}🐕 Installing Husky...${NC}"
npm run prepare || {
  echo "${RED}❌ Failed to install Husky${NC}"
  exit 1
}

# Make hook files executable
echo "${YELLOW}🔑 Making hook files executable...${NC}"
chmod +x .husky/commit-msg \
        .husky/post-checkout \
        .husky/post-merge \
        .husky/pre-commit \
        .husky/pre-push \
        .husky/prepare-commit-msg || {
  echo "${RED}❌ Failed to make hook files executable${NC}"
  exit 1
}

# Verify hooks installation
echo "${YELLOW}✨ Verifying hooks installation...${NC}"
if [ -d ".husky" ] && [ -f ".husky/commit-msg" ] && [ -f ".husky/pre-commit" ]; then
  echo "${GREEN}✅ Git hooks initialized successfully!${NC}"
  echo ""
  echo "${YELLOW}The following hooks are installed:${NC}"
  echo "- commit-msg: Enforces conventional commit message format"
  echo "- post-checkout: Runs after switching branches"
  echo "- post-merge: Runs after merging branches"
  echo "- pre-commit: Runs before committing"
  echo "- pre-push: Runs before pushing"
  echo "- prepare-commit-msg: Prepares commit message template"
else
  echo "${RED}❌ Git hooks initialization failed${NC}"
  exit 1
fi
