#!/usr/bin/env python
from __future__ import unicode_literals

from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.history import FileHistory

from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

import dataset
import click

from utils import create_project_directory, add_path, get_file_list
from config import project_path, history_file, db_file, movie_paths

db = dataset.connect('sqlite:///{}'.format(db_file))


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


@click.command()
@click.argument('directories', nargs=-1, type=click.Path())
def main(directories):
    """
    Enter the absolute paths of the directories containing your
    Movies/TV Shows, separated by an empty space
    """
    # creates the project dir if it doesn't exists
    create_project_directory(project_path)
    if directories:
        for directory in directories:
            # Ensure that the directory path begins with '/', but doesn't end with one
            path = '/{}'.format(directory.strip('/'))
            if path not in movie_paths:
                add_path(path)

    print('Press Ctrl+D to exit at any time!')
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
