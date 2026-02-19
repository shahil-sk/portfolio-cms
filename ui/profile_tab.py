from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                                 QLineEdit, QTextEdit, QLabel, QFormLayout, QScrollArea, 
                                 QPushButton, QListWidget, QInputDialog, QMessageBox, QGroupBox)
from models.data_manager import DataManager

class ProfileTab(QWidget):
    def __init__(self, repo_path):
        super().__init__()
        self.repo_path = repo_path
        self.manager = None
        self.data = {}
        
        if repo_path:
            self.manager = DataManager(repo_path)
            self.data = self.manager.load_data()

        self._init_ui()

    def set_repo_path(self, path):
        self.repo_path = path
        self.manager = DataManager(path)
        self.data = self.manager.load_data()
        self._populate_fields()

    def _init_ui(self):
        layout = QVBoxLayout()
        
        # Save Button Area
        top_bar = QHBoxLayout()
        self.save_btn = QPushButton("Save Profile Changes")
        self.save_btn.clicked.connect(self._save_data)
        top_bar.addStretch()
        top_bar.addWidget(self.save_btn)
        layout.addLayout(top_bar)

        # Tabs for sections
        self.tabs = QTabWidget()
        
        self.hero_tab = QWidget()
        self.about_tab = QWidget()
        self.exp_tab = QWidget()
        self.proj_tab = QWidget()
        self.skills_tab = QWidget()
        
        self.tabs.addTab(self.hero_tab, "Hero")
        self.tabs.addTab(self.about_tab, "About")
        self.tabs.addTab(self.exp_tab, "Experience")
        self.tabs.addTab(self.proj_tab, "Projects")
        self.tabs.addTab(self.skills_tab, "Skills")
        
        self._setup_hero()
        self._setup_about()
        self._setup_experience() # Complex list
        self._setup_projects()   # Complex list
        self._setup_skills()     # Dictionary
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
        if self.data:
            self._populate_fields()

    def _setup_hero(self):
        layout = QFormLayout()
        self.hero_name = QLineEdit()
        self.hero_subtitle = QLineEdit()
        self.hero_location = QLineEdit()
        
        layout.addRow("First Name:", self.hero_name)
        layout.addRow("Subtitle:", self.hero_subtitle)
        layout.addRow("Location:", self.hero_location)
        self.hero_tab.setLayout(layout)

    def _setup_about(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Intro Paragraph:"))
        self.about_intro = QTextEdit()
        self.about_intro.setMaximumHeight(100)
        layout.addWidget(self.about_intro)
        
        layout.addWidget(QLabel("Detail Paragraph 1:"))
        self.about_p1 = QTextEdit()
        self.about_p1.setMaximumHeight(100)
        layout.addWidget(self.about_p1)

        layout.addWidget(QLabel("Detail Paragraph 2:"))
        self.about_p2 = QTextEdit()
        self.about_p2.setMaximumHeight(100)
        layout.addWidget(self.about_p2)
        
        self.about_tab.setLayout(layout)

    def _setup_experience(self):
        # Master-Detail view
        layout = QHBoxLayout()
        
        # List
        list_layout = QVBoxLayout()
        self.exp_list = QListWidget()
        self.exp_list.currentItemChanged.connect(self._on_exp_select)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+")
        add_btn.clicked.connect(self._add_exp)
        del_btn = QPushButton("-")
        del_btn.clicked.connect(self._del_exp)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        
        list_layout.addWidget(self.exp_list)
        list_layout.addLayout(btn_layout)
        
        # Form
        self.exp_form = QWidget()
        form_layout = QFormLayout()
        self.exp_company = QLineEdit()
        self.exp_role = QLineEdit()
        self.exp_date = QLineEdit()
        self.exp_highlights = QTextEdit() # Newline separated
        
        form_layout.addRow("Company:", self.exp_company)
        form_layout.addRow("Role:", self.exp_role)
        form_layout.addRow("Date:", self.exp_date)
        form_layout.addRow("Highlights (one per line):", self.exp_highlights)
        
        # Connect updates
        self.exp_company.textChanged.connect(self._update_exp_data)
        self.exp_role.textChanged.connect(self._update_exp_data)
        self.exp_date.textChanged.connect(self._update_exp_data)
        self.exp_highlights.textChanged.connect(self._update_exp_data)
        
        self.exp_form.setLayout(form_layout)
        self.exp_form.setEnabled(False)
        
        layout.addLayout(list_layout, 1)
        layout.addWidget(self.exp_form, 2)
        self.exp_tab.setLayout(layout)

    def _setup_projects(self):
        layout = QHBoxLayout()
        
        # List
        list_layout = QVBoxLayout()
        self.proj_list = QListWidget()
        self.proj_list.currentItemChanged.connect(self._on_proj_select)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+")
        add_btn.clicked.connect(self._add_proj)
        del_btn = QPushButton("-")
        del_btn.clicked.connect(self._del_proj)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        
        list_layout.addWidget(self.proj_list)
        list_layout.addLayout(btn_layout)
        
        # Form
        self.proj_form = QWidget()
        form_layout = QFormLayout()
        self.proj_name = QLineEdit()
        self.proj_desc = QTextEdit()
        self.proj_tech = QLineEdit() # Comma sep
        self.proj_link = QLineEdit()
        
        form_layout.addRow("Name:", self.proj_name)
        form_layout.addRow("Description:", self.proj_desc)
        form_layout.addRow("Tech (comma sep):", self.proj_tech)
        form_layout.addRow("Link:", self.proj_link)
        
        self.proj_name.textChanged.connect(self._update_proj_data)
        self.proj_desc.textChanged.connect(self._update_proj_data)
        self.proj_tech.textChanged.connect(self._update_proj_data)
        self.proj_link.textChanged.connect(self._update_proj_data)
        
        self.proj_form.setLayout(form_layout)
        self.proj_form.setEnabled(False)
        
        layout.addLayout(list_layout, 1)
        layout.addWidget(self.proj_form, 2)
        self.proj_tab.setLayout(layout)

    def _setup_skills(self):
        # Plain text edit for JSON for now to ensure flexibility, or structured? 
        # Structured: Category list -> Item list
        layout = QHBoxLayout()
        
        # Categories
        cat_layout = QVBoxLayout()
        cat_layout.addWidget(QLabel("Categories"))
        self.skill_cats = QListWidget()
        self.skill_cats.currentItemChanged.connect(self._on_skill_cat_select)
        cat_layout.addWidget(self.skill_cats)
        
        # Items
        item_layout = QVBoxLayout()
        item_layout.addWidget(QLabel("Skills (one per line)"))
        self.skill_items = QTextEdit()
        self.skill_items.textChanged.connect(self._update_skill_data)
        item_layout.addWidget(self.skill_items)
        
        layout.addLayout(cat_layout)
        layout.addLayout(item_layout)
        self.skills_tab.setLayout(layout)

    # --- Data Population ---
    def _populate_fields(self):
        if not self.data: return
        
        # Hero
        hero = self.data.get('hero', {})
        self.hero_name.setText(hero.get('firstName', ''))
        self.hero_subtitle.setText(hero.get('subtitle', ''))
        self.hero_location.setText(hero.get('location', ''))
        
        # About
        about = self.data.get('about', {})
        self.about_intro.setText(about.get('intro', ''))
        self.about_p1.setText(about.get('paragraph1', ''))
        self.about_p2.setText(about.get('paragraph2', ''))
        
        # Experience
        self.exp_list.clear()
        exps = self.data.get('experience', [])
        for e in exps:
            self.exp_list.addItem(f"{e.get('company')} - {e.get('role')}")
            
        # Projects
        self.proj_list.clear()
        projs = self.data.get('projects', [])
        for p in projs:
            self.proj_list.addItem(p.get('name'))
            
        # Skills
        self.skill_cats.clear()
        skills = self.data.get('skills', {})
        for cat in skills.keys():
            self.skill_cats.addItem(cat)

    # --- Event Handlers ---
    def _on_exp_select(self, current, prev):
        if not current: 
            self.exp_form.setEnabled(False)
            return
        self.exp_form.setEnabled(True)
        idx = self.exp_list.row(current)
        if idx < len(self.data.get('experience', [])):
            exp = self.data['experience'][idx]
            self.exp_company.blockSignals(True)
            self.exp_company.setText(exp.get('company', ''))
            self.exp_company.blockSignals(False)
            
            self.exp_role.blockSignals(True)
            self.exp_role.setText(exp.get('role', ''))
            self.exp_role.blockSignals(False)

            self.exp_date.blockSignals(True)
            self.exp_date.setText(exp.get('date', ''))
            self.exp_date.blockSignals(False)
            
            self.exp_highlights.blockSignals(True)
            self.exp_highlights.setPlainText('\n'.join(exp.get('highlights', [])))
            self.exp_highlights.blockSignals(False)

    def _update_exp_data(self):
        idx = self.exp_list.currentRow()
        if idx < 0: return
        
        highlights = [line for line in self.exp_highlights.toPlainText().split('\n') if line.strip()]
        
        self.data['experience'][idx] = {
            'company': self.exp_company.text(),
            'role': self.exp_role.text(),
            'date': self.exp_date.text(),
            'highlights': highlights
        }
        item = self.exp_list.item(idx)
        item.setText(f"{self.exp_company.text()} - {self.exp_role.text()}")

    def _add_exp(self):
        new_exp = {'company': 'New Company', 'role': 'Role', 'date': '', 'highlights': []}
        if 'experience' not in self.data: self.data['experience'] = []
        self.data['experience'].append(new_exp)
        self.exp_list.addItem("New Company - Role")
        self.exp_list.setCurrentRow(len(self.data['experience']) - 1)

    def _del_exp(self):
        row = self.exp_list.currentRow()
        if row >= 0:
            self.data['experience'].pop(row)
            self.exp_list.takeItem(row)

    # Projects Handlers (Simplified for brevity, similar logic)
    def _on_proj_select(self, current, prev):
        if not current: return
        self.proj_form.setEnabled(True)
        idx = self.proj_list.row(current)
        proj = self.data['projects'][idx]
        
        self.proj_name.blockSignals(True)
        self.proj_name.setText(proj.get('name', ''))
        self.proj_name.blockSignals(False)
        
        self.proj_desc.blockSignals(True)
        self.proj_desc.setPlainText(proj.get('description', ''))
        self.proj_desc.blockSignals(False)

        self.proj_tech.blockSignals(True)
        self.proj_tech.setText(", ".join(proj.get('tech', [])))
        self.proj_tech.blockSignals(False)
        
        self.proj_link.blockSignals(True)
        self.proj_link.setText(proj.get('link', ''))
        self.proj_link.blockSignals(False)

    def _update_proj_data(self):
        idx = self.proj_list.currentRow()
        if idx < 0: return
        
        tech = [t.strip() for t in self.proj_tech.text().split(',') if t.strip()]
        
        self.data['projects'][idx] = {
            'name': self.proj_name.text(),
            'description': self.proj_desc.toPlainText(),
            'tech': tech,
            'link': self.proj_link.text(),
            'stars': self.data['projects'][idx].get('stars', 0)
        }
        item = self.proj_list.item(idx)
        item.setText(self.proj_name.text())

    def _add_proj(self):
        new_proj = {'name': 'New Project', 'description': '', 'tech': [], 'link': ''}
        if 'projects' not in self.data: self.data['projects'] = []
        self.data['projects'].append(new_proj)
        self.proj_list.addItem("New Project")
        self.proj_list.setCurrentRow(len(self.data['projects']) - 1)

    def _del_proj(self):
        row = self.proj_list.currentRow()
        if row >= 0:
            self.data['projects'].pop(row)
            self.proj_list.takeItem(row)

    # Skills Handlers
    def _on_skill_cat_select(self, current, prev):
        if not current: return
        cat = current.text()
        skills = self.data.get('skills', {}).get(cat, [])
        self.skill_items.blockSignals(True)
        self.skill_items.setPlainText('\n'.join(skills))
        self.skill_items.blockSignals(False)

    def _update_skill_data(self):
        item = self.skill_cats.currentItem()
        if not item: return
        cat = item.text()
        skills = [line.strip() for line in self.skill_items.toPlainText().split('\n') if line.strip()]
        self.data['skills'][cat] = skills

    def _save_data(self):
        # Update Hero/About from fields before saving
        if 'hero' not in self.data: self.data['hero'] = {}
        self.data['hero']['firstName'] = self.hero_name.text()
        self.data['hero']['subtitle'] = self.hero_subtitle.text()
        self.data['hero']['location'] = self.hero_location.text()
        
        if 'about' not in self.data: self.data['about'] = {}
        self.data['about']['intro'] = self.about_intro.toPlainText()
        self.data['about']['paragraph1'] = self.about_p1.toPlainText()
        self.data['about']['paragraph2'] = self.about_p2.toPlainText()
        
        success, msg = self.manager.save_data(self.data)
        if success:
            QMessageBox.information(self, "Saved", "Profile data saved successfully!")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save: {msg}")
