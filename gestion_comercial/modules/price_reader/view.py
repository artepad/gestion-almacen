"""
Vista del lector de precios.
Permite consultar precios mediante escáner de código de barras con dos modos:
- Modo normal: interfaz completa con controles
- Modo pantalla completa: solo muestra precio y nombre (uso público)
"""

import tkinter as tk
from gestion_comercial.config.theme import Theme
from gestion_comercial.modules.tag_manager.database import ProductDatabase


class PriceReaderView(tk.Frame):
    def __init__(self, parent, navigator):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self.navigator = navigator
        self.fullscreen_mode = False
        self.auto_clear_timer = None

        # Binding global para F5 (toggle pantalla completa)
        self.bind_all('<F5>', self.toggle_fullscreen)
        self.bind_all('<Escape>', self.exit_fullscreen)

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz según el modo actual."""
        if self.fullscreen_mode:
            self.create_fullscreen_ui()
        else:
            self.create_normal_ui()

    def create_normal_ui(self):
        """Crea la interfaz en modo normal."""
        # Top green accent strip
        self.create_top_accent()

        # Header
        self.create_header()

        # Container principal
        main_container = tk.Frame(self, bg=Theme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=40, pady=20)

        # Instrucciones
        tk.Label(
            main_container,
            text="Escanea el código de barras del producto para consultar su precio",
            font=(Theme.FONT_FAMILY, 12),
            bg=Theme.BACKGROUND,
            fg='#6c757d'
        ).pack(pady=(0, 20))

        # Campo de entrada
        input_frame = tk.Frame(main_container, bg=Theme.BACKGROUND)
        input_frame.pack(fill='x', pady=(0, 25))

        tk.Label(
            input_frame,
            text="Código de barras:",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 5))

        self.barcode_entry = tk.Entry(
            input_frame,
            font=(Theme.FONT_FAMILY, 13),
            bg='white',
            fg=Theme.TEXT_PRIMARY,
            bd=0,
            relief='flat',
            highlightthickness=2,
            highlightcolor='#2ecc71',
            highlightbackground='#2ecc71'
        )
        self.barcode_entry.pack(fill='x', ipady=8)
        self.barcode_entry.bind('<Return>', self.search_product)
        self.barcode_entry.focus_set()

        # Área de resultados
        self.result_frame = tk.LabelFrame(
            main_container,
            text="📊 Información del Producto",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='#f8f9fa',
            fg='#495057',
            padx=25,
            pady=15
        )
        self.result_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Mensaje inicial
        self.result_content = tk.Frame(self.result_frame, bg='#f8f9fa')
        self.result_content.pack(fill='both', expand=True)

        self.show_initial_message()

        # Información de base de datos
        self.create_db_info_section(main_container)

        # Botones inferiores
        self.create_bottom_buttons(main_container)

        # Bottom blue accent strip
        self.create_bottom_accent()

    def create_fullscreen_ui(self):
        """Crea la interfaz en modo pantalla completa."""
        # Configurar ventana principal en pantalla completa
        root = self.winfo_toplevel()
        root.attributes('-fullscreen', True)

        # Container principal centrado
        main_container = tk.Frame(self, bg='#f0f4f8')
        main_container.pack(fill='both', expand=True)

        # Frame centrado verticalmente
        center_frame = tk.Frame(main_container, bg='#f0f4f8')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Instrucciones iniciales
        self.instruction_label = tk.Label(
            center_frame,
            text="Escanea el código de barras del producto",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='#f0f4f8',
            fg='#495057'
        )
        self.instruction_label.pack(pady=(0, 30))

        # Icono de escáner
        self.scanner_icon = tk.Label(
            center_frame,
            text="📊",
            font=(Theme.FONT_FAMILY, 80),
            bg='#f0f4f8'
        )
        self.scanner_icon.pack(pady=20)

        # Nombre del producto (oculto inicialmente)
        self.product_name_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 32, 'bold'),
            bg='#f0f4f8',
            fg='#2c3e50',
            wraplength=900
        )

        # Precio del producto (oculto inicialmente)
        self.product_price_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 120, 'bold'),
            bg='#f0f4f8',
            fg='#27ae60'
        )

        # Mensaje de error (oculto inicialmente)
        self.error_label = tk.Label(
            center_frame,
            text="",
            font=(Theme.FONT_FAMILY, 28, 'bold'),
            bg='#f0f4f8',
            fg='#e74c3c',
            wraplength=800
        )

        # Campo de entrada invisible pero funcional
        self.barcode_entry = tk.Entry(
            center_frame,
            font=(Theme.FONT_FAMILY, 1),
            bg='#f0f4f8',
            fg='#f0f4f8',
            bd=0,
            highlightthickness=0,
            insertwidth=0
        )
        self.barcode_entry.pack()
        self.barcode_entry.bind('<Return>', self.search_product)
        self.barcode_entry.focus_set()

        # Indicador de modo (esquina superior derecha)
        mode_label = tk.Label(
            main_container,
            text="Modo Pantalla Completa | F5: Salir",
            font=(Theme.FONT_FAMILY, 10),
            bg='#f0f4f8',
            fg='#95a5a6'
        )
        mode_label.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

    def create_top_accent(self):
        """Crea la franja verde superior."""
        accent_frame = tk.Frame(self, bg='#2ecc71', height=5)
        accent_frame.pack(fill='x')
        accent_frame.pack_propagate(False)

    def create_bottom_accent(self):
        """Crea la franja azul inferior."""
        accent_frame = tk.Frame(self, bg=Theme.TOTAL_FG, height=5)
        accent_frame.pack(side='bottom', fill='x')
        accent_frame.pack_propagate(False)

    def create_header(self):
        """Crea el header en modo normal."""
        header_frame = tk.Frame(self, bg=Theme.TEXT_PRIMARY, height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        content_container = tk.Frame(header_frame, bg=Theme.TEXT_PRIMARY)
        content_container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(
            content_container,
            text="Lector de Precios",
            font=(Theme.FONT_FAMILY, 20, 'bold'),
            bg=Theme.TEXT_PRIMARY,
            fg='white'
        ).pack()

    def create_bottom_buttons(self, parent):
        """Crea los botones en la parte inferior."""
        button_container = tk.Frame(parent, bg=Theme.BACKGROUND)
        button_container.pack(fill='x', pady=(15, 0))

        # Container centrado para los botones
        buttons_center = tk.Frame(button_container, bg=Theme.BACKGROUND)
        buttons_center.pack(anchor='center')

        # Botón Volver
        back_button = tk.Button(
            buttons_center,
            text="⬅ Volver",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.TOTAL_FG,
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=lambda: self.navigator.show_view('launcher')
        )
        back_button.pack(side='left', padx=(0, 10))

        def on_back_enter(e):
            back_button.config(bg='#1565c0')

        def on_back_leave(e):
            back_button.config(bg=Theme.TOTAL_FG)

        back_button.bind('<Enter>', on_back_enter)
        back_button.bind('<Leave>', on_back_leave)

        # Botón Pantalla Completa
        fullscreen_button = tk.Button(
            buttons_center,
            text="Pantalla Completa",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg=Theme.BILLS_FG,
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.toggle_fullscreen
        )
        fullscreen_button.pack(side='left', padx=(10, 0))

        def on_full_enter(e):
            fullscreen_button.config(bg='#1e7e34')

        def on_full_leave(e):
            fullscreen_button.config(bg=Theme.BILLS_FG)

        fullscreen_button.bind('<Enter>', on_full_enter)
        fullscreen_button.bind('<Leave>', on_full_leave)

    def create_db_info_section(self, parent):
        """Crea la sección de información de la base de datos."""
        info_frame = tk.LabelFrame(
            parent,
            text="💾 Información de Base de Datos",
            font=(Theme.FONT_FAMILY, 11, 'bold'),
            bg='white',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            padx=20,
            pady=15
        )
        info_frame.pack(fill='x', pady=(15, 0))

        # Obtener información de la BD
        db_info = ProductDatabase.get_database_info()

        if db_info['exists']:
            # Estado de conexión
            status_container = tk.Frame(info_frame, bg='white')
            status_container.pack(fill='x', pady=(0, 10))

            tk.Label(
                status_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                status_container,
                text="Conectada",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#28a745'
            ).pack(side='left', padx=(10, 0))

            # Última actualización
            update_container = tk.Frame(info_frame, bg='white')
            update_container.pack(fill='x', pady=(0, 10))

            tk.Label(
                update_container,
                text="Última actualización:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                update_container,
                text=db_info['last_modified'],
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(side='left', padx=(10, 0))

            # Productos disponibles
            products_container = tk.Frame(info_frame, bg='white')
            products_container.pack(fill='x')

            tk.Label(
                products_container,
                text="Productos disponibles:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                products_container,
                text=str(db_info['total_products']),
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(side='left', padx=(10, 0))
        else:
            # Mensaje de error
            error_container = tk.Frame(info_frame, bg='white')
            error_container.pack(fill='x', pady=(0, 8))

            tk.Label(
                error_container,
                text="Estado:",
                font=(Theme.FONT_FAMILY, 10),
                bg='white',
                fg='#495057'
            ).pack(side='left')

            tk.Label(
                error_container,
                text="✗ No disponible",
                font=(Theme.FONT_FAMILY, 10, 'bold'),
                bg='white',
                fg='#dc3545'
            ).pack(side='left', padx=(10, 0))

            # Instrucción
            tk.Label(
                info_frame,
                text="Por favor, configura la base de datos desde el Gestor de Etiquetas",
                font=(Theme.FONT_FAMILY, 9),
                bg='white',
                fg='#6c757d',
                wraplength=600,
                justify='left'
            ).pack(fill='x')

    def show_initial_message(self):
        """Muestra el mensaje inicial en el área de resultados."""
        # Limpiar contenido anterior
        for widget in self.result_content.winfo_children():
            widget.destroy()

        # Mensaje de espera
        tk.Label(
            self.result_content,
            text="🔍",
            font=(Theme.FONT_FAMILY, 50),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack(pady=(20, 10))

        tk.Label(
            self.result_content,
            text="Esperando escaneo...",
            font=(Theme.FONT_FAMILY, 13),
            bg='#f8f9fa',
            fg='#6c757d'
        ).pack()

    def show_product_info(self, product_data):
        """Muestra la información del producto encontrado."""
        if self.fullscreen_mode:
            # Ocultar elementos iniciales
            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.error_label.pack_forget()

            # Mostrar nombre y precio
            self.product_name_label.config(text=product_data['name'])
            self.product_name_label.pack(pady=(0, 20))

            price_text = f"${self.format_price(product_data['price'])}"
            self.product_price_label.config(text=price_text)
            self.product_price_label.pack(pady=10)

            # Auto-limpiar después de 5 segundos
            self.schedule_auto_clear()
        else:
            # Limpiar contenido anterior
            for widget in self.result_content.winfo_children():
                widget.destroy()

            # Mostrar información del producto
            tk.Label(
                self.result_content,
                text="✓ Producto Encontrado",
                font=(Theme.FONT_FAMILY, 12, 'bold'),
                bg='#f8f9fa',
                fg='#28a745'
            ).pack(pady=(8, 15))

            # Nombre del producto
            tk.Label(
                self.result_content,
                text="Producto:",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='#f8f9fa',
                fg='#495057',
                anchor='w'
            ).pack(fill='x', pady=(0, 3))

            tk.Label(
                self.result_content,
                text=product_data['name'],
                font=(Theme.FONT_FAMILY, 12),
                bg='#f8f9fa',
                fg=Theme.TEXT_PRIMARY,
                anchor='w',
                wraplength=650
            ).pack(fill='x', pady=(0, 12))

            # Precio
            tk.Label(
                self.result_content,
                text="Precio:",
                font=(Theme.FONT_FAMILY, 9, 'bold'),
                bg='#f8f9fa',
                fg='#495057',
                anchor='w'
            ).pack(fill='x', pady=(0, 3))

            price_text = f"${self.format_price(product_data['price'])}"
            tk.Label(
                self.result_content,
                text=price_text,
                font=(Theme.FONT_FAMILY, 32, 'bold'),
                bg='#f8f9fa',
                fg='#27ae60',
                anchor='w'
            ).pack(fill='x', pady=(0, 8))

    def show_error_message(self, error_msg):
        """Muestra un mensaje de error."""
        if self.fullscreen_mode:
            # Ocultar elementos
            self.instruction_label.pack_forget()
            self.scanner_icon.pack_forget()
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()

            # Mostrar error
            self.error_label.config(text=f"✗ {error_msg}")
            self.error_label.pack(pady=20)

            # Auto-limpiar después de 5 segundos
            self.schedule_auto_clear()
        else:
            # Limpiar contenido anterior
            for widget in self.result_content.winfo_children():
                widget.destroy()

            # Mostrar error
            tk.Label(
                self.result_content,
                text="✗",
                font=(Theme.FONT_FAMILY, 50),
                bg='#f8f9fa',
                fg='#dc3545'
            ).pack(pady=(20, 10))

            tk.Label(
                self.result_content,
                text=error_msg,
                font=(Theme.FONT_FAMILY, 13),
                bg='#f8f9fa',
                fg='#dc3545',
                wraplength=600
            ).pack(pady=(0, 20))

    def search_product(self, event=None):
        """Busca el producto en la base de datos."""
        barcode = self.barcode_entry.get().strip()

        if not barcode:
            return

        # Buscar en la base de datos
        success, result = ProductDatabase.search_product(barcode)

        if success:
            self.show_product_info(result)
        else:
            self.show_error_message(result)

        # Limpiar campo de entrada
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus_set()

    def schedule_auto_clear(self):
        """Programa la limpieza automática de la pantalla."""
        # Cancelar timer anterior si existe
        if self.auto_clear_timer:
            self.after_cancel(self.auto_clear_timer)

        # Programar nueva limpieza en 5 segundos
        self.auto_clear_timer = self.after(5000, self.clear_fullscreen_display)

    def clear_fullscreen_display(self):
        """Limpia la pantalla en modo fullscreen."""
        if self.fullscreen_mode:
            # Ocultar todo
            self.product_name_label.pack_forget()
            self.product_price_label.pack_forget()
            self.error_label.pack_forget()

            # Mostrar estado inicial
            self.instruction_label.pack(pady=(0, 30))
            self.scanner_icon.pack(pady=20)

            # Mantener focus en entrada
            self.barcode_entry.focus_set()

    def toggle_fullscreen(self, event=None):
        """Alterna entre modo normal y pantalla completa."""
        self.fullscreen_mode = not self.fullscreen_mode

        # Limpiar interfaz actual
        for widget in self.winfo_children():
            widget.destroy()

        # Recrear interfaz
        self.setup_ui()

    def exit_fullscreen(self, event=None):
        """Sale del modo pantalla completa."""
        if self.fullscreen_mode:
            self.fullscreen_mode = False

            # Restaurar ventana normal
            root = self.winfo_toplevel()
            root.attributes('-fullscreen', False)

            # Limpiar y recrear interfaz
            for widget in self.winfo_children():
                widget.destroy()

            self.setup_ui()

    def format_price(self, price):
        """Formatea el precio con separadores de miles."""
        return f"{int(price):,}".replace(',', '.')
