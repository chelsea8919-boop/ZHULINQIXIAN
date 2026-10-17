@echo off
setlocal
title Zhulin Sages - Local Preview Server (Camera Gesture)
cd /d "%~dp0"

rem ============================================================
rem  Find a usable Python in this order:
rem    1) py launcher   2) python on PATH   3) WorkBuddy bundled
rem ============================================================

where py >nul 2>&1
if errorlevel 1 goto try_python
py -3 -c "import http.server" >nul 2>&1
if errorlevel 1 goto try_python
goto run_py_launcher

:try_python
where python >nul 2>&1
if errorlevel 1 goto try_bundled
python -c "import http.server" >nul 2>&1
if errorlevel 1 goto try_bundled
goto run_python

:try_bundled
for /d %%D in ("%USERPROFILE%\.workbuddy\binaries\python\versions\*") do if exist "%%D\python.exe" set "PYB=%%D\python.exe"
if defined PYB goto run_bundled
goto no_python

:run_py_launcher
echo Starting local server ... entry: http://127.0.0.1:8000/puzzle.html
echo After the browser opens, click the "Start Gesture Control"
echo button and allow camera permission. Keep this window open.
echo.
py -3 run_local.py --open
goto end

:run_python
echo Starting local server ... entry: http://127.0.0.1:8000/puzzle.html
echo After the browser opens, click the "Start Gesture Control"
echo button and allow camera permission. Keep this window open.
echo.
python run_local.py --open
goto end

:run_bundled
echo Starting local server ... entry: http://127.0.0.1:8000/puzzle.html
echo After the browser opens, click the "Start Gesture Control"
echo button and allow camera permission. Keep this window open.
echo.
"%PYB%" run_local.py --open
goto end

:no_python
echo.
echo [ERROR] No usable Python found (tried: py / python / WorkBuddy bundled).
echo Install Python 3.8+ from python.org (check "Add python.exe to PATH"),
echo or make sure the WorkBuddy bundled python exists, then retry.
echo.
pause
exit /b 1

:end
echo.
echo Server stopped.
pause
