@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%start-sockshop.ps1"
if errorlevel 1 (
  echo.
  echo Start failed.
) else (
  echo.
  echo Start finished.
)
pause
