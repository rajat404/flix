import os
from config import movie_ext

def create_project_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_list(movie_paths):
    all_paths = []
    for each_path in movie_paths.distinct('directory'):
        all_paths.append(each_path.get('directory'))
    file_list = []
    for directory in all_paths:
        for path, subdirs, files in os.walk(directory):
            # exclude hidden & temprary files
            files = [f for f in files if not f[0] in ('.', '~')]
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext.lower() in movie_ext:
                    file_list.append(filename)
    return file_list
