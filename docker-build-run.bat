@echo off

docker --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    PAUSE
    EXIT /B 1
)

IF NOT EXIST "docker-compose.yml" (
    PAUSE
    EXIT /B 1
)

docker-compose down >nul 2>&1

docker-compose build
IF %ERRORLEVEL% NEQ 0 (
    PAUSE
    EXIT /B 1
)

docker-compose up -d
IF %ERRORLEVEL% NEQ 0 (
    PAUSE
    EXIT /B 1
)

PAUSE >nul

start http://localhost:8501
EXIT /B 0
