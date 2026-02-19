from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                                 QPushButton, QTextEdit, QLabel, QSplitter, QMessageBox, 
                                 QGroupBox)
from PySide6.QtCore import Qt, QTimer
from models.git_manager import GitManager

class GitTab(QWidget):
    def __init__(self, repo_path):
        super().__init__()
        self.repo_path = repo_path
        self.manager = None
        if repo_path:
            self.manager = GitManager(repo_path)
            
        self._init_ui()
        self._refresh_status()

    def set_repo_path(self, path):
        self.repo_path = path
        self.manager = GitManager(path)
        self._refresh_status()

    def _init_ui(self):
        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # Left: Staging Area
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Unstaged Files
        unstaged_group = QGroupBox("Unstaged Changes")
        u_layout = QVBoxLayout()
        self.unstaged_list = QListWidget()
        self.unstaged_list.itemClicked.connect(self._on_unstaged_select)
        self.stage_btn = QPushButton("Stage Selected")
        self.stage_btn.clicked.connect(self._stage_selected)
        u_layout.addWidget(self.unstaged_list)
        u_layout.addWidget(self.stage_btn)
        unstaged_group.setLayout(u_layout)

        # Staged Files
        staged_group = QGroupBox("Staged Changes (Ready to Commit)")
        s_layout = QVBoxLayout()
        self.staged_list = QListWidget()
        self.staged_list.itemClicked.connect(self._on_staged_select)
        self.unstage_btn = QPushButton("Unstage Selected")
        self.unstage_btn.clicked.connect(self._unstage_selected)
        s_layout.addWidget(self.staged_list)
        s_layout.addWidget(self.unstage_btn)
        staged_group.setLayout(s_layout)

        left_layout.addWidget(unstaged_group)
        left_layout.addWidget(staged_group)

        # Right: Diff & Commit
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.diff_view = QTextEdit()
        self.diff_view.setReadOnly(True)
        self.diff_view.setPlaceholderText("Select a file to view diff...")

        commit_group = QGroupBox("Commit")
        c_layout = QVBoxLayout()
        self.commit_msg = QTextEdit()
        self.commit_msg.setPlaceholderText("Commit message...")
        self.commit_msg.setMaximumHeight(100)
        
        btn_layout = QHBoxLayout()
        self.commit_btn = QPushButton("Commit")
        self.commit_btn.clicked.connect(self._commit)
        self.push_btn = QPushButton("Push to Origin")
        self.push_btn.clicked.connect(self._push)
        self.pull_btn = QPushButton("Pull")
        self.pull_btn.clicked.connect(self._pull)
        
        btn_layout.addWidget(self.pull_btn)
        btn_layout.addWidget(self.commit_btn)
        btn_layout.addWidget(self.push_btn)
        
        c_layout.addWidget(self.commit_msg)
        c_layout.addLayout(btn_layout)
        commit_group.setLayout(c_layout)

        right_layout.addWidget(QLabel("Diff View"))
        right_layout.addWidget(self.diff_view)
        right_layout.addWidget(commit_group)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Timer to auto-refresh status periodically or after actions
        self.refresh_btn = QPushButton("Refresh Status")
        self.refresh_btn.clicked.connect(self._refresh_status)
        left_layout.insertWidget(0, self.refresh_btn)

    def _refresh_status(self):
        if not self.manager: return
        self.unstaged_list.clear()
        self.staged_list.clear()
        
        staged, unstaged = self.manager.get_status()
        
        for item in unstaged:
            self.unstaged_list.addItem(f"{item['status']} {item['path']}")
        
        for item in staged:
            self.staged_list.addItem(f"{item['status']} {item['path']}")

    def _on_unstaged_select(self, item):
        path = item.text().split(' ', 1)[1]
        diff = self.manager.get_diff(filepath=path, staged=False)
        self.diff_view.setPlainText(diff)

    def _on_staged_select(self, item):
        path = item.text().split(' ', 1)[1]
        diff = self.manager.get_diff(filepath=path, staged=True)
        self.diff_view.setPlainText(diff)

    def _stage_selected(self):
        item = self.unstaged_list.currentItem()
        if not item: return
        path = item.text().split(' ', 1)[1]
        self.manager.stage_file(path)
        self._refresh_status()

    def _unstage_selected(self):
        item = self.staged_list.currentItem()
        if not item: return
        path = item.text().split(' ', 1)[1]
        self.manager.unstage_file(path)
        self._refresh_status()

    def _commit(self):
        msg = self.commit_msg.toPlainText().strip()
        if not msg:
            QMessageBox.warning(self, "Error", "Commit message cannot be empty")
            return
        self.manager.commit(msg)
        self.commit_msg.clear()
        self._refresh_status()
        QMessageBox.information(self, "Success", "Committed successfully")

    def _push(self):
        QMessageBox.information(self, "Pushing", "Pushing to remote... This might take a moment.")
        out, err = self.manager.push()
        if err:
            QMessageBox.warning(self, "Git Output", f"{out}\n{err}")
        else:
            QMessageBox.information(self, "Success", "Pushed successfully")

    def _pull(self):
        QMessageBox.information(self, "Pulling", "Pulling from remote...")
        out, err = self.manager.pull()
        self._refresh_status()
        QMessageBox.information(self, "Git Output", f"{out}\n{err}")
