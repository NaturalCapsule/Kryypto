from config import get_stylefile

ids = [
    "MainWindow",
    "Window",
    "Editor",
    "Terminal",
    "Finder",
    "GoLine",
    "AutoCompleter",
    "GitPanel",
    "DockTitles",
    "Docks",
    "TitleBarBG",
    "TitleBarName",
    "TitleBarMin",
    "TitleBarMax",
    "TitleBarClose",
    "DocStrings",
    "FileMaker",
    "FolderMaker",
    "horizontalLines",
    "DirectoryViewer",
    "OpenedFiles",
    "CloseTabButton",
    "SyntaxChecker",
    "NameErrorChecker",
    "NumberLines",
    "Greeting",
    "Date",
    "TotalCommits",
    "ActiveBranch",
    "RemoteURL",
    "Username",
    "CommitInfo",
    "CommitTime",
    "CommitMessage",
    "RepoName",
    "RepoNotFound",
    "fileChanges",
    "UntrackedFiles",
    "RepoInfo",
    "UserProfile",
    "ShortCutTexts",
    "MessageBox",
    "MessageBoxSave",
    "MessageBoxSaveNot",
    "MessageBoxCancel"
]
import os
def get_css_style():
    try:
        with open(get_stylefile()) as f:
            read_file = f.read()
            for id in ids:
                if f"#{id}" not in read_file:
                    with open(get_stylefile(), 'a', encoding = 'utf-8') as append_text:
                        append_text.write(f"\n#{id}" + " {\n    \n}")
            # print(f.read())
            # return f.read()
            return read_file

    except FileNotFoundError:
        with open(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css') as f:
            return f.read()