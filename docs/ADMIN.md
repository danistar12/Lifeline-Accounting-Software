# Admin Access

The Django admin interface allows full access to all models and data in the system.

URL: http://localhost:8000/admin/

## Creating a Superuser

Before you can log in, you need to create an admin (superuser) account. Run:

```powershell
# Activate virtualenv (if not already)
& ".\env\Scripts\Activate.ps1"

# From backend folder:
python manage.py createsuperuser
```

You will be prompted to enter:
- **Username** admin
- **Email address** (e.g. `admin@lifelinedatacenters.com)
- **Password** Password#123

Once created, use these credentials to log in at `/admin/`.

> Note: In a production environment, ensure you secure this interface behind HTTPS and restrict access by network or VPN as needed.