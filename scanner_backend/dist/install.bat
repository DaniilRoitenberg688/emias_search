@echo off
REM =========================================
REM Scanner Service Installer
REM Только создание и запуск службы
REM =========================================

REM Проверка прав администратора
echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Please run as Administrator!
    echo Right-click on this file -> "Run as administrator"
    pause
    exit /b 1
)

echo.
echo =========================================
echo SCANNER SERVICE INSTALLER
echo =========================================
echo.

REM Определяем путь к exe-файлу (там же где находится этот bat файл)
set SCRIPT_DIR=%~dp0
set EXE_FILE=%SCRIPT_DIR%win_sys.exe

echo Script directory: %SCRIPT_DIR%
echo Executable: %EXE_FILE%

REM Проверяем существование exe файла
if not exist "%EXE_FILE%" (
    echo ERROR: win_sys.exe not found in current directory!
    echo Please place this bat file in the same folder as win_sys.exe
    pause
    exit /b 1
)

echo.
echo =========================================
echo CREATING SERVICE: %SERVICE_NAME%
echo =========================================
echo.

REM Install service
echo Step 5: Installing service...
"%EXE_FILE%" install

REM Запускаем службу
echo Step 5: Starting service...
sc start ScannerBackendService

if %errorLevel% neq 0 (
    echo ERROR: Failed to start service!
    echo.
    echo Try running manually: sc start %SERVICE_NAME%
    pause
    exit /b 1
)

echo.
echo =========================================
echo INSTALLATION COMPLETE!
echo =========================================

pause
