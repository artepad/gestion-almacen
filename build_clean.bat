@echo off
REM =========================================
REM Script para construir el ejecutable
REM CON LIMPIEZA COMPLETA
REM =========================================

echo.
echo ========================================
echo CONSTRUYENDO GESTION COMERCIAL
echo (Limpieza completa)
echo ========================================
echo.

REM Limpiar builds anteriores
echo [1/4] Limpiando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "GestionComercial.spec" del /q "GestionComercial.spec"

REM Limpiar caché de Python
echo [2/4] Limpiando cache de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"

REM Construir con PyInstaller
echo.
echo [3/4] Compilando aplicacion con PyInstaller...
echo (Esto puede tardar 2-3 minutos...)
echo.
pyinstaller build_exe.spec --clean --noconfirm

REM Verificar resultado
echo.
echo [4/4] Verificando resultado...
if exist "dist\GestionComercial.exe" (
    echo.
    echo ========================================
    echo BUILD EXITOSO!
    echo ========================================
    echo.
    echo El ejecutable esta en: dist\GestionComercial.exe
    echo Tamano:
    dir "dist\GestionComercial.exe" | find "GestionComercial.exe"
    echo.
    echo Puedes probarlo ejecutando:
    echo   dist\GestionComercial.exe
    echo.
    echo O crear el instalador con Inno Setup
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
