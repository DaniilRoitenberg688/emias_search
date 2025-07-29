@echo off
chcp 65001 > nul

REM Проверка наличия параметра version
if "%1"=="" (
    echo Ошибка: не указана версия. Пример использования: .\build_and_push.bat 3.2.73t
    exit /b 1
)

set version=%1

REM Проверка, работает ли Docker
docker info >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Docker не запущен или недоступен.
    exit /b 1
)

REM Сборка, тегирование и пуш образа
docker build -t rt-scan-doc-frontend ./frontend
if errorlevel 1 (
    echo Ошибка при сборке образа.
    exit /b 1
)

docker tag rt-scan-doc-frontend docker.emias.ru/stacionary/rt-scan-doc-frontend:%version%
docker push docker.emias.ru/stacionary/rt-scan-doc-frontend:%version%

REM Сборка, тегирование и пуш образа
docker build -t rt-scan-doc-backend ./backend
if errorlevel 1 (
    echo Ошибка при сборке образа.
    exit /b 1
)

docker tag rt-scan-doc-backend docker.emias.ru/stacionary/rt-scan-doc-backend:%version%
docker push docker.emias.ru/stacionary/rt-scan-doc-backend:%version%

cd scanner_backend
pyinstaller -F .\app.py
cd ..