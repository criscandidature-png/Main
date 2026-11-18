@echo off
rem Crea un collegamento in Esecuzione automatica: il team parte da solo quando accendi il PC
set "DEST=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Team Bot.bat"
(echo @echo off& echo start "Team Bot" /min "%~dp0avvia.bat") > "%DEST%"
echo Fatto: Max, Vivi e Jess partiranno da soli ad ogni accensione del PC.
pause
