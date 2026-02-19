import subprocess
import os

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def _check_repo(self):
        if not self.repo_path or not os.path.exists(self.repo_path):
            return False, "Repository path does not exist."
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            return False, "Directory is not a git repository."
        return True, ""

    def run_git(self, args):
        valid, msg = self._check_repo()
        if not valid:
            return "", msg

        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                # Return stderr as the error message if command failed
                return result.stdout.strip(), result.stderr.strip()
            return result.stdout.strip(), ""
        except FileNotFoundError:
            return "", "Git executable not found in PATH."
        except Exception as e:
            return "", str(e)

    def get_status(self):
        stdout, err = self.run_git(['status', '-z', '--porcelain'])
        if err:
            return [], [], err  # Return error
        
        staged = []
        unstaged = []
        
        if not stdout:
            return staged, unstaged, ""

        entries = stdout.split('\x00')
        for entry in entries:
            if not entry or len(entry) < 3: continue
            code = entry[:2]
            path = entry[3:]
            
            x_code = code[0]
            y_code = code[1]
            
            if x_code in 'MADRC': 
                staged.append({'path': path, 'status': x_code})
            if y_code in 'MD?':   
                unstaged.append({'path': path, 'status': y_code})
                
        return staged, unstaged, ""

    def get_diff(self, filepath=None, staged=False):
        args = ['diff']
        if staged:
            args.append('--cached')
        if filepath:
            args.append(filepath)
        stdout, err = self.run_git(args)
        if err: return f"Error getting diff: {err}"
        return stdout

    def stage_file(self, filepath):
        return self.run_git(['add', filepath])

    def unstage_file(self, filepath):
        return self.run_git(['reset', 'HEAD', filepath])

    def commit(self, message):
        return self.run_git(['commit', '-m', message])

    def push(self):
        return self.run_git(['push'])

    def pull(self):
        return self.run_git(['pull', '--rebase'])
