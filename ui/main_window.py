from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QMessageBox, QFileDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout
from ui.posts_tab import PostsTab
from ui.git_tab import GitTab
from ui.profile_tab import ProfileTab
from utils.settings import SettingsManager
from utils.theme import apply_dark_theme # Import theme
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("shahil-sk.github.io CMS")
        self.resize(1200, 800)
        
        # Apply Theme
        apply_dark_theme(self.app_instance) 

        self.settings_manager = SettingsManager()
        self.repo_path = self.settings_manager.get_repo_path()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Tabs
        self.profile_tab = ProfileTab(self.repo_path)
        self.posts_tab = PostsTab(self.repo_path)
        self.git_tab = GitTab(self.repo_path)
        self.settings_tab = QWidget()
        self._setup_settings_tab()
        
        self.tabs.addTab(self.profile_tab, "Profile")
        self.tabs.addTab(self.posts_tab, "Posts")
        self.tabs.addTab(self.git_tab, "Git Version Control")
        self.tabs.addTab(self.settings_tab, "Settings")
        
        if not self.repo_path:
            QMessageBox.warning(self, "Setup Required", "Please select your website repository path in Settings.")
            self.tabs.setCurrentIndex(3)

    def _setup_settings_tab(self):
        layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(self.repo_path)
        self.path_input.setReadOnly(True)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_repo)
        
        path_layout.addWidget(QLabel("Repository Path:"))
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        layout.addStretch()
        self.settings_tab.setLayout(layout)

    def _browse_repo(self):
        path = QFileDialog.getExistingDirectory(self, "Select Repository")
        if path:
            self.path_input.setText(path)
            self.repo_path = path
            self.settings_manager.save_settings({"repo_path": path})
            
            # Update all tabs
            self.profile_tab.set_repo_path(path)
            self.posts_tab.set_repo_path(path)
            self.git_tab.set_repo_path(path)
