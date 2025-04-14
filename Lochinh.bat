@echo off
echo ===== UNG DUNG LOC HINH ANH =====
echo.

echo Dang kiem tra cac thu vien can thiet...
python -c "import PyQt5" 2>nul
if %errorlevel% neq 0 (
    echo Chua cai dat thu vien PyQt5
    echo Dang tien hanh cai dat...
    python -m pip install PyQt5
    if %errorlevel% neq 0 (
        echo Loi khi cai dat PyQt5. Vui long kiem tra lai.
        pause
        exit /b 1
    )
    echo Cai dat PyQt5 thanh cong!
)

echo.
echo Dang khoi dong ung dung...
start /b pythonw main.py
if %errorlevel% neq 0 (
    echo.
    echo Co loi xay ra khi chay ung dung. 
    echo Vui long kiem tra thu muc va cac thanh phan can thiet.
    pause
    exit /b 1
)
exit
