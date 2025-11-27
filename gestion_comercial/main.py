import sys
import os
import tkinter as tk

# Add the current directory to sys.path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from gestion_comercial.core.app import MainApp
# Import views to register them (will be added later)
from gestion_comercial.modules.launcher.view import LauncherView
from gestion_comercial.modules.cash_counter.view import CashCounterView
from gestion_comercial.modules.tag_manager.view import TagManagerView
# Import licensing
from gestion_comercial.licensing import LicenseValidator
from gestion_comercial.modules.activation.view import show_activation_dialog


def check_license():
    """
    Verifica la licencia antes de iniciar la aplicación.

    Returns:
        bool: True si la licencia es válida, False si se debe salir
    """
    is_valid, message, needs_activation = LicenseValidator.validate_on_startup()

    if is_valid:
        # Licencia válida, continuar normalmente
        return True

    if needs_activation:
        # Mostrar ventana de activación
        activation_success = [False]  # Lista para permitir modificación en closure

        def on_success():
            activation_success[0] = True

        # Crear ventana de activación
        root = tk.Tk()
        root.withdraw()
        activation_window = show_activation_dialog(parent=root, on_success=on_success)
        activation_window.wait_window()  # Esperar a que se cierre

        if activation_success[0]:
            # Activación exitosa
            root.destroy()
            return True
        else:
            # Usuario canceló la activación
            root.destroy()
            return False

    return False


def main():
    """Función principal de la aplicación."""
    # Verificar licencia antes de iniciar
    if not check_license():
        print("Aplicación cerrada: licencia no válida o activación cancelada")
        sys.exit(0)

    # Licencia válida, iniciar aplicación
    app = MainApp()

    # Register views
    app.navigator.register_view('launcher', LauncherView)
    app.navigator.register_view('cash_counter', CashCounterView)
    app.navigator.register_view('tag_manager', TagManagerView)

    # Start with launcher
    app.navigator.show_view('launcher')

    app.mainloop()


if __name__ == "__main__":
    main()
