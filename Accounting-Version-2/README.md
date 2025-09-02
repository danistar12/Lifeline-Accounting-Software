# Lifeline Accounting Software - Version 2

A comprehensive accounting software solution with enhanced features, schema compliance, and modern architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd Accounting-Version-2/backend
   ```

2. **Set up virtual environment (if not already done):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create test data (optional but recommended):**
   ```bash
   python manage.py create_test_data
   ```

6. **Start the backend server:**
   ```bash
   python manage.py runserver 8001
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd Accounting-Version-2/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

## 🔐 Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`
- **Django Admin:** `http://127.0.0.1:8001/admin/`

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Django 5.0.14 with Django REST Framework
- SQLite (development) / MSSQL (production)
- Custom authentication with JWT support
- Comprehensive API endpoints

**Frontend:**
- Vue 3 with Composition API
- Vite for fast development
- Tailwind CSS for styling
- Modern responsive design

### Database Schema Compliance

Version 2 strictly follows the database schema specification with proper:
- Table naming conventions
- Column mappings using `db_column` attributes
- Foreign key relationships
- Data integrity constraints

## 📊 Features

### Core Accounting
- **Multi-company Support**: Manage multiple companies in one system
- **Chart of Accounts**: Comprehensive account structure
- **General Ledger**: Complete transaction tracking
- **Financial Reports**: Profit & Loss, Balance Sheet, Cash Flow

### Payroll Management
- **Employee Directory**: Complete employee information management
- **Payroll Processing**: Automated payroll calculations with tax withholding
- **Payroll Reports**: Comprehensive payroll analytics and summaries
- **Tax Management**: Automated tax calculations and reporting

### Banking & Transactions
- **Bank Account Management**: Multiple bank account support
- **Transaction Processing**: Automated transaction categorization
- **Bank Reconciliation**: Advanced reconciliation features
- **Banking Reports**: Transaction analysis and cash flow reporting

### Business Management
- **Customer Management**: Complete customer relationship tracking
- **Vendor Management**: Vendor information and payment tracking
- **Inventory Management**: Stock tracking and management (Version 2 enhancement)
- **Document Management**: File upload and organization system

### Reporting & Analytics
- **Financial Dashboard**: Real-time financial metrics and KPIs
- **Custom Reports**: Flexible reporting with date filtering
- **Data Export**: Export capabilities for all reports
- **Interactive Charts**: Visual data representation

### Security & Compliance
- **Role-based Access Control**: Admin, Accountant, Viewer roles
- **Audit Trail**: Complete audit logging system
- **Data Validation**: Comprehensive input validation
- **Secure Authentication**: JWT-based authentication system

## 🗄️ Database Models

### Core Models
- **Company**: Multi-tenant company management
- **User**: Enhanced user model with company relationships
- **ChartOfAccounts**: Account structure management
- **GeneralLedger**: Transaction recording

### Payroll Models
- **Employee**: Employee information (schema-compliant)
- **Payroll**: Payroll records with tax calculations
- **PayrollDeduction**: Flexible deduction management

### Banking Models
- **BankAccount**: Bank account management
- **BankTransaction**: Transaction processing and reconciliation

### Business Models
- **Customer**: Customer relationship management
- **Vendor**: Vendor management
- **Invoice**: Billing and invoicing
- **Bill**: Accounts payable management

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Token refresh

### Reports API
- `GET /api/reports/dashboard/` - Financial dashboard
- `GET /api/reports/payroll-summary/` - Payroll analysis
- `GET /api/reports/employees/` - Employee directory
- `GET /api/reports/banking/` - Banking reports
- `GET /api/reports/profit-loss/` - Profit & Loss statement
- `GET /api/reports/balance-sheet/` - Balance Sheet
- `GET /api/reports/cash-flow/` - Cash Flow statement

### Core APIs
- `/api/payroll/` - Payroll management
- `/api/banking/` - Banking operations
- `/api/contacts/` - Customer/Vendor management
- `/api/core/` - Core accounting functions

## 📈 Test Data

The system includes comprehensive test data for development and demonstration:

- **2 Companies** with full organizational structure
- **5 Employees** with realistic hourly rates and tax withholding
- **30 Payroll Records** spanning 3 months of bi-weekly pay periods
- **3 Bank Accounts** with 30 realistic transactions
- **28 Chart of Accounts** entries for comprehensive reporting
- **5 Customers and 5 Vendors** for business relationships

### Creating Test Data
```bash
python manage.py create_test_data
```

### Clearing Test Data
```bash
python manage.py clear_test_data
```

## 🛠️ Development Commands

### Django Management Commands

