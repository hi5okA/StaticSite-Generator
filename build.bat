@echo off
set BASEPATH=%1
if "%BASEPATH%"=="" set BASEPATH=/
python src/main.py %BASEPATH%
