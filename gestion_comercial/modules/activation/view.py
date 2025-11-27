"""
Vista de activación de licencia.
Muestra la ventana para que el usuario active la aplicación.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gestion_comercial.licensing import get_formatted_hwid, LicenseValidator


class ActivationView(tk.Toplevel):
    """Ventana de activación de licencia."""

    def __init__(self, parent=None, on_success=None):
        """
        Inicializa la ventana de activación.

        Args:
            parent: Ventana padre (opcional)
            on_success: Callback a ejecutar cuando la activación sea exitosa
        """
        if parent:
            super().__init__(parent)
        else:
            # Si no hay padre, crear ventana raíz
            self.root = tk.Tk()
            self.root.withdraw()
            super().__init__(self.root)

        self.on_success = on_success
        self.hwid = get_formatted_hwid()

        self.title("Activación de Licencia - Gestión Comercial")
        self.geometry("600x450")
        self.resizable(False, False)

        # Centrar ventana
        self.center_window()

        # Hacer modal
        self.transient(parent if parent else self.root)
        self.grab_set()

        self.create_widgets()

        # Prevenir cierre con X
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Crea los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Activación de Licencia",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Por favor, active su copia de Gestión Comercial",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack(pady=(0, 20))

        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Información del HWID
        hwid_frame = ttk.LabelFrame(main_frame, text="Identificador de Equipo (HWID)", padding="15")
        hwid_frame.pack(fill=tk.X, pady=10)

        hwid_info = ttk.Label(
            hwid_frame,
            text="Este es el identificador único de su equipo.\nCompártalo con el proveedor para obtener su código de activación.",
            font=("Segoe UI", 9),
            foreground="#666"
        )
        hwid_info.pack(anchor=tk.W, pady=(0, 10))

        # Campo HWID (solo lectura)
        hwid_display_frame = ttk.Frame(hwid_frame)
        hwid_display_frame.pack(fill=tk.X)

        self.hwid_entry = ttk.Entry(
            hwid_display_frame,
            font=("Courier New", 10),
            justify=tk.CENTER
        )
        self.hwid_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.hwid_entry.insert(0, self.hwid)
        self.hwid_entry.config(state="readonly")

        # Botón copiar HWID
        copy_btn = ttk.Button(
            hwid_display_frame,
            text="Copiar",
            command=self.copy_hwid,
            width=10
        )
        copy_btn.pack(side=tk.RIGHT)

        # Frame de código de licencia
        license_frame = ttk.LabelFrame(main_frame, text="Código de Activación", padding="15")
        license_frame.pack(fill=tk.X, pady=10)

        license_info = ttk.Label(
            license_frame,
            text="Ingrese el código de activación proporcionado por el proveedor:",
            font=("Segoe UI", 9),
            foreground="#666"
        )
        license_info.pack(anchor=tk.W, pady=(0, 10))

        # Campo de código de licencia
        self.license_entry = ttk.Entry(
            license_frame,
            font=("Courier New", 12),
            justify=tk.CENTER
        )
        self.license_entry.pack(fill=tk.X, pady=5)
        self.license_entry.focus()

        # Formato de ejemplo
        format_label = ttk.Label(
            license_frame,
            text="Formato: XXXXX-XXXXX-XXXXX-XXXXX",
            font=("Segoe UI", 8),
            foreground="#999"
        )
        format_label.pack(pady=(5, 0))

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Botón activar
        activate_btn = ttk.Button(
            button_frame,
            text="Activar Licencia",
            command=self.activate_license,
            width=20
        )
        activate_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Botón salir
        exit_btn = ttk.Button(
            button_frame,
            text="Salir",
            command=self.on_closing,
            width=15
        )
        exit_btn.pack(side=tk.RIGHT)

        # Bind Enter key
        self.license_entry.bind('<Return>', lambda e: self.activate_license())

    def copy_hwid(self):
        """Copia el HWID al portapapeles."""
        self.clipboard_clear()
        self.clipboard_append(self.hwid)
        messagebox.showinfo(
            "HWID Copiado",
            "El identificador de equipo ha sido copiado al portapapeles."
        )

    def activate_license(self):
        """Intenta activar la licencia con el código ingresado."""
        license_code = self.license_entry.get().strip().upper()

        if not license_code:
            messagebox.showerror(
                "Error",
                "Por favor, ingrese un código de activación."
            )
            return

        # Intenta activar
        success, message = LicenseValidator.activate(license_code)

        if success:
            messagebox.showinfo(
                "¡Activación Exitosa!",
                "Su licencia ha sido activada correctamente.\n"
                "La aplicación se iniciará ahora."
            )

            # Ejecutar callback de éxito
            if self.on_success:
                self.on_success()

            # Cerrar ventana
            self.destroy()
            if hasattr(self, 'root'):
                self.root.destroy()

        else:
            messagebox.showerror(
                "Error de Activación",
                f"No se pudo activar la licencia:\n\n{message}\n\n"
                "Por favor, verifique el código e intente nuevamente."
            )

    def on_closing(self):
        """Maneja el cierre de la ventana."""
        result = messagebox.askyesno(
            "Salir",
            "Si cierra esta ventana, la aplicación se cerrará.\n\n"
            "¿Está seguro de que desea salir?"
        )

        if result:
            self.destroy()
            if hasattr(self, 'root'):
                self.root.destroy()
            sys.exit(0)


def show_activation_dialog(parent=None, on_success=None):
    """
    Muestra el diálogo de activación.

    Args:
        parent: Ventana padre (opcional)
        on_success: Función a ejecutar si la activación es exitosa

    Returns:
        ActivationView: La ventana de activación
    """
    window = ActivationView(parent, on_success)
    return window


if __name__ == "__main__":
    # Test standalone
    def on_activation_success():
        print("¡Activación exitosa!")

    app = show_activation_dialog(on_success=on_activation_success)
    app.mainloop()
