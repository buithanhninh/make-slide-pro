@echo off
chcp 65001 > nul
echo ================================================================================
echo    MAKE SLIDE PRO V8.6.0 - 1-CLICK SYNC TO VPS (hmu-vm-makeslidepro)
echo ================================================================================
python "%~dp0scripts\sync_to_vps.py" %*
pause
