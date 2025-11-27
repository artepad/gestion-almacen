import sys
import os

# Add the current directory to sys.path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from gestion_comercial.core.app import MainApp
# Import views to register them (will be added later)
from gestion_comercial.modules.launcher.view import LauncherView
from gestion_comercial.modules.cash_counter.view import CashCounterView
from gestion_comercial.modules.tag_manager.view import TagManagerView

def main():
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
