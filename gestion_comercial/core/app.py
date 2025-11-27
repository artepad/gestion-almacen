import tkinter as tk
from gestion_comercial.config.settings import Settings
from gestion_comercial.config.theme import Theme
from gestion_comercial.core.navigation import Navigator

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(Settings.APP_NAME)
        self.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}")
        
        if not Settings.RESIZABLE:
            self.resizable(False, False)
            
        self.configure(bg=Theme.BACKGROUND)
        
        # Center window
        self._center_window()
        
        # Main container for views
        self.container = tk.Frame(self, bg=Theme.BACKGROUND)
        self.container.pack(fill='both', expand=True)
        
        # Initialize Navigator
        self.navigator = Navigator(self.container)
        
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
