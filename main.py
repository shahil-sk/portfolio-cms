import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("shahil-sk.github.io CMS")
    
    # Pass app instance to MainWindow so it can set the theme
    window = MainWindow(app)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
