"""
Ventana de escáner de código de barras.
Permite buscar productos en la base de datos y autocompletar información.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import os
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.database import ProductDatabase


class BarcodeScannerWindow(tk.Toplevel):
    """Ventana emergente para escanear códigos de barras y buscar productos."""

    def __init__(self, parent, row_index, on_product_selected):
        """
        Inicializa la ventana de escáner.

        Args:
            parent: Ventana padre
            row_index (int): Índice de la fila (0-13)
            on_product_selected (callable): Callback que recibe (row_index, name, price)
        """
        super().__init__(parent)

        self.row_index = row_index
        self.on_product_selected = on_product_selected

        self.setup_window()
        self.setup_ui()

        # Actualizar información de la base de datos
        self.update_db_info()

        # Foco en el campo de código
        self.barcode_entry.focus_set()

    def setup_window(self):
        """Configura las propiedades de la ventana."""
        self.title(f"Escáner de Código de Barras - Fila {self.row_index + 1:02d}")
        self.configure(bg=Theme.BACKGROUND)
        self.resizable(False, False)

        # Tamaño de la ventana
        window_width = 520
        window_height = 350

        # Centrar la ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Hacer modal
        self.transient(self.master)
        self.grab_set()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Header
        self.create_header()

        # Contenido principal
        content_frame = tk.Frame(self, bg=Theme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Sección de información de BD
        self.create_db_info_section(content_frame)

        # Sección de escáner
        self.create_scanner_section(content_frame)

        # Botón cerrar
        self.create_close_button(content_frame)

    def create_header(self):
        """Crea el encabezado de la ventana."""
        header_frame = tk.Frame(self, bg=Theme.BILLS_FG, height=85)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Línea de acento verde
        tk.Frame(header_frame, bg='#27ae60', height=4).pack(fill='x')

        # Contenedor centrado
        content_container = tk.Frame(header_frame, bg=Theme.BILLS_FG)
        content_container.pack(expand=True)

        # Icono (más pequeño)
        tk.Label(
            content_container,
            text="🔍",
            font=(Theme.FONT_FAMILY, 24),
            bg=Theme.BILLS_FG,
            fg='white'
        ).pack(pady=(0, 3))

        # Título (más pequeño)
        tk.Label(
            content_container,
            text="Búsqueda de Producto",
            font=(Theme.FONT_FAMILY, 13, 'bold'),
            bg=Theme.BILLS_FG,
            fg='white'
        ).pack()

    def create_db_info_section(self, parent):
        """Crea la sección de información de la base de datos."""
        self.info_frame = tk.LabelFrame(
            parent,
            text="📊 Base de Datos",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=15,
            pady=10
        )
        self.info_frame.pack(fill='x', pady=(0, 15))

        # Contenedor de información
        self.db_status_label = tk.Label(
            self.info_frame,
            text="Verificando...",
            font=(Theme.FONT_FAMILY, 9),
            bg='#f8f9fa',
            fg='#6c757d',
            justify='left',
            anchor='w'
        )
        self.db_status_label.pack(fill='x')

        # Botón para buscar BD (se mostrará solo si no existe)
        self.search_db_button = tk.Button(
            self.info_frame,
            text="📁 Buscar Archivo de Base de Datos",
            font=(Theme.FONT_FAMILY, 9, 'bold'),
            bg='#007bff',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.search_database_file
        )
        # No se empaqueta aún, solo si no existe BD

    def create_scanner_section(self, parent):
        """Crea la sección de escáner."""
        scanner_frame = tk.LabelFrame(
            parent,
            text="🔢 Código de Barras",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='white',
            fg='#495057',
            padx=15,
            pady=15
        )
        scanner_frame.pack(fill='x', pady=(0, 15))

        # Instrucciones
        tk.Label(
            scanner_frame,
            text="Escanea o ingresa el código del producto:",
            font=(Theme.FONT_FAMILY, 9),
            bg='white',
            fg='#6c757d'
        ).pack(anchor='w', pady=(0, 8))

        # Campo de entrada
        self.barcode_entry = tk.Entry(
            scanner_frame,
            font=(Theme.FONT_FAMILY, 12),
            bg='#f8f9fa',
            relief='flat',
            bd=1,
            highlightthickness=2,
            highlightbackground='#ced4da',
            highlightcolor='#27ae60'
        )
        self.barcode_entry.pack(fill='x', ipady=6)

        # Bind para búsqueda automática
        self.barcode_entry.bind('<Return>', lambda e: self.auto_search())

    def create_close_button(self, parent):
        """Crea el botón de cerrar."""
        button_frame = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_frame.pack(fill='x')

        # Botón Cerrar
        close_btn = tk.Button(
            button_frame,
            text="Cerrar",
            font=(Theme.FONT_FAMILY, 10, 'bold'),
            bg='#6c757d',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.destroy
        )
        close_btn.pack()

        # Hover effect
        def on_enter(e):
            close_btn.config(bg='#5a6268')

        def on_leave(e):
            close_btn.config(bg='#6c757d')

        close_btn.bind('<Enter>', on_enter)
        close_btn.bind('<Leave>', on_leave)

    def update_db_info(self):
        """Actualiza la información de la base de datos."""
        info = ProductDatabase.get_database_info()

        if info['exists']:
            status_text = f"✓ Archivo encontrado\n"
            status_text += f"Última actualización: {info['last_modified']}\n"
            status_text += f"Productos registrados: {info['total_products']}"
            color = '#28a745'
            # Ocultar botón de búsqueda si existe BD
            self.search_db_button.pack_forget()
        else:
            status_text = f"✗ Archivo no encontrado\n"
            status_text += f"Debe buscar y cargar un archivo Excel (.xlsx)"
            color = '#dc3545'
            # Mostrar botón de búsqueda
            self.search_db_button.pack(pady=(10, 0))

        self.db_status_label.config(text=status_text, fg=color)

    def auto_search(self):
        """Busca automáticamente el producto y transfiere los datos."""
        barcode = self.barcode_entry.get().strip()

        if not barcode:
            messagebox.showwarning("Código Vacío", "Por favor escanea un código de barras", parent=self)
            return

        # Buscar en la base de datos
        success, result = ProductDatabase.search_product(barcode)

        if success:
            # Producto encontrado - transferir datos inmediatamente
            self.on_product_selected(
                self.row_index,
                result['name'],
                result['price']
            )

            # Animación de éxito (verde)
            self.barcode_entry.config(highlightbackground='#28a745', highlightthickness=2, bg='#d4edda')

            # Volver a color normal después de 300ms
            self.after(300, lambda: self.barcode_entry.config(
                highlightbackground='#ced4da',
                highlightthickness=2,
                bg='#f8f9fa'
            ))

            # Limpiar campo para siguiente escaneo
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.focus_set()
        else:
            # Producto no encontrado
            messagebox.showerror("Producto No Encontrado", result, parent=self)

            # Animación de error (rojo)
            self.barcode_entry.config(highlightbackground='#dc3545', highlightthickness=2, bg='#f8d7da')

            # Volver a color normal después de 500ms
            self.after(500, lambda: self.barcode_entry.config(
                highlightbackground='#ced4da',
                highlightthickness=2,
                bg='#f8f9fa'
            ))

            # Limpiar campo
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.focus_set()

    def search_database_file(self):
        """Permite al usuario buscar y cargar un archivo de base de datos manualmente."""
        # Abrir diálogo para seleccionar archivo Excel
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo de Base de Datos",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            parent=self
        )

        if file_path:
            try:
                # Asegurar que la carpeta bd existe
                if not os.path.exists(ProductDatabase.DB_FOLDER):
                    os.makedirs(ProductDatabase.DB_FOLDER)

                # Obtener nombre del archivo y copiar a la carpeta bd
                filename = os.path.basename(file_path)
                destination = os.path.join(ProductDatabase.DB_FOLDER, filename)

                shutil.copy2(file_path, destination)

                # Refrescar información de la base de datos
                self.update_db_info()

                messagebox.showinfo(
                    "Éxito",
                    f"Base de datos cargada correctamente:\n{filename}",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo copiar el archivo:\n{str(e)}",
                    parent=self
                )


def show_barcode_scanner(parent, row_index, on_product_selected):
    """
    Muestra la ventana de escáner de código de barras.

    Args:
        parent: Ventana padre
        row_index (int): Índice de la fila
        on_product_selected (callable): Callback que recibe (row_index, name, price)
    """
    scanner_window = BarcodeScannerWindow(parent, row_index, on_product_selected)
    return scanner_window
