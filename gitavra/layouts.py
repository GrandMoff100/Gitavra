import PySimpleGUI as sg
from gitavra.utils import reshape_2d_array
import git


COMMIT_LIST_COLOR = 'lightgray'
THEME = 'TealMono'
FONT = "serif"

# Sets Global Theme
sg.theme(THEME)

# Class for dealing with formatting a branches commits
class CommitList:
    def __init__(self, branch: str, repo: git.Repo):
        self.commits = []
        for commit in repo.iter_commits(branch):
            self.commits.append(
                [
                    sg.Text(commit.author.name, background_color=COMMIT_LIST_COLOR, font=f'{FONT} 10'),
                    sg.Text(commit.message.replace('\n', ''), background_color=COMMIT_LIST_COLOR, font=f'{FONT} 10'),
                    sg.Text('+{} / –{}'.format(
                        commit.stats.total['insertions'],
                        commit.stats.total['deletions']
                        ), background_color=COMMIT_LIST_COLOR, font=f'{FONT} 10'
                    ),
                    sg.Text(str(commit.stats.total['files']), background_color=COMMIT_LIST_COLOR, font=f'{FONT} 10'),
                    sg.Text('{}/{}/{}'.format(
                        commit.authored_datetime.month,
                        commit.authored_datetime.day,
                        commit.authored_datetime.year
                        ), background_color=COMMIT_LIST_COLOR, font=f'{FONT} 10'
                    ),
                ]
            )

    def __iter__(self):
        yield [
            sg.Text('Author', font=f'{FONT} 14 bold', background_color=COMMIT_LIST_COLOR),
            sg.Text('Message', font=f'{FONT} 14 bold', background_color=COMMIT_LIST_COLOR),
            sg.Text('Lines +/-', font=f'{FONT} 14 bold', background_color=COMMIT_LIST_COLOR),
            sg.Text('Files', font=f'{FONT} 14 bold', background_color=COMMIT_LIST_COLOR),
            sg.Text('Date', font=f'{FONT} 14 bold', background_color=COMMIT_LIST_COLOR)
        ]

        for commit in self.commits:
            yield commit


def new_window(name: str, layout: list, *args, **kwargs):
    import PySimpleGUI as new_sg
    new_sg.theme(THEME)
    return new_sg.Window(name, layout, *args, **kwargs)


def main_layout(repo=None, is_git_repo:bool = True):
    def branch_tab_layout(branch: str = ''):
        # Git Buttons
        column1 = sg.Column([
            [sg.Text('Git', font=f'{FONT} 24 bold')],
            [sg.TabGroup([[
                sg.Tab('Basic', [[sg.B('Add'), sg.B('Commit'), sg.B('Push'), sg.B('Pull')], [sg.B('Fetch'), sg.B('Branch'),]]),
                sg.Tab('Files', [[sg.B('Move'), sg.B('Delete'),]]),
                sg.Tab('Remotes', [[sg.B('List'), sg.B('Remove'),]]),
                sg.Tab('Verbose', [[sg.B('Remotes'), sg.B('Branches')]]),
                sg.Tab('Advanced', [[sg.B('Reset'), sg.B('Restore'), sg.B('Config')]]),
            ]], key='button-tab')],
            [sg.Text('Some More graphs down here.')]
        ], element_justification='center')

        column3 = sg.Text('None')

        column2 = sg.Column(
            [[sg.Text('Commits', font=f'{FONT} 24 bold', background_color=COMMIT_LIST_COLOR)]] +
            [[sg.Column([[element] for element in column], background_color=COMMIT_LIST_COLOR) for column in reshape_2d_array(list(CommitList(branch, repo)))]],
            background_color=COMMIT_LIST_COLOR,
            element_justification='center'
        ) if is_git_repo else sg.Text(' ' * 50 + 'No Commits Yet...' + ' ' * 50)
        return [[column1, column2, column3]]

    topmenu = [
        ['&Repo', ['&Open', '&Refresh', '---', ' E&xit']],
        ['&Help', ['&Docs', 'Guide to git']]
    ]

    layout = [
        [sg.Menu(topmenu, key='menu')],
        [sg.Text(' '*30), sg.Text('This Repository Has Not Been Initialized Yet.', font=f'{FONT} 24 bold')] if not is_git_repo else [],
        [sg.Text(' '*40), sg.Text('Refresh The Aplication When Done.', font=f'{FONT} 24 bold')] if not is_git_repo else [],
        [sg.TabGroup(
            [[sg.Tab(branch, branch_tab_layout(branch)) for branch in repo.branches] if repo else []], key='branch-tab'
        )]
    ]
    return layout


