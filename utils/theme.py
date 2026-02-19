from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

def apply_dark_theme(app):
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    app.setPalette(palette)
    
    # Additional styling for specific widgets
    app.setStyleSheet("""
        QToolTip { 
            color: #ffffff; 
            background-color: #2a82da; 
            border: 1px solid white; 
        }
        QTextEdit, QPlainTextEdit, QListWidget {
            background-color: #1e1e1e;
            color: #dcdcdc;
            border: 1px solid #3e3e3e;
        }
        QPushButton {
            background-color: #3e3e3e;
            border: 1px solid #5e5e5e;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #4e4e4e;
        }
        QPushButton:pressed {
            background-color: #2e2e2e;
        }
        QHeaderView::section {
            background-color: #3e3e3e;
            color: white;
        }
        QLineEdit {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #3e3e3e;
            padding: 3px;
        }
    """)
