REM filepath: /d:/Python-App/ts_to_mp4/build_exe.bat
@echo on
echo Starting build process...

REM 检查 Python 是否安装
python --version
if errorlevel 1 (
    echo Python not found! Please install Python first.
    pause
    exit /b 1
)

REM 检查并安装 pyinstaller
pip show pyinstaller
if errorlevel 1 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

REM 执行打包命令
echo Building executable with pyinstaller...
pyinstaller --onefile --noconsole --add-data "C:\ffmpeg\bin\*.*;ffmpeg\bin" app.py

REM 检查是否成功
if errorlevel 1 (
    echo Build failed! See error message above.
) else (
    echo Build successful! Check the dist folder for the executable.
)

echo Build process complete.
pause
