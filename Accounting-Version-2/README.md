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

### Backend Deployment

1. **Update settings for production:**
   - Uncomment MSSQL database configuration in `settings.py`
   - Update `ALLOWED_HOSTS`
   - Set `DEBUG = False`

2. **Database Migration:**
   ```bash
   python manage.py migrate --settings=lifeline_backend.settings_production
   ```

3. **Static Files:**
   ```bash
   python manage.py collectstatic
   ```

### Frontend Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Deploy dist folder** to your web server

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
