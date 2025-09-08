# Lifeline Accounting Software

A comprehensive accounting software solution.

## Repository Structure

This repository contains the Lifeline Accounting Software project with the following structure:

```
├── Accounting-Version-1/          # First version implementation
│   ├── lifeline_accounting/
│   │   ├── backend/               # Django backend
│   │   └── frontend/              # Vue.js frontend
│   ├── docs/                      # Version 1 documentation
│   └── screenshots/               # Version 1 screenshots
├── Alex Docs/                     # Additional documentation
├── Diagrams/                      # System diagrams and flowcharts
├── Lifeline Accounting Application Development Document.docx
├── Lifeline Accounting Application Development Document.pdf
└── X_api_Key.txt                  # API keys (ignored by git)
```

## Technology Stack

### Backend (Django/Python)
- Django REST Framework
- SQLite database
- Python 3.13
- Celery for background tasks

### Frontend (Vue.js)
- Vue 3
- Vue Router
- Vuex for state management
- Modern JavaScript/TypeScript

## Version Differences

### Version 1
- Original implementation with full audit system
- Advanced user management
- Complete accounting modules
- Rich UI components

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 16+
- npm or yarn

### Setup Version 1

1. **Backend Setup:**
   ```bash
   cd Accounting-Version-1/lifeline_accounting/backend
   python -m venv env
   .\env\Scripts\activate  # Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Frontend Setup:**
   ```bash
   cd Accounting-Version-1/lifeline_accounting/frontend
   npm install
   npm run serve
   ```

## Features

- **Multi-company Support**: Manage multiple companies in one system
- **Complete Accounting**: Chart of Accounts, General Ledger, Financial Reports
- **Accounts Payable/Receivable**: Full AP/AR management
- **Banking**: Bank reconciliation and statement processing
- **Payroll**: Employee management and payroll processing
- **Inventory**: Stock management (Version 2)
- **Document Management**: File upload and organization
- **Audit Trail**: Complete audit logging system
- **User Management**: Role-based access control
- **Reports**: Financial statements and custom reports

## Documentation

- Main documentation: `Lifeline Accounting Application Development Document.pdf`
- Additional docs: `Alex Docs/Lifeline Accounting System Software Documentation v3.pdf`
- Setup instructions: See individual version README files

## Development Workflow

1. Choose the version you want to work on
2. Set up the development environment following the setup instructions
3. Make changes in the appropriate version directory
4. Test your changes locally
5. Commit and push to the repository

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Add your license information here]

## Support

For questions or support, please [add contact information].
