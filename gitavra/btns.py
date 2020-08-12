import git
import PySimpleGUI as sg
from gitavra.layouts import new_window, THEME, FONT

sg.theme(THEME)


def git_init(values: dict):
    git.Repo.init(values['FOLDER'])
    sg.Popup(
        'Repository Initialized!'
    )


# Define Git Action Button responses
def git_add(values: dict):
        files = ['All Files'] + values["REPO"].untracked_files

        selector_layout = [
            [sg.Text('Choose a File', font=f'{FONT} 14 bold')],
            [sg.Text('Note: No files to add to git.')] if len(files) == 1 else [],
            [sg.Listbox(files, size=(150, 8), key='file-to-add')],
            [sg.Button('Enter')]
        ]

        file_selector_window = new_window(
            'Git -  [ git add <file> ]',
            selector_layout,
            size=(400, 250),
            keep_on_top=True,
            element_justification='center'
        )

        # Reads the windows for a one-shot window event.
        event, vals = file_selector_window.read()

        # Closes once read.
        file_selector_window.close()

        # Assigns the File to add to a variable.
        file = vals['file-to-add'] if vals['file-to-add'] != ['All Files'] else ['.']

        # Validates if there were any actual files to add besides the Default Option.
        if len(files) != 1:
            # Adds `file` the Repository's Index Tree.
            values['REPO'].git.add(file)

            sg.Popup(
                f'File(s) have been added to git!',
                title='Executed Successfully',
                font=f'{FONT} 10 bold'
            )
