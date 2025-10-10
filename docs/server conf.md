# Lifeline Accounting Software - Linux Server Deployment Guide

## Server Information
- **Web Server**: 02-vuweb01 (10.100.5.61)
- **Database Server**: 10.100.5.27 (MSSQL)
- **Operating System**: Linux (Ubuntu recommended)
- **User Account**: ds3297l

## Deployment Workflow (Windows to Linux)

### Recommended SSH Tools
- **Windows SSH** (built-in): Use PowerShell or Command Prompt
- **VS Code SSH Extension**: Best for development and deployment
- **PuTTY**: Alternative GUI option

### SSH Connection
```bash
ssh ds3297l@10.100.5.61
```

## 1. Initial Server Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Essential Packages
```bash
sudo apt install -y python3 python3-pip python3-venv nodejs npm git
sudo apt install -y apache2 libapache2-mod-wsgi-py3
sudo apt install -y curl unixodbc-dev
```

### Install Microsoft ODBC Driver for MSSQL
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt update
sudo apt install -y msodbcsql17 mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```

## 2. Application Deployment

### Clone Repository
```bash
cd /var/www
sudo git clone <repository_url> lifeline-accounting
sudo chown -R ds3297l:www-data lifeline-accounting
cd lifeline-accounting
```

### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyodbc  # For MSSQL connection
```

### Database Configuration

**Connecting to Existing MSSQL Database**

The deployment connects to your existing MSSQL database server at `10.100.5.27` with the `LifelineAccounting` database that contains all your tables and data.

Create `lifeline_backend/settings_production.py`:
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['10.100.5.61', '02-vuweb01', 'lifelinedatacenters.com']

# Connect to existing MSSQL database with your schema
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'LLAcctTemp',
        'USER': 'LLAcct',
        'PASSWORD': 'SilverMoon#3',
        'HOST': '10.100.5.27',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;Encrypt=no',
        }
    }
}

# Important: Do NOT run migrations on production database
# Your existing database schema will be used as-is

STATIC_ROOT = '/var/www/lifeline-accounting/static/'
MEDIA_ROOT = '/var/www/lifeline-accounting/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Run Django Setup (Production Database)

**Important**: Since you're connecting to an existing database with data, **DO NOT** run migrations:

```bash
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production

# Only collect static files - do NOT migrate
python manage.py collectstatic --noinput

# Test database connection without modifying schema
python manage.py check --database default
```

**Note**: Your existing MSSQL database schema and data will remain unchanged. The Django models should match your existing table structure.

### Frontend Setup
```bash
cd ../frontend
npm install
npm run build

# Copy built files to Apache directory
sudo cp -r dist/* /var/www/html/
```

## 3. Apache Configuration

### Enable Required Modules
```bash
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod wsgi
```

### Create Virtual Host
Create `/etc/apache2/sites-available/lifeline-accounting.conf`:
```apache
<VirtualHost *:80>
    ServerName 10.100.5.61
    DocumentRoot /var/www/html
    
    # Redirect all HTTP to HTTPS
    Redirect permanent / https://10.100.5.61/
</VirtualHost>

<VirtualHost *:443>
    ServerName 10.100.5.61
    DocumentRoot /var/www/html
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem
    SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
    
    # Django Backend API
    WSGIDaemonProcess lifeline python-path=/var/www/lifeline-accounting/backend python-home=/var/www/lifeline-accounting/backend/venv
    WSGIProcessGroup lifeline
    WSGIScriptAlias /api /var/www/lifeline-accounting/backend/lifeline_backend/wsgi.py
    
    <Directory /var/www/lifeline-accounting/backend/lifeline_backend>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
    # Static and Media Files
    Alias /static /var/www/lifeline-accounting/static
    Alias /media /var/www/lifeline-accounting/media
    
    <Directory /var/www/lifeline-accounting/static>
        Require all granted
    </Directory>
    
    <Directory /var/www/lifeline-accounting/media>
        Require all granted
    </Directory>
    
    # Frontend (Vue.js)
    <Directory /var/www/html>
        Options -Indexes
        AllowOverride All
        Require all granted
        
        # Handle Vue.js routing
        FallbackResource /index.html
    </Directory>
    
    # Security Headers
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
```

