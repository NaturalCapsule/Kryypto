import os
import sys
import requests
import shutil
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from config import write_config, get_openedDir

# Try to import git, but handle the case where it's not available
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

folder_path_ = get_openedDir()

def is_gitInstalled():
    """Check if git is available both as a package and as a system command"""
    if not GIT_AVAILABLE:
        return False
    if shutil.which("git") is None:
        return False
    return True

def safe_git_operation(func):
    """Decorator to safely execute git operations"""
    def wrapper(*args, **kwargs):
        if not is_gitInstalled():
            return "Git Not installed"
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Git error: {str(e)}"
    return wrapper

def open_file_dialog(parent, check):
    global folder_path_
    if (folder_path_ == '' or folder_path_ == None or not folder_path_) and check:
        from widgets import MessageBox

        folder_path = QFileDialog.getExistingDirectory(parent, "Select a folder")
        if folder_path == '' or folder_path == None:
            MessageBox('No Folder selected\nKryypto will close')
            sys.exit()

        elif folder_path:
            folder_path_ = folder_path
            write_config(folder_path_, 'Appearance', 'OpenedFolder')
            return folder_path

def open_file_dialog_again(parent):
    global folder_path_

    folder_path = QFileDialog.getExistingDirectory(parent, "Select a folder")

    if folder_path:
        folder_path_ = folder_path
        write_config(folder_path_, 'Appearance', 'OpenedFolder')
        return folder_path

class GitWorkerSignals(QObject):
    dataReady = pyqtSignal(str, str, int, str, dict, str)

class GitWorker(QRunnable):
    def __init__(self):

        super().__init__()
        self.signals = GitWorkerSignals()

    def run(self):
        try:
            commit_msg = get_latest_commit()
            branch = get_active_branch_name()

            total = get_TotalCommits()

            commit_time = get_latest_commit_time()

            file_changes_ = file_changes()

            untracked_ = untracked()

            self.signals.dataReady.emit(commit_msg, branch, total, commit_time, file_changes_, untracked_)
        except Exception as e:
            pass


@safe_git_operation
def is_init():
    """Check if current directory is a git repository"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        return repo is not None
    except (git.InvalidGitRepositoryError, git.NoSuchPathError, git.GitCommandNotFound, git.GitError):
        return False

@safe_git_operation
def get_TotalCommits():
    """Get total number of commits in the repository"""
    repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
    commits = list(repo.iter_commits('HEAD'))
    return len(commits)

@safe_git_operation
def get_latest_commit_time():
    """Get the timestamp of the latest commit"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        latest_commit = repo.head.commit
        commit_timestamp = latest_commit.committed_date
        commit_datetime = datetime.fromtimestamp(commit_timestamp)
        return commit_datetime.strftime("%Y-%m-%d %I:%M %p")
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def get_reopName():
    """Get the repository name from the remote URL"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        repo_url = repo.remotes.origin.url
        if repo_url.endswith('.git'):
            repo_name = repo_url.split('/')[-1][:-4]
        else:
            repo_name = repo_url.split('/')[-1]
        return repo_name
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def get_active_branch_name():
    """Get the name of the active branch"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            return repo.active_branch.name
        else:
            return "No Active branch name"
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def get_github_remote_url(message):
    """Get the GitHub remote URL for the repository"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            return repo.remotes.origin.url
        else:
            return "No URL"
    except Exception as e:
        message(f'An error occurred:\n{e}')
        return f"Error: {e}"

@safe_git_operation
def get_github_profile(message):
    """Download GitHub profile picture for the user"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            config_reader = repo.config_reader()
            username = config_reader.get_value('user', 'name')

        r = requests.get(f'https://api.github.com/users/{username}')
        if r.status_code == 200:
            data = r.json()
            avatar_url = data.get("avatar_url")
            avatar_response = requests.get(avatar_url)

            if avatar_response.status_code == 200:
                with open("icons/github/user_profile/users_profile.png", "wb") as f:
                    f.write(avatar_response.content)
            else:
                message('Could not download pfp\nplease make sure you have internet connection')
        else:
            message('User Not Found!')
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def get_github_username():
    """Get the GitHub username from git config"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            config_reader = repo.config_reader()
            username = config_reader.get_value('user', 'name')
            return username
    except Exception as e:
        return f"Error: {e}"

def is_downloaded(message):
    if not os.path.exists('icons/github/user_profile/users_profile.png'):
        # Only try to download if git is installed
        if is_gitInstalled():
            get_github_profile(message)



@safe_git_operation
def get_latest_commit():
    """Get the message of the latest commit"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            commit = str(repo.head.commit.message)
            commit = commit[:-1]
            if len(commit) > 43:
                commit = f"{commit[:43]}..."
            return commit
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def file_changes():
    """Get file changes from the latest commit"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            return repo.head.commit.stats.files
    except Exception as e:
        return f"Error: {e}"

@safe_git_operation
def untracked():
    """Get list of untracked files"""
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        if repo:
            untracked_files = "\n   ".join(repo.untracked_files)
            return untracked_files
    except Exception as e:
        return f"Error: {e}"