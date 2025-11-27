@echo off
REM =========================================
REM Script para construir el ejecutable
REM =========================================

echo.
echo ========================================
echo CONSTRUYENDO GESTION COMERCIAL
echo ========================================
echo.

REM Limpiar builds anteriores
echo [1/3] Limpiando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Construir con PyInstaller
echo.
echo [2/3] Compilando aplicacion con PyInstaller...
pyinstaller build_exe.spec --clean

REM Verificar resultado
echo.
echo [3/3] Verificando resultado...
if exist "dist\GestionComercial.exe" (
    echo.
    echo ========================================
    echo BUILD EXITOSO!
    echo ========================================
    echo.
    echo El ejecutable esta en: dist\GestionComercial.exe
    echo.
    echo Puedes probarlo ejecutando:
    echo   dist\GestionComercial.exe
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR EN EL BUILD
    echo ========================================
    echo.
    echo Revisa los errores arriba.
    echo.
)

pause
