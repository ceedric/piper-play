@echo off
rem Double-click this file to make your play.
rem The first time, Windows may ask if you are sure. See the README, Part 6.

chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 make_my_play.py
    goto done
)
where python >nul 2>nul
if %errorlevel%==0 (
    python make_my_play.py
    goto done
)
echo Python is not installed yet.
echo Please see Part 2 of the README, then double-click this file again.

:done
echo.
pause
