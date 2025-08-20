@echo off
:: Fix Chinese encoding issue
chcp 65001 > nul

:: Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Please ensure Python is installed correctly.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install dependencies
 echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies. Please check your network connection.
    pause
    exit /b 1
)

:: Run the application
 echo Starting AI Personal Clone Assistant...
python app.py
if errorlevel 1 (
    echo Failed to start application.
    pause
    exit /b 1
)

pause

    exit /b 1
)

pause

:: 启动应用
echo 启动AI个人克隆助手...
python app.py
if errorlevel 1 (
    echo 启动应用失败。
    pause
    exit /b 1
)

pause