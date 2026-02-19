import subprocess
import os
import sys

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        # Try to find git executable
        self.git_exec = "git"
        if sys.platform == "win32":
            # Common windows paths if not in PATH
            paths = [
                r"C:\Program Files\Git\bin\git.exe",
                r"C:\Program Files\Git\cmd\git.exe",
                r"C:\Users\{}\AppData\Local\Programs\Git\bin\git.exe".format(os.getlogin())
            ]
            for p in paths:
                if os.path.exists(p):
                    self.git_exec = p
                    break

    def get_git_version(self):
        try:
            res = subprocess.run([self.git_exec, '--version'], capture_output=True, text=True)
            return True, res.stdout.strip()
        except FileNotFoundError:
            return False, "Git executable not found in PATH."
        except Exception as e:
            return False, str(e)

    def _check_repo(self):
        if not self.repo_path or not os.path.exists(self.repo_path):
            return False, f"Repository path does not exist: {self.repo_path}"
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            return False, f"Directory is not a git repository (no .git folder): {self.repo_path}"
        return True, ""

    def run_git(self, args):
        valid, msg = self._check_repo()
        if not valid:
            return "", msg

        try:
            # Important: set shell=False for security, but ensure executable is found
            # On Linux, shell=False is standard.
            result = subprocess.run(
                [self.git_exec] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                return result.stdout.strip(), result.stderr.strip()
            return result.stdout.strip(), ""
        except Exception as e:
            return "", str(e)

    def get_status(self):
        # Check binary first
        ok, ver = self.get_git_version()
        if not ok:
            return [], [], ver

        stdout, err = self.run_git(['status', '-z', '--porcelain'])
        if err:
            return [], [], err
        
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

    # ... rest of methods use run_git, so they are fixed by proxy ...
    def get_diff(self, filepath=None, staged=False):
        args = ['diff']
        if staged: args.append('--cached')
        if filepath: args.append(filepath)
        stdout, err = self.run_git(args)
        return stdout if not err else err

    def stage_file(self, filepath): return self.run_git(['add', filepath])
    def unstage_file(self, filepath): return self.run_git(['reset', 'HEAD', filepath])
    def commit(self, message): return self.run_git(['commit', '-m', message])
    def push(self): return self.run_git(['push'])
    def pull(self): return self.run_git(['pull', '--rebase'])
