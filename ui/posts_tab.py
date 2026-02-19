from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                                 QLineEdit, QTextEdit, QPushButton, QLabel, QSplitter, 
                                 QMessageBox, QInputDialog)
from PySide6.QtCore import Qt, QProcess
from models.post_manager import PostManager

class PostsTab(QWidget):
    def __init__(self, repo_path):
        super().__init__()
        self.repo_path = repo_path
        self.manager = None
        self.current_file = None
        
        self._init_ui()
        if repo_path:
            self.set_repo_path(repo_path)

    def _init_ui(self):
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        
        # Left Pane: List & Actions
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.new_btn = QPushButton("New Post")
        self.new_btn.clicked.connect(self._new_post)
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self._refresh_list)
        
        self.post_list = QListWidget()
        self.post_list.currentItemChanged.connect(self._on_post_selected)
        
        self.build_btn = QPushButton("Run Build Script")
        self.build_btn.clicked.connect(self._run_build)
        
        left_layout.addWidget(self.new_btn)
        left_layout.addWidget(self.refresh_btn)
        left_layout.addWidget(self.post_list)
        left_layout.addWidget(self.build_btn)
        
        # Right Pane: Editor
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Select a post to edit...")
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self._save_current)
        
        right_layout.addWidget(QLabel("Markdown Editor"))
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.save_btn)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def set_repo_path(self, path):
        self.repo_path = path
        self.manager = PostManager(path)
        self._refresh_list()

    def _refresh_list(self):
        if not self.manager: return
        self.post_list.clear()
        posts = self.manager.get_posts()
        for p in posts:
            self.post_list.addItem(f"{p['title']} ({p['filename']})")
        
        # Store data in items if needed, or look up by index
        self.posts_data = posts

    def _on_post_selected(self, current, previous):
        if not current: return
        row = self.post_list.row(current)
        post = self.posts_data[row]
        self.current_file = post['filename']
        self.editor.setPlainText(post['content'])

    def _save_current(self):
        if not self.current_file or not self.manager: return
        content = self.editor.toPlainText()
        self.manager.save_post(self.current_file, content)
        QMessageBox.information(self, "Saved", f"{self.current_file} saved successfully.")

    def _new_post(self):
        if not self.manager: return
        title, ok = QInputDialog.getText(self, "New Post", "Enter post title:")
        if ok and title:
            filename = self.manager.create_post(title)
            self._refresh_list()
            QMessageBox.information(self, "Created", f"Created {filename}")

    def _run_build(self):
        if not self.repo_path: return
        script = os.path.join(self.repo_path, 'scripts', 'manage_posts.py')
        
        self.process = QProcess()
        self.process.setWorkingDirectory(self.repo_path)
        self.process.start("python3", [script, "build"])
        self.process.finished.connect(lambda: QMessageBox.information(self, "Build", "Build process finished!"))
