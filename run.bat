@echo off
cd /d "%~dp0"
if not exist venv (
    python -m venv venv
    venv\Scripts\python -m pip install -r requirements\dev.txt
)
if not exist .env copy .env.example .env
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py seed_demo
echo.
echo Open http://127.0.0.1:8000/admin/   (admin@gamerlair.com / admin12345)
venv\Scripts\python manage.py runserver
