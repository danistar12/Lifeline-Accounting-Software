#!/bin/bash

# Deployment script for Lifeline Accounting FedRAMP Security Setup
# Run this on the production server after deploying code

echo "🔒 Setting up FedRAMP Security Infrastructure..."

# Navigate to the project directory
cd /var/www/lifeline-accounting/backend

# Activate virtual environment
source venv/bin/activate

echo "📁 Creating logs directory..."
# Create logs directory with proper permissions
python manage.py setup_logging

echo "🔍 Running security verification..."
# Verify security configuration
python manage.py verify_security

echo "✅ Running Django system check..."
# Run Django system check
python manage.py check

echo "📊 Testing database connectivity..."
# Test database connection
python manage.py migrate --check

echo ""
echo "🎯 Deployment verification complete!"
echo ""
echo "Next steps:"
echo "1. Restart Apache/WSGI server"
echo "2. Test login functionality"
echo "3. Verify session timeout behavior"
echo "4. Check log files are being created in /var/www/lifeline-accounting/backend/logs/"