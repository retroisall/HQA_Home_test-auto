@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
pytest tests/test_stream_search.py -v
pause