### Enable Site and Restart Apache
```bash
sudo a2ensite lifeline-accounting.conf
sudo a2dissite 000-default.conf
sudo systemctl restart apache2
```

## 4. Permissions and Security

### Set Proper Ownership
```bash
sudo chown -R ds3297l:www-data /var/www/lifeline-accounting
sudo chmod -R 755 /var/www/lifeline-accounting
sudo chmod -R 775 /var/www/lifeline-accounting/media
```

### Firewall Configuration
```bash
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

## 5. Monitoring and Maintenance

### Create Backup Script
Create `/home/ds3297l/backup-lifeline.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/home/ds3297l/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/lifeline_app_$DATE.tar.gz /var/www/lifeline-accounting

# Backup media files
tar -czf $BACKUP_DIR/lifeline_media_$DATE.tar.gz /var/www/lifeline-accounting/media

# Keep only last 7 days of backups
find $BACKUP_DIR -name "lifeline_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
chmod +x /home/ds3297l/backup-lifeline.sh
```

### Setup Log Rotation
Create `/etc/logrotate.d/lifeline-accounting`:
```
/var/log/apache2/lifeline_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root adm
    postrotate
        systemctl reload apache2
    endscript
}
```

### Create Deployment Update Script
Create `/home/ds3297l/update-lifeline.sh`:
```bash
#!/bin/bash
echo "Starting Lifeline Accounting deployment update..."

cd /var/www/lifeline-accounting

# Pull latest changes from repository
echo "Pulling latest changes..."
git pull origin main

# Update backend
echo "Updating backend..."
cd Accounting-Version-1/backend
source venv/bin/activate

# Install any new Python dependencies
pip install -r requirements.txt

# Set production environment
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production

# Collect static files
python manage.py collectstatic --noinput

# DO NOT run migrate - using existing database
# python manage.py migrate  # COMMENTED OUT for existing database

# Update frontend
echo "Updating frontend..."
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/html/

# Restart Apache to apply changes
echo "Restarting Apache..."
sudo systemctl restart apache2

echo "Deployment update completed successfully!"
echo "Application is now running with latest changes."
```

# Update frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/html/

# Restart Apache
sudo systemctl restart apache2

echo "Deployment updated successfully"
```

```bash
chmod +x /home/ds3297l/update-lifeline.sh
```

---

## Deployment Update Process

### **Manual Update (Recommended)**
1. **From Windows**: Push changes to GitHub
   ```powershell
   git add .
   git commit -m "Update description"
   git push origin main
   ```

2. **SSH to Linux server**:
   ```bash
   ssh ds3297l@10.100.5.61
   ```

3. **Run update script**:
   ```bash
   cd /home/ds3297l && ./update-lifeline.sh
   ```

### **Automated Deployment Options**

#### Option 1: GitHub Actions (Recommended for CI/CD)
Create `.github/workflows/deploy.yml` in your repository:
```yaml
name: Deploy to Linux Server

on:
  push:
    branches: [ main ]
  workflow_dispatch:  # Allow manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: 10.100.5.61
        username: ds3297l
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /home/ds3297l
          ./update-lifeline.sh
```

**Setup Steps for GitHub Actions**:
1. Generate SSH key pair on your Windows machine:
   ```powershell
   ssh-keygen -t rsa -b 4096 -f lifeline-deploy-key
   ```

2. Copy public key to Linux server:
   ```bash
   ssh-copy-id -i lifeline-deploy-key.pub ds3297l@10.100.5.61
   ```

3. Add private key to GitHub Secrets:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add new secret: `SSH_PRIVATE_KEY` (paste the private key content)

#### Option 2: Simple Webhook (Alternative)
Create a webhook endpoint on your server:

