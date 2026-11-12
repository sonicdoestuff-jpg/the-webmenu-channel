@echo off
title the webmenu channel - Proxy Launcher

:: Request Administrator privileges to ensure firewall rule applies
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator permissions...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Step up one level from \run into the main webmenu folder
cd /d "%~dp0.."
cls

echo.
echo               ___.                                
echo __  _  __ ____\_ ^|__   _____   ____   ____  __ __ 
echo \ \/ \/ // __ \^| __ \ /     \_/ __ \ /    \^|  ^|  \
echo  \     /\  ___/^| \_\ \  Y Y  \  ___/^|   ^|  \  ^|  /
echo   \/\_/  \___  ^>___  /__^|_^|  /\___  ^>___^|  /____/ 
echo              \/    \/      \/     \/     \/       
echo.
echo ======================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo Failed! Please install Python!
    echo.
    pause
    exit /b
)

:: Allow port 8080 through Windows Firewall
netsh advfirewall firewall delete rule name="Switch Webmenu Proxy" >nul 2>&1
netsh advfirewall firewall add rule name="Switch Webmenu Proxy" dir=in action=allow protocol=TCP localport=8080 >nul 2>&1

color 0B
echo Successful! Please connect your Nintendo Switch to Wi-Fi, then press "Next"!
echo.
echo Switch Proxy Settings:
echo  -^> Server: 192.168.1.176
echo  -^> Port:   8080
echo.
echo ======================================================
echo Proxy Logs (Keep this window open while using your Switch):
echo.

python proxy_server.py
pause
