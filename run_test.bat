@echo off
cd /d %~dp0
call venv\Scripts\activate.bat

if not exist logs mkdir logs

pytest tests/test_stream_search.py -v -s --tb=short --log-cli-level=INFO --log-file=logs/test_run.log --log-file-level=INFO

echo.
echo Log saved to logs\test_run.log
pause
