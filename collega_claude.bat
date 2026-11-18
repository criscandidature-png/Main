@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where claude >nul 2>nul || (echo Claude Code non trovato: installalo da PowerShell con  irm https://claude.ai/install.ps1 ^| iex & pause & exit /b)
echo Accedi con il tuo account Claude. Quando hai finito scrivi /exit
claude
pause
