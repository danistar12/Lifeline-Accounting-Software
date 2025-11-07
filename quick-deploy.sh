#!/bin/bash

# Quick Deploy Script for Lifeline Accounting
# A simplified version that just does the essential steps

echo "🚀 Quick Deploy - Lifeline Accounting"
echo "======================================"

# Navigate to project directory if not already there  
cd /var/www/lifeline-accounting || { echo "❌ Failed to navigate to project"; exit 1; }

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin master || { echo "❌ Git pull failed"; exit 1; }

# Backend checks
echo "🐍 Checking backend..."
cd backend
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production
python manage.py check || { echo "❌ Django check failed"; exit 1; }

# Build and deploy frontend
echo "🌐 Building frontend..."
cd ../frontend  
npm run build || { echo "❌ Build failed"; exit 1; }

echo "🚀 Deploying..."
sudo rsync -av --delete dist/ /var/www/html/

echo "🔄 Restarting Apache..."
sudo systemctl restart apache2

echo "✅ Quick deploy completed!"
echo "🌐 Your site is updated and ready!"