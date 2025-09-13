@echo off
echo Installing all dependencies for WeDonate ML System...
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing PostgreSQL adapter...
pip install psycopg2-binary

echo.
echo Step 3: Installing ML dependencies...
pip install scikit-learn pandas numpy joblib

echo.
echo Step 4: Installing advanced ML libraries...
pip install xgboost lightgbm catboost imbalanced-learn

echo.
echo Step 5: Installing visualization libraries...
pip install matplotlib seaborn plotly

echo.
echo Step 6: Installing Django and web dependencies...
pip install Django python-decouple whitenoise gunicorn

echo.
echo Step 7: Installing additional dependencies...
pip install scipy Pillow requests

echo.
echo All dependencies installed successfully!
echo You can now run: python train_high_accuracy_model.py
pause