import os
import shutil
import sys

SCRIPT = 'source_script'

os.system('pip3 install pyinstaller')

os.system(f'pyinstaller -wF {SCRIPT}.py')

file_exts = {
    'linux': '',
    'linux2': '',
    'win32': '.exe',
    'cygwin': '.exe',
    'msys': '.exe',
    'darwin': '.app',
}


print(f'Done Building From Source. :) \n Run dist/{SCRIPT}{file_exts[sys.platform]} to launch Gitavra.')
