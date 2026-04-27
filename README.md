# GrabInfo

`GrabInfo` is a Django web app with user accounts, profiles, post creation, topic-based filtering, and image uploads.

## Tech Stack

- Python 3.10+ recommended
- Django 5
- SQLite for local development
- PostgreSQL optional via environment variables
- `django-jazzmin` for the admin UI
- Pillow for image fields
- `psycopg2-binary` for PostgreSQL connectivity

## Project Structure

```text
grabinfo-main/
|-- manage.py
|-- grab/                # Main app
|-- grabinfo/            # Django project settings
|-- media/               # Uploaded files
`-- static/              # Static assets
```

## Prerequisites

Install these before running the project:

- Python 3.10 or newer
- PostgreSQL 14+ or any reasonably recent version
- `pip`
- Optional: `venv`

## Database Configuration

By default, the project now uses SQLite for local development. No separate database server is required.

The SQLite database file is created automatically at:

- `db.sqlite3`

### Optional: PostgreSQL

If you want to use PostgreSQL instead, set these environment variables before running Django:

```powershell
$env:USE_POSTGRES="1"
$env:POSTGRES_DB="grab"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```

Then create the database in PostgreSQL:

```sql
CREATE DATABASE grab;
```

## Installation

### Windows PowerShell

```powershell
cd D:\program\python\grabinfo-main
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install Django==5.0.7 django-jazzmin Pillow psycopg2-binary
```

### macOS / Linux

```bash
cd /path/to/grabinfo-main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install Django==5.0.7 django-jazzmin Pillow psycopg2-binary
```

## Run the Project

After dependencies are installed:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Useful Commands

Run the development server on a custom port:

```powershell
python manage.py runserver 0.0.0.0:8000
```

Collect static files:

```powershell
python manage.py collectstatic
```

Run tests:

```powershell
python manage.py test
```

## Notes

- The checked-in `.venv` points to a machine-specific Python path and should be recreated locally.
- This project uses uploaded media from the `media/` folder during development.
- Static and media files are served by Django only when `DEBUG = True`.
- PostgreSQL is still supported, but only when `USE_POSTGRES=1` is set.

## Current Run Status

I verified the startup entry point is `manage.py`, and the project now runs locally with `python manage.py runserver` using SQLite by default.
