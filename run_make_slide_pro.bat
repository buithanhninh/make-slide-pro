@echo off
chcp 65001 >nul
title Make Slide Pro V7.3 - Trình Biên Tập Slide Tự Động

echo ================================================================================
echo           ★ MAKE SLIDE PRO V7.3 - PRODUCTION SUITE ★
echo     Universal Document-to-PowerPoint Publishing & Quality Certification
echo ================================================================================
echo.

cd /d "%~dp0"

IF "%~1"=="" (
    echo [THÔNG BÁO] Khởi chạy chế độ tương tác (Interactive Mode)...
    python -X utf8 make_slide_pro.py
) ELSE (
    echo [THÔNG BÁO] Đang xử lý tệp được kéo thả: "%~nx1"
    echo.
    python -X utf8 make_slide_pro.py --input "%~1" --open
)

echo.
echo ================================================================================
echo Quá trình thực thi đã hoàn tất!
echo ================================================================================
pause
