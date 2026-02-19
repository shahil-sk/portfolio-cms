import subprocess
import os

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def run_git(self, args):
        try:
            # Run git command in the repo directory
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)

    def get_status(self):
        # -z for machine readable output, --porcelain for stable format
        stdout, _ = self.run_git(['status', '-z', '--porcelain'])
        if not stdout:
            return [], []
        
        staged = []
        unstaged = []
        
        # Parse null-terminated strings
        entries = stdout.split('\x00')
        for entry in entries:
            if not entry or len(entry) < 3: continue
            code = entry[:2]
            path = entry[3:]
            
            # X = Index (staged), Y = Worktree (unstaged)
            x_code = code[0]
            y_code = code[1]
            
            if x_code in 'MADRC': # Staged
                staged.append({'path': path, 'status': x_code})
            if y_code in 'MD?':   # Unstaged (Modified, Deleted, Untracked)
                unstaged.append({'path': path, 'status': y_code})
                
        return staged, unstaged

    def get_diff(self, filepath=None, staged=False):
        args = ['diff']
        if staged:
            args.append('--cached')
        if filepath:
            args.append(filepath)
        stdout, _ = self.run_git(args)
        return stdout

    def stage_file(self, filepath):
        self.run_git(['add', filepath])

    def unstage_file(self, filepath):
        self.run_git(['reset', 'HEAD', filepath])

    def commit(self, message):
        self.run_git(['commit', '-m', message])

    def push(self):
        return self.run_git(['push'])

    def pull(self):
        return self.run_git(['pull', '--rebase'])
