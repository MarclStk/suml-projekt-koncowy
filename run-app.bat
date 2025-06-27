@echo off
ECHO ================================
ECHO      LapiMate - Uruchamianie
ECHO ================================
ECHO.

CALL .venv\Scripts\activate.bat

WHERE py >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    py -m ensurepip --upgrade
    py -m pip --version >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        py -m ensurepip --default-pip
    )
)

py -m pip install --upgrade pip
py -m pip install wheel
py -m pip install scikit-learn
py -m pip install streamlit pandas matplotlib plotly fpdf forex-python pytest python-dotenv joblib
IF %ERRORLEVEL% NEQ 0 (
    PAUSE
    EXIT /B 1
)

py -m streamlit run app.py

CALL .venv\Scripts\deactivate.bat
