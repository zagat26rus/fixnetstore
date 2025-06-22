#!/bin/bash

# FixNet GitHub Deployment Script
# This script prepares the project for GitHub upload

echo "🚀 Preparing FixNet for GitHub deployment..."

# Create .gitignore if it doesn't exist
cat > .gitignore << EOF
# Dependencies
node_modules/
*/node_modules/

# Production builds
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Editor directories and files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite

# Logs
*.log

# IDE
.vscode/
.idea/

# System files
.DS_Store
Thumbs.db
EOF

# Create GitHub workflow for CI/CD
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml << EOF
name: Deploy FixNet

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mongodb:
        image: mongo:latest
        ports:
          - 27017:27017
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'yarn'
        cache-dependency-path: frontend/yarn.lock
    
    - name: Setup Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        yarn install
    
    - name: Install backend dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run frontend tests
      run: |
        cd frontend
        yarn test --watchAll=false
    
    - name: Run backend tests
      run: |
        cd backend
        pytest
      env:
        MONGO_URL: mongodb://localhost:27017
        DB_NAME: fixnet_test
    
    - name: Build frontend
      run: |
        cd frontend
        yarn build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    # Add your deployment steps here
    # Example: Deploy to Vercel, Netlify, or your hosting provider
EOF

# Create environment example files
cat > backend/.env.example << EOF
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=fixnet

# JWT Configuration
JWT_SECRET_KEY=change-this-to-a-secure-secret-key

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Server Configuration
HOST=0.0.0.0
PORT=8001
EOF

cat > frontend/.env.example << EOF
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001

# Application Configuration
REACT_APP_NAME=FixNet
REACT_APP_VERSION=1.0.0
EOF

# Create Docker configuration
cat > Dockerfile << EOF
# Multi-stage Docker build for FixNet

# Frontend build stage
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY frontend/ ./
RUN yarn build

# Backend stage
FROM python:3.9-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Expose port
EXPOSE 8001

# Run the application
CMD ["python", "-m", "uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8001"]
EOF

cat > docker-compose.yml << EOF
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: fixnet_mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: fixnet

  backend:
    build: .
    container_name: fixnet_backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      MONGO_URL: mongodb://mongodb:27017
      DB_NAME: fixnet
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app/backend

  frontend:
    build:
      context: .
      target: frontend-build
    container_name: fixnet_frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      REACT_APP_BACKEND_URL: http://localhost:8001

volumes:
  mongodb_data:
EOF

echo "✅ GitHub deployment files created!"
echo ""
echo "📋 Next steps:"
echo "1. Initialize git repository: git init"
echo "2. Add all files: git add ."
echo "3. Commit: git commit -m 'Initial commit: FixNet smartphone repair platform'"
echo "4. Create GitHub repository"
echo "5. Add remote: git remote add origin https://github.com/yourusername/fixnet.git"
echo "6. Push: git push -u origin main"
echo ""
echo "🔧 Don't forget to:"
echo "- Update .env files with your actual credentials"
echo "- Configure GitHub secrets for deployment"
echo "- Set up your hosting provider (Vercel, Netlify, etc.)"
echo ""
echo "🚀 Your FixNet project is ready for GitHub!"