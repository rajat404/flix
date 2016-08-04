import os
from config import movie_ext, movie_paths

def create_project_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def add_path(directory):
    """
    Adds the specified directory in the config as a movie path
    """
    if not os.path.exists(directory):
        return False
    movie_paths.append(directory)


def get_file_list():
    file_list = []
    for directory in movie_paths:
        for path, subdirs, files in os.walk(directory):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext.lower() in movie_ext:
                    file_list.append(filename)
    return file_list
