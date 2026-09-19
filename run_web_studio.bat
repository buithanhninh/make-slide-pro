@echo off
chcp 65001 > nul
title Make Slide Pro Web Studio V8.3
cls

echo ================================================================================
echo           ★ MAKE SLIDE PRO V8.3 - WEB STUDIO LAUNCHER ★
echo     Universal Document-to-PowerPoint Web Publishing & Presentation Suite
echo ================================================================================
echo.
echo [*] Đang khởi động máy chủ Make Slide Pro Web Studio...
echo [*] Giao diện web sẽ tự động mở trong trình duyệt mặc định của bạn.
echo.

python -X utf8 run_web_studio.py

pause
