@echo off
echo PostgreSQL Migration Setup for Organ Donation Web App

echo Step 1: Installing PostgreSQL dependencies...
pip install psycopg2-binary

echo.
echo Step 2: Database setup instructions:
echo 1. Make sure PostgreSQL is installed and running
echo 2. Create database: createdb organ_donation_db
echo 3. Update password in settings.py (replace 'your_password')
echo.

echo Step 3: Creating new migrations...
python manage.py makemigrations hospitals donors

echo Step 4: Applying migrations...
python manage.py migrate

echo.
echo PostgreSQL setup complete!
echo Remember to update the password in settings.py before running migrations.
pause