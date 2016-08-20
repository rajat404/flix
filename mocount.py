#!/usr/bin/env python
import os
import sys

import utils
from config import project_path, dataset_db


def main():
    """
    Enter the absolute paths of the directories containing your
    Movies/TV Shows, separated by an empty space
    """
    # creates the project dir if it doesn't exists
    utils.create_project_directory(project_path)
    directories = sys.argv[1:]
    print('dir entered:', directories)
    # if len(directories) == 0:
    #     print("Please mention the directories")
    #     return

    movie_paths = dataset_db['movie_paths']
    movie_data = dataset_db['movie_data']

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

    failed_list = []
    movie_data = dataset_db['movie_data']
    for i, filename in enumerate(file_list):
        try:
            data_exists = movie_data.find_one(Filename=filename)
            if data_exists:
                print('Already indexed:', filename)
                continue
        except:
            pass

        print(i, filename)
        temp = utils.fetch_movie_details(filename)
        if temp is False:
            failed_list.append(filename)
            continue

    print('Failed for:', failed_list)

if __name__ == '__main__':
    main()
