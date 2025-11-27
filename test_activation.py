"""
Script de prueba simple para verificar el sistema de activación
"""

import sys
import os

# Add to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 60)
print("TEST DE ACTIVACIÓN - GESTIÓN COMERCIAL")
print("=" * 60)

# Test 1: Verificar imports
print("\n[1/4] Verificando imports...")
try:
    from gestion_comercial.licensing import get_formatted_hwid, LicenseValidator
    from gestion_comercial.modules.activation.view import show_activation_dialog
    print("✓ Imports correctos")
except Exception as e:
    print(f"✗ Error en imports: {e}")
    sys.exit(1)

# Test 2: Generar HWID
print("\n[2/4] Generando HWID...")
try:
    hwid = get_formatted_hwid()
    print(f"✓ HWID generado: {hwid}")
except Exception as e:
    print(f"✗ Error generando HWID: {e}")
    sys.exit(1)

# Test 3: Verificar estado de licencia
print("\n[3/4] Verificando estado de licencia...")
try:
    is_valid, message, needs_activation = LicenseValidator.validate_on_startup()
    print(f"   Válida: {is_valid}")
    print(f"   Mensaje: {message}")
    print(f"   Necesita activación: {needs_activation}")
except Exception as e:
    print(f"✗ Error verificando licencia: {e}")
    sys.exit(1)

# Test 4: Mostrar ventana de activación
print("\n[4/4] Mostrando ventana de activación...")
print("   (Se abrirá una ventana, ciérrala para continuar)")

try:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()

    activation_success = [False]

    def on_success():
        activation_success[0] = True
        print("\n✓ ¡Activación exitosa!")

    activation_window = show_activation_dialog(parent=root, on_success=on_success)

    # Mostrar la ventana
    activation_window.deiconify()
    activation_window.lift()
    activation_window.focus_force()

    activation_window.wait_window()

    root.destroy()

    if activation_success[0]:
        print("\n" + "=" * 60)
        print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ Activación cancelada")
        print("=" * 60)

except Exception as e:
    print(f"✗ Error mostrando ventana: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