**Database Management:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check_database_tables  # Verify database structure
```

**User Management:**
```bash
python manage.py createsuperuser
```

**Test Data Management:**
```bash
python manage.py create_test_data     # Create comprehensive test data
python manage.py clear_test_data      # Clear all test data
```

**Development Server:**
```bash
python manage.py runserver 8001      # Start backend server
```

### Frontend Commands

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

## 🚀 Production Deployment

### Linux Server Deployment (02-vuweb01)

**Server Details:**
- **Server:** 02-vuweb01
- **IP:** 10.100.5.61
- **OS:** Linux with Apache2, MS ODBC driver
- **SSL:** Forced redirect enabled
- **Access:** SSH/Putty

#### Step 1: Connect to Server

```bash
# From Windows Command Line
ssh ds3297l@10.100.5.61
# or
ssh ds3297l@02-vuweb01

# Or use PuTTY with:
# Host: 10.100.5.61 or 02-vuweb01
# Username: ds3297l
# Password: ogpBdtXaBWgY6G9oLS9o3UBN
```

#### Step 2: Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y postgresql-client libpq-dev  # If using PostgreSQL
sudo apt install -y unixodbc-dev  # For MSSQL connectivity

# Install Node.js for frontend build
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Git
sudo apt install -y git

# Configure Apache modules
sudo a2enmod wsgi
sudo a2enmod ssl
sudo a2enmod rewrite
sudo systemctl restart apache2
```

#### Step 3: Deploy Application

```bash
# Create application directory
sudo mkdir -p /var/www/lifeline-accounting
sudo chown ds3297l:www-data /var/www/lifeline-accounting
cd /var/www/lifeline-accounting

# Clone repository (or upload files)
git clone https://github.com/danistar12/Lifeline-Accounting-Software.git .
# Or upload via SCP/SFTP

# Set up backend
cd Accounting-Version-2/backend

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install mod_wsgi  # For Apache integration

# Install additional production packages
pip install gunicorn  # Alternative to mod_wsgi
pip install whitenoise  # For static file serving
```

#### Step 4: Configure Database (MSSQL)

```bash
# Update settings.py for production
cd /var/www/lifeline-accounting/Accounting-Version-2/backend
```

Create `lifeline_backend/settings_production.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['10.100.5.61', '02-vuweb01', 'localhost']

# MSSQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'LifelineAccounting',
        'USER': 'LLAcct',
        'PASSWORD': 'SilverMoon#3',
        'HOST': '10.100.5.27',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}

# Security Settings
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static Files
STATIC_ROOT = '/var/www/lifeline-accounting/static/'
MEDIA_ROOT = '/var/www/lifeline-accounting/media/'

# Add Whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Step 5: Database Migration

```bash
# Run migrations on production database
source venv/bin/activate
python manage.py migrate --settings=lifeline_backend.settings_production

# Create superuser
python manage.py createsuperuser --settings=lifeline_backend.settings_production

