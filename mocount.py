#!/usr/bin/env python
from __future__ import unicode_literals

from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.history import FileHistory

from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

import os
import sqlite3
import dataset
import ptpdb

from utils import create_directory


project_path = '{}/.mocount'.format(os.path.expanduser('~'))
# creates the project dir if it doesn't exists
create_directory(project_path)

history_file = '{}/search-history'.format(project_path)
db_file = '{}/movies.db'.format(project_path)
db = dataset.connect('sqlite:///{}'.format(db_file))
db = dataset.connect()


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


def main():
    history = FileHistory(history_file)

    while True:
        try:
            text = prompt('> ', style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.
        if text:
            print('text:', text)
    print('GoodBye!')

if __name__ == '__main__':
    main()
