@echo off
echo Setting up Organ Donation Web App with updated dependencies...

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing updated dependencies...
pip install -r requirements_updated.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Collecting static files...
python manage.py collectstatic --noinput

echo Running PostgreSQL sequence fix...
python fix_sequences.py

echo Setup completed successfully!
echo You can now run: python manage.py runserver
pause