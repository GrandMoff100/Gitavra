import os
import sys

import PySimpleGUI as sg
import git
# GitPython Docs -> https://gitpython.readthedocs.io

from gitavra.config import get_config, set_config
from gitavra.layouts import main_layout, new_window
from gitavra.btns import git_init, git_add
from gitavra.menu import open_git_guide, open_gitavra_docs

# Main Script
if __name__ == '__main__':
    # Get Current confiuration settings from ~/.gitavra file
    config = get_config()

    # Assign the LAST_OPENED_REPO configuration variable to a global variable.
    FOLDER = config.get('LAST_OPENED_REPO', 'None') if config.get('LAST_OPENED_REPO', 'None') != 'None' else os.getcwd()

    # Assigns a global boolean to pass to the main_layout contructor function.
    IS_GIT_REPO = True

    try:
        # Create a Global Variable to access the git.Repo repo object for the current FOLDER.
        REPO = git.Repo(FOLDER, odbt=git.GitCmdObjectDB)
    except git.exc.InvalidGitRepositoryError:
        IS_GIT_REPO = False
        REPO = None

    # Create Initial GUI window.
    main_window = new_window(
        'Gitavra  [{}]  -  (An effective git interface.)'.format(FOLDER),
        main_layout(REPO, is_git_repo=IS_GIT_REPO),
        size=(1200, 600)
    )

    # Define a response to user closing the window.
    def exit_if_closed(values: dict):
        main_window.close()
        set_config('LAST_OPENED_REPO', FOLDER)
        sys.exit()

    # Define event triggers and appropriate responses (functions)
    events = {
        None: exit_if_closed,
        'Exit': exit_if_closed,
        'Docs': open_gitavra_docs,
        'Guide to git': open_git_guide,
        # Button Event Responses from gitavra/btns.py
        'Init': git_init,
        'Add': git_add,
    }

    while True:
        event, values = main_window.read()

        # Makes Global Variables here accessible to response functions
        if type(values) == dict:
            values['REPO'] = REPO
            values['FOLDER'] = FOLDER

        # If an event has a registered function to call from `events` then it gets the function and
        # calls in with the current values dictionary.
        if event in ['Open', 'Refresh']:
            if event == 'Open':
                FOLDER = sg.popup_get_folder('Open a Git Repository', keep_on_top=True)

            IS_GIT_REPO = True
            try:
                REPO = git.Repo(FOLDER, odbt=git.GitCmdObjectDB)
            except git.exc.InvalidGitRepositoryError:
                IS_GIT_REPO = False

            main_window.close()
            main_window = new_window(
                'Gitavra  [ {} ]  -  (An Effective Git Interface)'.format(FOLDER),
                main_layout(REPO, IS_GIT_REPO),
                size=(1200, 600)
            )

        print(event, values)

        if event in events:
            print('Calling... {}'.format(events[event].__name__))
            print(values)
            events[event](values)


