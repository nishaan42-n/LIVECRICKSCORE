@echo off
cd /d "%~dp0"
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if not exist .env (
  copy .env.example .env
  echo Created .env. Edit it and add your NEW RapidAPI key, then run this file again.
  pause
  exit /b 1
)
python app.py
pause
