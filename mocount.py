#!/usr/bin/env python
import os
import sys

import utils
from config import project_path
from db_config import db, dataset_db


def main():
    """
    Enter the absolute paths of the directories containing your
    Movies/TV Shows, separated by an empty space
    """
    # creates the project dir if it doesn't exists
    utils.create_project_directory(project_path)
    directories = sys.argv[1:]
    print('dir entered:', directories)
    if directories is None:
        print("Please mention the directories")
        return

    movie_paths = dataset_db['movie_paths']
    for directory in directories:
        # Ensure that the directory path begins with '/',
        # but doesn't end with one, and is NOT root
        path = '/{}'.format(directory.strip('/'))
        if path == '/':
            continue
        if os.path.exists(path):
            movie_paths.upsert(dict(directory=path), ['directory'])

    file_list = utils.get_file_list()
    if file_list is None:
        print('No video files found')
        return
    print('file_list:', file_list)

    movie_data = []
    for movie in file_list:
        temp = utils.fetch_movie_details(movie)
        movie_data.append(temp)


if __name__ == '__main__':
    main()