# Collect static files
python manage.py collectstatic --settings=lifeline_backend.settings_production
```

#### Step 6: Build Frontend

```bash
cd /var/www/lifeline-accounting/Accounting-Version-2/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Copy build files to Apache directory
sudo cp -r dist/* /var/www/html/
```

#### Step 7: Configure Apache Virtual Host

Create `/etc/apache2/sites-available/lifeline-accounting.conf`:

```apache
<VirtualHost *:80>
    ServerName 02-vuweb01
    ServerAlias 10.100.5.61
    
    # Redirect all HTTP to HTTPS
    Redirect permanent / https://02-vuweb01/
</VirtualHost>

<VirtualHost *:443>
    ServerName 02-vuweb01
    ServerAlias 10.100.5.61
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
    
    # Frontend (Vue.js)
    DocumentRoot /var/www/html
    <Directory /var/www/html>
        Options -Indexes
        AllowOverride All
        Require all granted
        
        # Handle Vue.js routing
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
    
    # Backend API (Django)
    WSGIDaemonProcess lifeline python-path=/var/www/lifeline-accounting/Accounting-Version-2/backend python-home=/var/www/lifeline-accounting/Accounting-Version-2/backend/venv
    WSGIProcessGroup lifeline
    WSGIScriptAlias /api /var/www/lifeline-accounting/Accounting-Version-2/backend/lifeline_backend/wsgi.py
    
    <Directory /var/www/lifeline-accounting/Accounting-Version-2/backend/lifeline_backend>
        WSGIProcessGroup lifeline
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
    # Static files
    Alias /static /var/www/lifeline-accounting/static
    <Directory /var/www/lifeline-accounting/static>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /var/www/lifeline-accounting/media
    <Directory /var/www/lifeline-accounting/media>
        Require all granted
    </Directory>
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/lifeline_error.log
    CustomLog ${APACHE_LOG_DIR}/lifeline_access.log combined
</VirtualHost>
```

#### Step 8: Enable Site and Restart Apache

```bash
# Enable the site
sudo a2ensite lifeline-accounting.conf
sudo a2dissite 000-default.conf

# Test Apache configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2

# Check status
sudo systemctl status apache2
```

#### Step 9: Set Permissions

```bash
# Set proper ownership and permissions
sudo chown -R ds3297l:www-data /var/www/lifeline-accounting/
sudo chmod -R 755 /var/www/lifeline-accounting/
sudo chmod -R 775 /var/www/lifeline-accounting/media/
sudo chmod -R 775 /var/www/lifeline-accounting/static/

# Set executable permission for manage.py
chmod +x /var/www/lifeline-accounting/Accounting-Version-2/backend/manage.py
```

#### Step 10: Create WSGI Configuration

Update `/var/www/lifeline-accounting/Accounting-Version-2/backend/lifeline_backend/wsgi.py`:

```python
import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.append('/var/www/lifeline-accounting/Accounting-Version-2/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lifeline_backend.settings_production')

application = get_wsgi_application()
```

#### Step 11: Testing Deployment

```bash
# Test backend API
curl -k https://02-vuweb01/api/reports/dashboard/

# Check logs
sudo tail -f /var/log/apache2/lifeline_error.log
sudo tail -f /var/log/apache2/lifeline_access.log

# Test database connection
cd /var/www/lifeline-accounting/Accounting-Version-2/backend
source venv/bin/activate
python manage.py check --settings=lifeline_backend.settings_production
```

### Alternative: Gunicorn + Nginx (Recommended)

If you prefer a more robust setup, consider using Gunicorn with Nginx:

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service
sudo nano /etc/systemd/system/lifeline.service
```

```ini
[Unit]
Description=Lifeline Accounting Gunicorn daemon
After=network.target

[Service]
User=ds3297l
Group=www-data
WorkingDirectory=/var/www/lifeline-accounting/Accounting-Version-2/backend
ExecStart=/var/www/lifeline-accounting/Accounting-Version-2/backend/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/lifeline-accounting/lifeline.sock \
          lifeline_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl start lifeline
sudo systemctl enable lifeline
```

### Backup and Maintenance

```bash
# Create backup script
sudo nano /usr/local/bin/lifeline-backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/lifeline"

mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/lifeline_app_$DATE.tar.gz /var/www/lifeline-accounting/

# Backup database (if using local DB)
# mysqldump or pg_dump commands here

# Keep only last 7 days of backups
find $BACKUP_DIR -name "lifeline_app_*.tar.gz" -mtime +7 -delete
```

```bash
# Make executable and add to cron
sudo chmod +x /usr/local/bin/lifeline-backup.sh
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/lifeline-backup.sh
```

### Monitoring and Logging

```bash
# Set up log rotation
sudo nano /etc/logrotate.d/lifeline
```

```
/var/log/apache2/lifeline_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload apache2
    endscript
}
```

### Security Hardening

```bash
# Update firewall rules
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Set up fail2ban for SSH protection
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Troubleshooting Production Issues

**Common Issues:**

1. **Permission Errors:**
   ```bash
   sudo chown -R ds3297l:www-data /var/www/lifeline-accounting/
   sudo chmod -R 755 /var/www/lifeline-accounting/
   ```

2. **Database Connection Issues:**
   ```bash
   # Test MSSQL connection
   python manage.py check_database_tables --settings=lifeline_backend.settings_production
   ```

3. **Static Files Not Loading:**
   ```bash
   python manage.py collectstatic --settings=lifeline_backend.settings_production
   sudo systemctl restart apache2
   ```

4. **Apache Errors:**
   ```bash
   sudo tail -f /var/log/apache2/error.log
   sudo apache2ctl configtest
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (MSSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'LifelineAccounting',
        'USER': 'LLAcct',
        'PASSWORD': 'SilverMoon#3',
        'HOST': '10.100.5.27',
        'OPTIONS': {
            'driver': 'SQL Server',
        },
    }
}
```

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### API Testing
Use tools like Postman or curl to test API endpoints:

```bash
# Test dashboard endpoint
curl -X GET http://127.0.0.1:8001/api/reports/dashboard/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📚 Documentation

- **API Documentation**: Available at `/api/schema/` when server is running
- **Admin Interface**: Available at `/admin/`
- **Database Schema**: See `DATABASE_SCHEMA.md` in the root directory

## 🤝 Contributing

1. Create a feature branch from `master`
2. Make your changes following the coding standards
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maintain database schema compliance
- Write tests for new features

## 🐛 Troubleshooting

### Common Issues

**1. Django can't find modules:**
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**2. Database migration errors:**
```bash
# Clear migrations and start fresh
rm apps/*/migrations/00*.py
python manage.py makemigrations
python manage.py migrate
```

**3. Authentication issues:**
```bash
# Reset admin password
python manage.py shell -c "
from apps.accounts.models import User
user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()
"
```

**4. Frontend connection issues:**
- Ensure backend is running on port 8001
- Check CORS settings in Django settings
- Verify API base URL in frontend configuration

## 📄 License

[Add your license information here]

## 💬 Support

For questions, issues, or support:
- Create an issue in the GitHub repository
- Contact: [Add contact information]

## 🔄 Version History

### Version 2.0.0 (Current)
- Schema-compliant database models
- Comprehensive reporting system
- Enhanced payroll management
- Modern Vue 3 frontend
- Improved security and authentication
- Complete test data management

---

**Note**: This is Version 2 of the Lifeline Accounting Software. For Version 1, see the `Accounting-Version-1` directory.
