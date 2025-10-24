#!/bin/bash

# Quick fix for logging directory issue
# Run this on the server to immediately resolve the FileNotFoundError

echo "🔧 Quick fix: Creating logs directory..."

# Navigate to backend directory
cd /var/www/lifeline-accounting/backend

# Create logs directory
mkdir -p logs

# Create empty log files with proper permissions
touch logs/lifeline.log
touch logs/security.log  
touch logs/audit.log

# Set proper permissions
chmod 755 logs
chmod 640 logs/*.log

echo "✅ Logs directory and files created!"
echo "Directory: /var/www/lifeline-accounting/backend/logs"
echo "Files: lifeline.log, security.log, audit.log"
echo ""
echo "Now try running: python manage.py check"