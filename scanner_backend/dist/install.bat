@echo off
:: =============================================
:: Service Installer (Run as Administrator)
:: =============================================

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run this as Administrator!
    pause
    exit /b 1
)

:: Configuration
set "SERVICE_NAME=emias scanner module"
set "SERVICE_DISPLAY_NAME=emias scanner module"
set "SERVICE_DESCRIPTION=helps you to scan"
set "EXE_NAME=scanner_module.exe"

:: Get absolute path of the current folder
for %%I in ("%~dp0.") do set "FOLDER_PATH=%%~fI"
set "EXE_PATH=%FOLDER_PATH%\%EXE_NAME%"

:: Verify EXE exists
if not exist "%EXE_PATH%" (
    echo [ERROR] %EXE_NAME% not found in:
    echo "%FOLDER_PATH%"
    pause
    exit /b 1
)

:: Remove old service if it exists
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorLevel% equ 0 (
    echo [INFO] Removing old service...
    sc stop "%SERVICE_NAME%" >nul 2>&1
    sc delete "%SERVICE_NAME%" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

:: Install new service
echo [INFO] Installing service...
sc create "%SERVICE_NAME%" binPath= "%EXE_PATH%" DisplayName= "%SERVICE_DISPLAY_NAME%" start= auto >nul
sc description "%SERVICE_NAME%" "%SERVICE_DESCRIPTION%" >nul
sc failure "%SERVICE_NAME%" reset= 30 actions= restart/5000 >nul

:: Start service
sc start "%SERVICE_NAME%" >nul

echo [SUCCESS] Service installed and running!
echo Service Name: %SERVICE_NAME%
echo EXE Path: "%EXE_PATH%"
pause