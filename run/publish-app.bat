@echo off
title the webmenu channel - Publish App

:: Step up one level from \run into the main webmenu folder
cd /d "%~dp0.."
cls

echo ======================================================
echo   the webmenu channel - App Store Publisher
echo ======================================================
echo.
set /p APP_NAME="Enter App Title: "
set /p APP_DESC="Enter Short Description: "
set /p APP_PATH="Drag & drop your .html app file here (or paste full path): "

:: Strip surrounding quotes if dragged and dropped
set APP_PATH=%APP_PATH:"=%

if not exist "%APP_PATH%" (
    color 0C
    echo.
    echo Error: File not found! Check the path and try again.
    pause
    exit /b
)

if not exist "store_apps" mkdir "store_apps"

for %%F in ("%APP_PATH%") do set "FILE_NAME=%%~nxF"
copy /Y "%APP_PATH%" "store_apps\%FILE_NAME%" >nul

python -c "import json, os; f='apps.json'; data=json.load(open(f)) if os.path.exists(f) else []; data.append({'title': r'%APP_NAME%', 'desc': r'%APP_DESC%', 'url': 'store_apps/%FILE_NAME%'}); json.dump(data, open(f,'w'), indent=2)"

color 0A
echo.
echo Published "%APP_NAME%" to the webmenu App Store!
pause
