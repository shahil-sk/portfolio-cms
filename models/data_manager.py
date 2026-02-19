import json
import os
import shutil

class DataManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.data_file = os.path.join(repo_path, 'data.json')
        self.backup_file = os.path.join(repo_path, 'data.json.bak')

    def load_data(self):
        if not os.path.exists(self.data_file):
            return {}
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data.json: {e}")
            return {}

    def save_data(self, data):
        # Create a backup first
        if os.path.exists(self.data_file):
            shutil.copy2(self.data_file, self.backup_file)
            
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True, "Saved successfully"
        except Exception as e:
            return False, str(e)
