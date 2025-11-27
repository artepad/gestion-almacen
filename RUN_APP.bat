@echo off
REM =========================================
REM Launcher para Gestión Comercial
REM =========================================

title Gestion Comercial

echo.
echo ========================================
echo    GESTION COMERCIAL
echo ========================================
echo.

REM Ejecutar la aplicación
python run_app.py

REM Si hay error, mantener ventana abierta
if errorlevel 1 (
    echo.
    echo ========================================
    echo Presiona cualquier tecla para salir...
    echo ========================================
    pause >nul
)
