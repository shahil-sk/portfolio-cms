from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                                 QLineEdit, QTextEdit, QPushButton, QLabel, QSplitter, 
                                 QMessageBox, QInputDialog, QFileDialog, QTextBrowser)
from PySide6.QtCore import Qt, QProcess, QTimer
from models.post_manager import PostManager
import markdown
import os

class PostsTab(QWidget):
    def __init__(self, repo_path):
        super().__init__()
        self.repo_path = repo_path
        self.manager = None
        self.current_file = None
        
        self._init_ui()
        if repo_path:
            self.set_repo_path(repo_path)

        # Debounce preview updates
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._update_preview)

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
        self.build_btn.setStyleSheet("background-color: #2a82da; font-weight: bold;")
        
        left_layout.addWidget(self.new_btn)
        left_layout.addWidget(self.refresh_btn)
        left_layout.addWidget(self.post_list)
        left_layout.addWidget(self.build_btn)
        
        # Right Pane: Editor & Preview
        right_splitter = QSplitter(Qt.Vertical)
        
        # Editor Top Bar
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_toolbar = QHBoxLayout()
        
        self.img_btn = QPushButton("Insert Image")
        self.img_btn.clicked.connect(self._insert_image)
        self.save_btn = QPushButton("Save (Ctrl+S)")
        self.save_btn.clicked.connect(self._save_current)
        self.save_btn.setShortcut("Ctrl+S")
        
        editor_toolbar.addWidget(QLabel("Markdown Editor"))
        editor_toolbar.addStretch()
        editor_toolbar.addWidget(self.img_btn)
        editor_toolbar.addWidget(self.save_btn)
        
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Select a post to edit...")
        self.editor.textChanged.connect(self._on_text_changed)
        
        editor_layout.addLayout(editor_toolbar)
        editor_layout.addWidget(self.editor)
        
        # Preview Pane
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.addWidget(QLabel("Live Preview"))
        
        self.preview = QTextBrowser()
        self.preview.setOpenExternalLinks(True)
        preview_layout.addWidget(self.preview)
        
        right_splitter.addWidget(editor_widget)
        right_splitter.addWidget(preview_widget)
        right_splitter.setStretchFactor(0, 1)
        right_splitter.setStretchFactor(1, 1)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_splitter)
        splitter.setStretchFactor(1, 3)
        
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
        self.posts_data = posts

    def _on_post_selected(self, current, previous):
        if not current: return
        row = self.post_list.row(current)
        post = self.posts_data[row]
        self.current_file = post['filename']
        self.editor.blockSignals(True)
        self.editor.setPlainText(post['content'])
        self.editor.blockSignals(False)
        self._update_preview()

    def _on_text_changed(self):
        # Debounce preview update (300ms)
        self.timer.start(300)

    def _update_preview(self):
        text = self.editor.toPlainText()
        # Convert MD to HTML with extensions
        html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        
        # Basic CSS to mimic site roughly
        style = """
        <style>
            body { font-family: sans-serif; color: #333; line-height: 1.6; }
            h1, h2, h3 { color: #2a82da; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
            img { max-width: 100%; border-radius: 5px; }
            blockquote { border-left: 4px solid #ddd; padding-left: 10px; color: #666; }
        </style>
        """
        # Dark mode adjust for preview if needed, but white paper look is often better for preview
        if self.parent() and "Dark" in str(self.parent()): # simplistic check
             style = """
            <style>
                body { font-family: sans-serif; color: #e0e0e0; background-color: #1e1e1e; line-height: 1.6; }
                h1, h2, h3 { color: #5aaaf0; }
                code { background: #2d2d2d; padding: 2px 5px; border-radius: 3px; color: #f0f0f0; }
                pre { background: #2d2d2d; padding: 10px; border-radius: 5px; }
                a { color: #5aaaf0; }
                img { max-width: 100%; border-radius: 5px; }
            </style>
            """
            
        self.preview.setHtml(style + html)

    def _save_current(self):
        if not self.current_file or not self.manager: return
        content = self.editor.toPlainText()
        self.manager.save_post(self.current_file, content)
        # Show mini status msg instead of popup?
        self.save_btn.setText("Saved!")
        QTimer.singleShot(2000, lambda: self.save_btn.setText("Save (Ctrl+S)"))

    def _new_post(self):
        if not self.manager: return
        title, ok = QInputDialog.getText(self, "New Post", "Enter post title:")
        if ok and title:
            filename = self.manager.create_post(title)
            self._refresh_list()
            # Select the new item
            items = self.post_list.findItems(f"{title} ({filename})", Qt.MatchContains)
            if items:
                self.post_list.setCurrentItem(items[0])

    def _insert_image(self):
        if not self.repo_path: return
        img_dir = os.path.join(self.repo_path, 'content', 'images')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
            
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", img_dir, "Images (*.png *.jpg *.jpeg *.gif *.webp)")
        if path:
            # Copy if not in repo? Or just ref.
            # Assuming user picks from content/images or we convert path to relative
            rel_path = os.path.relpath(path, os.path.join(self.repo_path, 'content', 'posts'))
            # If outside, maybe warn?
            
            # Insert Markdown: ![name](path)
            name = os.path.basename(path)
            # Fix slash for markdown
            rel_path = rel_path.replace("\\", "/")
            
            cursor = self.editor.textCursor()
            cursor.insertText(f"![{name}]({rel_path})")

    def _run_build(self):
        if not self.repo_path: return
        script = os.path.join(self.repo_path, 'scripts', 'manage_posts.py')
        
        self.process = QProcess()
        self.process.setWorkingDirectory(self.repo_path)
        self.process.start("python3", [script, "build"])
        self.process.finished.connect(lambda: QMessageBox.information(self, "Build", "Build script finished! Check output."))
