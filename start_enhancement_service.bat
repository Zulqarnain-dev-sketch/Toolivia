@echo off
echo Starting Image Enhancement Service...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Python service on http://127.0.0.1:5000
python image_enhancer.py
pause