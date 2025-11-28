"""
Script de verificación de estructura del proyecto
Verifica que todos los archivos necesarios existan antes de hacer build
"""

import os
import sys

# Fix encoding para Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
print("=" * 70)

errors = []
warnings = []

# Archivos que DEBEN existir
required_files = [
    "gestion_comercial/__init__.py",
    "gestion_comercial/main.py",
    "gestion_comercial/core/__init__.py",
    "gestion_comercial/core/app.py",
    "gestion_comercial/core/navigation.py",
    "gestion_comercial/config/__init__.py",
    "gestion_comercial/config/settings.py",
    "gestion_comercial/config/theme.py",
    "gestion_comercial/modules/__init__.py",
    "gestion_comercial/modules/launcher/__init__.py",
    "gestion_comercial/modules/launcher/view.py",
    "gestion_comercial/modules/cash_counter/__init__.py",
    "gestion_comercial/modules/cash_counter/view.py",
    "gestion_comercial/modules/cash_counter/model.py",
    "gestion_comercial/modules/tag_manager/__init__.py",
    "gestion_comercial/modules/tag_manager/view.py",
    "gestion_comercial/modules/tag_manager/model.py",
    "gestion_comercial/modules/activation/__init__.py",
    "gestion_comercial/modules/activation/view.py",
    "gestion_comercial/licensing/__init__.py",
    "gestion_comercial/licensing/hwid.py",
    "gestion_comercial/licensing/crypto.py",
    "gestion_comercial/licensing/validator.py",
    "build_exe.spec",
    "tools/license_generator.py",
]

print("\n[1/3] Verificando archivos requeridos...")
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - FALTANTE")
        errors.append(f"Archivo faltante: {file}")

# Verificar que PyInstaller esté instalado
print("\n[2/3] Verificando PyInstaller...")
try:
    import PyInstaller
    print(f"  ✓ PyInstaller instalado (versión {PyInstaller.__version__})")
except ImportError:
    print("  ✗ PyInstaller NO está instalado")
    errors.append("PyInstaller no está instalado. Ejecuta: pip install pyinstaller")

# Verificar que los módulos se puedan importar
print("\n[3/3] Verificando que los módulos se puedan importar...")
try:
    sys.path.insert(0, os.getcwd())

    from gestion_comercial.core.app import MainApp
    print("  ✓ gestion_comercial.core.app")

    from gestion_comercial.core.navigation import Navigator
    print("  ✓ gestion_comercial.core.navigation")

    from gestion_comercial.licensing import get_hwid, LicenseValidator
    print("  ✓ gestion_comercial.licensing")

    from gestion_comercial.modules.activation.view import show_activation_dialog
    print("  ✓ gestion_comercial.modules.activation")

    print("\n  ✓ Todos los módulos se importaron correctamente")

except Exception as e:
    print(f"\n  ✗ Error al importar módulos: {e}")
    errors.append(f"Error de importación: {e}")
    import traceback
    traceback.print_exc()

# Resumen
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)

if errors:
    print(f"\n❌ Se encontraron {len(errors)} errores:")
    for error in errors:
        print(f"  • {error}")
    print("\n⚠ NO ejecutes el build hasta corregir estos errores.")
    sys.exit(1)
else:
    print("\n✅ ¡TODO CORRECTO!")
    print("   Puedes ejecutar el build con seguridad:")
    print("   → Ejecuta: build_clean.bat")
    print()
    sys.exit(0)
