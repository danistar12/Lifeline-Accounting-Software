#!/bin/bash

# Lifeline Accounting - Manual Deployment Script
# Run this script on your server after logging in to deploy the latest changes
# Usage: ./deploy.sh

set -e

DEPLOY_PATH="/var/www/lifeline-accounting"
LOG_FILE="/tmp/lifeline-deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages with colors
log_message() {
    local color=$1
    local message=$2
    echo -e "${color}$(date '+%Y-%m-%d %H:%M:%S') - $message${NC}" | tee -a "$LOG_FILE"
}

echo -e "${BLUE}
╔════════════════════════════════════════╗
║        Lifeline Accounting Deploy      ║
║            Manual Deployment           ║
╚════════════════════════════════════════╝${NC}"

log_message "$BLUE" "🚀 Starting deployment..."

# Check if we're in the right directory
if [[ $(pwd) != "$DEPLOY_PATH" ]]; then
    log_message "$BLUE" "📁 Navigating to project directory: $DEPLOY_PATH"
    cd "$DEPLOY_PATH" || { log_message "$RED" "❌ Failed to navigate to $DEPLOY_PATH"; exit 1; }
else
    log_message "$GREEN" "📁 Already in project directory: $DEPLOY_PATH"
fi

# Show current git status
log_message "$BLUE" "📊 Current git status:"
if git status --porcelain | grep -q .; then
    log_message "$YELLOW" "⚠️  Uncommitted changes detected:"
    git status --short
    echo ""
    read -p "Continue with deployment? This will reset any local changes. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_message "$YELLOW" "🛑 Deployment cancelled by user"
        exit 0
    fi
    log_message "$YELLOW" "🔄 Resetting local changes..."
    git reset --hard HEAD
else
    log_message "$GREEN" "✅ Working directory clean"
fi

# Pull latest changes
log_message "$BLUE" "📥 Pulling latest changes from GitHub..."
git fetch origin
BEFORE_COMMIT=$(git rev-parse HEAD)
git pull origin master || { log_message "$RED" "❌ Git pull failed"; exit 1; }
AFTER_COMMIT=$(git rev-parse HEAD)

if [[ "$BEFORE_COMMIT" == "$AFTER_COMMIT" ]]; then
    log_message "$GREEN" "✅ Already up to date - no new changes"
    echo ""
    read -p "Continue with deployment anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_message "$BLUE" "🛑 Deployment skipped - no changes"
        exit 0
    fi
else
    log_message "$GREEN" "✅ New changes pulled successfully"
    log_message "$BLUE" "📝 Changes: $BEFORE_COMMIT -> $AFTER_COMMIT"
fi

# Backend setup
log_message "$BLUE" "🐍 Setting up backend..."
cd backend || { log_message "$RED" "❌ Backend directory not found"; exit 1; }

# Check if virtual environment exists
if [[ ! -d "venv" ]]; then
    log_message "$RED" "❌ Virtual environment not found. Please create it first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
log_message "$BLUE" "🔧 Activating virtual environment..."
source venv/bin/activate || { log_message "$RED" "❌ Failed to activate venv"; exit 1; }

# Show Python info
log_message "$GREEN" "✅ Virtual environment activated"
log_message "$BLUE" "🐍 Python: $(python --version)"
log_message "$BLUE" "📍 Python path: $(which python)"

# Set Django settings
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production

# Check Django configuration
log_message "$BLUE" "✅ Running Django checks..."
python manage.py check || { log_message "$RED" "❌ Django check failed"; exit 1; }
log_message "$GREEN" "✅ Django checks passed"

# Frontend build and deploy
log_message "$BLUE" "🌐 Building and deploying frontend..."
cd ../frontend || { log_message "$RED" "❌ Frontend directory not found"; exit 1; }

# Check if package.json exists
if [[ ! -f "package.json" ]]; then
    log_message "$RED" "❌ package.json not found in frontend directory"
    exit 1
fi

# Install dependencies
log_message "$BLUE" "📦 Installing npm dependencies..."
if npm ci > /dev/null 2>&1; then
    log_message "$GREEN" "✅ npm ci completed successfully"
elif npm install > /dev/null 2>&1; then
    log_message "$YELLOW" "⚠️ npm ci failed, used npm install instead"
else
    log_message "$RED" "❌ npm install failed"
    exit 1
fi

# Build frontend
log_message "$BLUE" "🔨 Building frontend..."
npm run build || { log_message "$RED" "❌ Frontend build failed"; exit 1; }
log_message "$GREEN" "✅ Frontend build completed"

# Check if dist directory was created
if [[ ! -d "dist" ]]; then
    log_message "$RED" "❌ Build output directory 'dist' not found"
    exit 1
fi

# Deploy frontend
log_message "$BLUE" "🚀 Deploying frontend files..."
sudo rsync -av --delete dist/ /var/www/html/ || { log_message "$RED" "❌ Frontend deployment failed"; exit 1; }
log_message "$GREEN" "✅ Frontend files deployed successfully"

# Set proper permissions
log_message "$BLUE" "🔐 Setting file permissions..."
sudo chown -R www-data:www-data /var/www/html/ || { log_message "$YELLOW" "⚠️ Permission setting failed but continuing"; }
log_message "$GREEN" "✅ File permissions set"

# Restart Apache
log_message "$BLUE" "🔄 Restarting Apache..."
sudo systemctl restart apache2 || { log_message "$RED" "❌ Apache restart failed"; exit 1; }
log_message "$GREEN" "✅ Apache restarted successfully"

# Verify Apache is running
log_message "$BLUE" "🔍 Verifying Apache status..."
if systemctl is-active apache2 > /dev/null; then
    log_message "$GREEN" "✅ Apache is running properly"
else
    log_message "$RED" "❌ Apache is not running after restart"
    exit 1
fi

# Final success message
echo ""
log_message "$GREEN" "╔════════════════════════════════════════╗"
log_message "$GREEN" "║     🎉 DEPLOYMENT SUCCESSFUL! 🎉      ║"
log_message "$GREEN" "╚════════════════════════════════════════╝"
echo ""
log_message "$BLUE" "🌐 Your site has been updated and is ready!"
log_message "$BLUE" "📄 Deployment log saved to: $LOG_FILE"
echo ""

# Show deployment summary
echo -e "${BLUE}Deployment Summary:${NC}"
echo -e "  ${GREEN}✅${NC} Git pull completed"
echo -e "  ${GREEN}✅${NC} Django checks passed" 
echo -e "  ${GREEN}✅${NC} Frontend built successfully"
echo -e "  ${GREEN}✅${NC} Files deployed to web server"
echo -e "  ${GREEN}✅${NC} Apache restarted and verified"
echo ""