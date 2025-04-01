@echo off
echo EVA & GUARANI EGOS - BIOS-Q Initialization
echo =======================================
echo.
cd /d %~dp0
python BIOS-Q\init_bios_q.py
echo.
echo BIOS-Q initialization complete.
echo Please refer to QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md for next steps.
echo.
pause
