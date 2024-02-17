@echo off
cd /d "%~dp0"
set /P ign=Enter ign: 
py main.py %ign%
