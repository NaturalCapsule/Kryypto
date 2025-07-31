import git
import os
import sys
import requests
from datetime import datetime
# from widgets import MessageBox_someshit
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

folder_path_ = None
# class Dialog(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.deleteLater()

def open_file_dialog(parent):
    global folder_path_
    folder_path = QFileDialog.getExistingDirectory(parent, "Select a folder")

    if folder_path:
        folder_path_ = folder_path
        return folder_path

# dialoger = QApplication(sys.argv)
# window = Dialog()
# file = open_file_dialog()
# window.show()
# sys.exit(dialoger.exec())



class GitWorkerSignals(QObject):
    dataReady = pyqtSignal(str, str, int, str, dict, str)

class GitWorker(QRunnable):
    # def __init__(self, repo):
    def __init__(self):

        super().__init__()
        # self.repo = repo
        self.signals = GitWorkerSignals()

    def run(self):
        try:
            commit_msg = get_latest_commit()
            # commit_msg = self.repo.head.commit.message
            # branch = self.repo.active_branch.name
            branch = get_active_branch_name()

            # total = len(list(self.repo.iter_commits('HEAD')))
            total = get_TotalCommits()

            commit_time = get_latest_commit_time()

            file_changes_ = file_changes()

            untracked_ = untracked()

            self.signals.dataReady.emit(commit_msg, branch, total, commit_time, file_changes_, untracked_)
        except Exception as e:
            # print("GitWorker error:", e)
            pass


def is_init():
    try:
        # print(folder_path_)
        # repo = git.Repo(os.getcwd(), search_parent_directories=True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)


        if repo:
            # MessageBox_someshit()
            return True
        else:
            return False
        # return "Initialized!"

        # else:
        #     # return "Initialize in current or a parent directory!"
        #     return "Initialized"

    except Exception:
        # pass
        return False
    except git.InvalidGitRepositoryError:
        # print('d')
        # return "Not initialized"
        return False

    except git.NoSuchPathError:
        return False

def get_TotalCommits():
    # repo_path = os.getcwd() 

    # repo = git.Repo(repo_path)
    repo = git.Repo(fr'{folder_path_}', search_parent_directories = True)

    commits = list(repo.iter_commits('HEAD'))

    total_commits = len(commits)
    return total_commits

def get_latest_commit_time():
    try:
        repo_path = os.getcwd()
        # repo = git.Repo(repo_path, search_parent_directories=True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)


        latest_commit = repo.head.commit
        commit_timestamp = latest_commit.committed_date
        commit_datetime = datetime.fromtimestamp(commit_timestamp)

        # return f"{commit_datetime}"
        return commit_datetime.strftime("%Y-%m-%d %I:%M %p")

    except git.InvalidGitRepositoryError:
        return f"Error: '{repo_path}' is not a valid Git repository."

    except Exception as e:
        return f"An error occurred: {e}"


def get_reopName():
    try:
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)


        repo = repo.remotes.origin.url
        if repo.endswith('.git'):
            repo = repo.split('/')[-1]
            repo = repo[:-4]
        else:
            repo = repo.split('/')[-1]
            repo = ''.join(repo)

        return repo
    except git.InvalidGitRepositoryError:
        # return f"Error: '{repo_name}' is not a valid Git repository."
        pass

    except Exception as e:
        return f"An error occurred: {e}"

def get_active_branch_name():
    try:
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

        if repo:
            return repo.active_branch.name
        else:
            return "No Active branch name"

    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

def get_github_remote_url(message):
    try:
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

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


def get_github_profile(message):
    try:
        # repo = git.Repo(os.getcwd(), search_parent_directories = True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

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
                # print("Could not download pfp")
                message('Could not download pfp\nplease make sure you have internet connection')


        else:
            # print("User not found")
            message('User Not Found!')


    except git.InvalidGitRepositoryError as e:
        # message(f'Invalid Git Repository\n{e}')
        return f"Error: something went wrong!"

    except Exception as e:
        # message(f'An error occurred:\n{e}')
        return f"An error occurred: {e}"

def get_github_username():
    try:
        # repo = git.Repo(os.getcwd(), search_parent_directories = True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

        if repo:
            config_reader = repo.config_reader()
            username = config_reader.get_value('user', 'name')
            return username

    except git.InvalidGitRepositoryError as e:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"


def is_downloaded(message):
    if not os.path.exists('icons/github/user_profile/users_profile.png'):
        get_github_profile(message)



def get_latest_commit():
    try:
        # repo = git.Repo(os.getcwd(), search_parent_directories = True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

        if repo:
            commit = str(repo.head.commit.message)
            commit = commit[:-1]
            if len(commit) > 43:
                commit = f"{commit[:43]}..."

            # return repo.head.commit.message
            return commit


    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"


def file_changes():
    try:
        # repo = git.Repo(os.getcwd(), search_parent_directories = True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

        if repo:
            # print(repo.head.commit.stats.total)
            return repo.head.commit.stats.files


    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"

def untracked():
    try:
        # repo = git.Repo(os.getcwd(), search_parent_directories = True)
        repo = git.Repo(fr'{folder_path_}', search_parent_directories=True)

        if repo:
            # for file in repo.untracked_files:
                # print(file)
            untracked_files = "\n   ".join(repo.untracked_files)
            # return repo.untracked_files
            return untracked_files



    except git.InvalidGitRepositoryError:
        return f"Error: something went wrong!"

    except Exception as e:
        return f"An error occurred: {e}"
