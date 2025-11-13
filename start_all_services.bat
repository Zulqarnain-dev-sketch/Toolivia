@echo off
echo Starting All Advanced Services...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Starting Image Enhancement Service on port 5000...
start "Image Enhancement" python image_enhancer.py
timeout /t 2 /nobreak >nul

echo Starting Advanced Tools Service on port 5001...
start "Advanced Tools" python advanced_tools_service.py
timeout /t 2 /nobreak >nul

echo.
echo ✅ All services started successfully!
echo.
echo Services running:
echo - Image Enhancement: http://127.0.0.1:5000
echo - Advanced Tools: http://127.0.0.1:5001
echo.
echo Keep these windows open while using the application.
echo Press any key to continue...
pause >nul