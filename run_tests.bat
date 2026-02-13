@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
pytest --html=report.html --self-contained-html
deactivate
exit /b %errorlevel%
