@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Team Bot - Max, Vivi, Jess
if exist "venv\Scripts\activate.bat" call "venv\Scripts\activate.bat"
if exist "..\venv\Scripts\activate.bat" call "..\venv\Scripts\activate.bat"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
rem Il PC non va in sospensione mentre i bot sono accesi (corrente e batteria)
powercfg /change standby-timeout-ac 0 >nul 2>nul
:avvio
echo [%date% %time%] Avvio del team... lascia aperta questa finestra.
python -m pcbot.main
echo [%date% %time%] I bot si sono fermati (codice %errorlevel%). Riparto tra 10 secondi...
timeout /t 10 /nobreak >nul
goto avvio