Create `/home/ds3297l/webhook-server.py`:
```python
#!/usr/bin/env python3
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import hmac

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/deploy':
            # Run deployment script
            result = subprocess.run(['/home/ds3297l/update-lifeline.sh'], 
                                  capture_output=True, text=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success' if result.returncode == 0 else 'error',
                'output': result.stdout,
                'error': result.stderr
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), WebhookHandler)
    print("Webhook server running on port 8080...")
    server.serve_forever()
```

Run webhook server:
```bash
python3 /home/ds3297l/webhook-server.py &
```

Then configure GitHub webhook to POST to `http://10.100.5.61:8080/deploy`

## 6. Testing and Verification

### Test Database Connection

Test the connection to your existing MSSQL database:
```bash
cd /var/www/lifeline-accounting/Accounting-Version-1/backend
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production
python manage.py shell
```

In the Django shell:
```python
from django.db import connection
cursor = connection.cursor()

# Test basic connection
cursor.execute("SELECT 1")
print("Database connection successful!")

# Verify your existing tables
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = cursor.fetchall()
print(f"Found {len(tables)} tables in LifelineAccounting database")

# Test a specific table from your schema
cursor.execute("SELECT COUNT(*) FROM Companies")
company_count = cursor.fetchone()[0]
print(f"Companies table has {company_count} records")
```

### Test Application
1. **Frontend**: Navigate to `https://10.100.5.61`
2. **API**: Test `https://10.100.5.61/api/admin/`
3. **Static Files**: Check `https://10.100.5.61/static/`

## 7. Troubleshooting

### Common Issues

**Apache Not Starting**:
```bash
sudo systemctl status apache2
sudo journalctl -u apache2
```

**WSGI Errors**:
```bash
sudo tail -f /var/log/apache2/error.log
```

**Database Connection Issues**:
```bash
# Test ODBC connection to your existing database
odbcinst -q -d
sqlcmd -S 10.100.5.27 -U your_username -P your_password -d LifelineAccounting

# Test specific connection from Django
cd /var/www/lifeline-accounting/Accounting-Version-1/backend
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production
python manage.py dbshell

# If connection fails, check:
# 1. Database server is accessible: telnet 10.100.5.27 1433
# 2. Credentials are correct
# 3. Database name exists: LifelineAccounting
# 4. User has permissions on the database
```

**Permission Errors**:
```bash
sudo chown -R ds3297l:www-data /var/www/lifeline-accounting
sudo chmod -R 755 /var/www/lifeline-accounting
```

### Log Locations
- Apache Errors: `/var/log/apache2/error.log`
- Apache Access: `/var/log/apache2/access.log`
- Django Logs: Configure in `settings_production.py`

## 8. SSL Certificate (Production)

For production, replace self-signed certificate with proper SSL:

### Using Let's Encrypt
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d your-domain.com
```

### Manual Certificate
Replace paths in Apache configuration:
```apache
SSLCertificateFile /path/to/your/certificate.crt
SSLCertificateKeyFile /path/to/your/private.key
SSLCertificateChainFile /path/to/your/chain.crt
```

## 9. Monitoring Commands

### System Status
```bash
# Apache status
sudo systemctl status apache2

# Disk usage
df -h

# Memory usage
free -h

# Process monitoring
htop
```

### Application Logs
```bash
# Real-time Apache logs
sudo tail -f /var/log/apache2/error.log

# Django application logs
tail -f /var/www/lifeline-accounting/logs/django.log
```

---

## Quick Reference Commands

```bash
# Restart services
sudo systemctl restart apache2

# Manual update (most common)
ssh ds3297l@10.100.5.61
cd /home/ds3297l && ./update-lifeline.sh

# Create backup before updates
cd /home/ds3297l && ./backup-lifeline.sh

# Check logs
sudo tail -f /var/log/apache2/error.log

# Test database connection
cd /var/www/lifeline-accounting/Accounting-Version-1/backend && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=lifeline_backend.settings_production && python manage.py shell

# Quick deployment workflow:
# 1. From Windows: git push origin main
# 2. SSH to server: ssh ds3297l@10.100.5.61  
# 3. Run update: ./update-lifeline.sh
```
