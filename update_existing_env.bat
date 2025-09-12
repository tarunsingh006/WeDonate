@echo off
echo Updating existing environment with compatible dependencies...

echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Virtual environment not found. Run setup_dependencies.bat first.
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip

echo Uninstalling old packages...
pip uninstall -y Django cairocffi CairoSVG cffi cssselect2 defusedxml html5lib pdfkit Pillow pycparser PyPDF2 Pyphen pytz reportlab six tinycss2 WeasyPrint webencodings wkhtmltopdf xhtml2pdf

echo Installing updated dependencies...
pip install -r requirements_updated.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Collecting static files...
python manage.py collectstatic --noinput

echo Update completed successfully!
echo You can now run: python manage.py runserver
pause