import json
import os
from PySide6.QtCore import QStandardPaths

class SettingsManager:
    def __init__(self):
        self.config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        self.config_file = os.path.join(self.config_dir, 'config.json')
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
    def load_settings(self):
        if not os.path.exists(self.config_file):
            return {"repo_path": ""}
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {"repo_path": ""}

    def save_settings(self, settings):
        with open(self.config_file, 'w') as f:
            json.dump(settings, f, indent=4)
            
    def get_repo_path(self):
        return self.load_settings().get("repo_path", "")
