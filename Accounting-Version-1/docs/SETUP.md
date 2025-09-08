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

## Frontend Setup

1. Navigate to the frontend folder:
   ```powershell
   cd lifeline_accounting/frontend
   ```

2. Install Node.js dependencies:
   ```powershell
   npm install
   ```

3. Start the development server:
   ```powershell
   npm run serve
   ```

The application will be available at `http://localhost:8080/`.