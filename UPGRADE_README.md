# Organ Donation Web App - Updated Version

This is an updated version of the Organ Donation Web App with modern dependencies.

## Changes Made

### Dependencies Updated:
- Django: 2.1.7 → 4.2.7 (LTS version)
- Pillow: 5.4.1 → 10.1.0
- reportlab: 3.5.13 → 4.0.7
- xhtml2pdf: 0.2.3 → 0.2.11
- WeasyPrint: 46 → 60.2
- All other dependencies updated to latest compatible versions

### Configuration Updates:
- Added `DEFAULT_AUTO_FIELD` setting for Django 4.2 compatibility
- Maintained all existing functionality

## Quick Setup

1. Run the setup script:
   ```
   setup.bat
   ```

2. Or manually:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

## Database
The existing SQLite database has been copied and should work with the updated Django version.

## Notes
- All your existing data, templates, static files, and media files have been preserved
- The project structure remains unchanged
- All custom apps (donors, hospitals) are intact