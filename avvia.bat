@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Team Bot - Max, Vivi, Jess
if exist "venv\Scripts\activate.bat" call "venv\Scripts\activate.bat"
if exist "..\venv\Scripts\activate.bat" call "..\venv\Scripts\activate.bat"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
:avvio
echo Avvio del team... lascia aperta questa finestra.
python -m pcbot.main
if %errorlevel%==3 (echo Aggiornamento fatto, riavvio... & goto avvio)
echo.
echo I bot si sono fermati. Se vedi un errore qui sopra, fai uno screenshot.
pause
