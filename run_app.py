"""
Launcher para Gestión Comercial
Ejecuta la aplicación mostrando mensajes de debug
"""

import sys
import os

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 70)
print(" GESTIÓN COMERCIAL - INICIANDO")
print("=" * 70)

try:
    print("\n[1/3] Cargando módulos...")
    from gestion_comercial.main import main
    print("      ✓ Módulos cargados correctamente")

    print("\n[2/3] Verificando sistema de licencias...")
    from gestion_comercial.licensing import LicenseValidator

    is_valid, message, needs_activation = LicenseValidator.validate_on_startup()

    if is_valid:
        print(f"      ✓ Licencia válida: {message}")
    else:
        print(f"      ⚠ {message}")
        if needs_activation:
            print("      → Se mostrará la ventana de activación")

    print("\n[3/3] Iniciando aplicación...")
    print("=" * 70)
    print()

    # Ejecutar aplicación
    main()

except KeyboardInterrupt:
    print("\n\n✗ Aplicación interrumpida por el usuario")
    sys.exit(0)

except Exception as e:
    print(f"\n\n✗ ERROR CRÍTICO: {e}")
    print("\nDetalles del error:")
    import traceback
    traceback.print_exc()

    print("\n" + "=" * 70)
    print("La aplicación se cerrará. Presiona Enter para salir...")
    input()
    sys.exit(1)
