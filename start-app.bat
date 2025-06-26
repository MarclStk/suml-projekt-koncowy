@echo off
ECHO ================================
ECHO   LapiMate - Start
ECHO ================================
ECHO.

CALL .venv\Scripts\activate.bat

IF NOT EXIST "models" mkdir models
IF NOT EXIST "outputs" mkdir outputs

py -m streamlit run app.py

CALL .venv\Scripts\deactivate.bat
