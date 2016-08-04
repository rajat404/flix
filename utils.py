import inspect
import os
import shutil


def create_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print('Error creating directory {} : {}'.format(directory, e))
