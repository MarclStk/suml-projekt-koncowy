@echo off
ECHO ================================
ECHO      LapiMate - Uruchamianie
ECHO ================================
ECHO.


@echo off

IF NOT EXIST ".venv\Scripts\activate.bat" (
    py -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        PAUSE
        EXIT /B 1
    )
)

CALL .venv\Scripts\activate.bat

WHERE py >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    py -m ensurepip --upgrade
    py -m pip --version >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        py -m ensurepip --default-pip
    )
)

IF NOT EXIST "requirements.txt" (
    PAUSE
    EXIT /B 1
)

py -m pip install --upgrade pip
py -m pip install wheel
py -m pip install scikit-learn
py -m pip install streamlit pandas matplotlib plotly fpdf forex-python pytest python-dotenv joblib
IF %ERRORLEVEL% NEQ 0 (
    PAUSE
    EXIT /B 1
)

IF NOT EXIST "models" mkdir models
IF NOT EXIST "outputs" mkdir outputs

IF NOT EXIST "models\best_model.joblib" (
    py src/utils/init_model.py
    IF %ERRORLEVEL% NEQ 0 (
        PAUSE
        EXIT /B 1
    )
)

start "" http://localhost:8501
py -m streamlit run app.py

CALL .venv\Scripts\deactivate.bat

PAUSE
EXIT /B 0

