# Project Setup

This document guides you through setting up the Lifeline Accounting backend and frontend for local development.

## Prerequisites
- Python 3.13+ installed
- Node.js (v16+) and npm
- (Optional) Redis server for Celery

## Backend Setup

1. Clone the repo and navigate to the backend folder:
   ```powershell
   cd lifeline_accounting/backend
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv env
   & .\env\Scripts\Activate.ps1
   ```

3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Configure local settings in `lifeline_backend/settings.py` if needed.

5. Create database migrations and apply them:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. (Optional) Install and run Redis for Celery:
   ```powershell
   choco install redis-64 -y
   Start-Service redis
   ```

7. Start Celery worker:
   ```powershell
   celery -A lifeline_backend worker --loglevel=info
   ```

8. Run the Django development server:
   ```powershell
   python manage.py runserver
   ```

## Frontend Setup

1. Navigate to the `frontend` folder:
   ```powershell
   cd ../frontend
   ```

2. Install Node dependencies:
   ```powershell
   npm install
   ```

3. Run the development server:
   ```powershell
   npm run serve
   ```

4. Open your browser at `http://localhost:8080`.  

## Creating a Superuser

```powershell
python manage.py createsuperuser
```  
Use these credentials at `http://localhost:8000/admin/`.

user name: testuser
password: testpass123

user name: User1
password: Password#1