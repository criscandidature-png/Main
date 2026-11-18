@echo off
chcp 65001 >nul
cd /d "%~dp0cervelli\max"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
echo Collego Notion a Max.
echo 1) Nella chat che si apre scrivi:  /mcp
echo 2) Scegli "notion" e poi "Authenticate": nel browser accedi a Notion e premi Consenti
echo 3) Quando vedi "connected" scrivi:  /exit
echo.
claude
pause
