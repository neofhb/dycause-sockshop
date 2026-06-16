@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0enable-istio.ps1" %*
