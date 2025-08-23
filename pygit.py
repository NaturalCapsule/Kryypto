import git
import os
import sys
import requests
import shutil
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from config import write_config, get_openedDir

folder_path_ = get_openedDir()

def is_gitInstalled():
    if shutil.which("git") is None:
        return False
    else:
        return True

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


def is_init():

    if shutil.which("git") is None:
        return False

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)



        if repo:
            return True
        else:
            return False

    except Exception:
        return False
    except git.InvalidGitRepositoryError:
        return False

    except git.NoSuchPathError:
        return False
    except git.GitCommandNotFound:
        return False

    except git.GitError:
        return False

def get_TotalCommits():
    if shutil.which("git") is None:
        return "Git Not installed"

    repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)


    commits = list(repo.iter_commits('HEAD'))

    total_commits = len(commits)
    return total_commits

def get_latest_commit_time():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo_path = os.getcwd()
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)



        latest_commit = repo.head.commit
        commit_timestamp = latest_commit.committed_date
        commit_datetime = datetime.fromtimestamp(commit_timestamp)

        return commit_datetime.strftime("%Y-%m-%d %I:%M %p")

    except git.InvalidGitRepositoryError:
        return f"Error: '{repo_path}' is not a valid Git repository."

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitError:
        return "Git Not installed or not found"

def get_reopName():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)
        repo = repo.remotes.origin.url
        if repo.endswith('.git'):
            repo = repo.split('/')[-1]
            repo = repo[:-4]
        else:
            repo = repo.split('/')[-1]
            repo = ''.join(repo)

        return repo
    except git.InvalidGitRepositoryError:
        pass

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def get_active_branch_name():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)


        if repo:
            return repo.active_branch.name
        else:
            return "No Active branch name"

    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"
    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def get_github_remote_url(message):
    if shutil.which("git") is None:
        return "Git Not installed"
    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)


        if repo:
            return repo.remotes.origin.url
        else:
            return "No URL"

    except git.InvalidGitRepositoryError as e:
        message(f'Invalid Git Repository\n{e}')
        return f"Error: something went wrong!"

    except Exception as e:
        message(f'An error occurred:\n{e}')
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def get_github_profile(message):
    if shutil.which("git") is None:
        return "Git Not installed"

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


    except git.InvalidGitRepositoryError as e:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def get_github_username():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)

        if repo:
            config_reader = repo.config_reader()
            username = config_reader.get_value('user', 'name')
            return username

    except git.InvalidGitRepositoryError as e:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def is_downloaded(message):
    if not os.path.exists('icons/github/user_profile/users_profile.png'):
        get_github_profile(message)



def get_latest_commit():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)

        if repo:
            commit = str(repo.head.commit.message)
            commit = commit[:-1]
            if len(commit) > 43:
                commit = f"{commit[:43]}..."

            return commit


    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def file_changes():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)

        if repo:
            return repo.head.commit.stats.files


    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"

def untracked():
    if shutil.which("git") is None:
        return "Git Not installed"

    try:
        repo = git.Repo(fr'{get_openedDir()}', search_parent_directories=True)

        if repo:
            untracked_files = "\n   ".join(repo.untracked_files)
            return untracked_files



    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"
        
    except git.GitCommandNotFound:
        return 'Git Not installed'

    except git.GitError:
        return "Git Not installed or not found"