import os
import requests
import json
import glob
from guessit import guessit
from settings import media_extenions, dataset_db, movie_api_url, response_mapping, logger

import linecache
import sys
import traceback
from decorator import decorator


@decorator
def print_error(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        traceback_text = ''.join(traceback.format_exception(*sys.exc_info()))
        logger.error('EXCEPTION IN:\nFUNCTION: {}\nERROR: {}\nEXCEPTION: {}'.format(
            fn.__name__, exc_obj, traceback_text))
        print('EXCEPTION IN:\nFUNCTION: {}\nERROR: {}\nEXCEPTION: {}'.format(
            fn.__name__, exc_obj, traceback_text))
        print('-'*50)


def create_project_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


# def get_file_list(dir_list):
#     # dir_list = db.tables.movie_paths.unique('directory')['directory'].tolist()
#     file_list = []
#     for directory in dir_list:
#         for path, subdirs, files in os.walk(directory):
#             # exclude hidden & temprary files
#             files = [f for f in files if not f[0] in ('.', '~')]
#             for filename in files:
#                 name, ext = os.path.splitext(filename)
#                 if ext.lower() in media_extenions:
#                     file_list.append(filename)
#     return file_list

def get_file_list(dir_list):
    file_list = []
    for directory in dir_list:
        # TODO: Instead of all media_extenions, ask user which extensions to consider
        file_list.extend(flatten([glob.glob('{}/*/**/*{}'.format(directory, ext), recursive=True)
                                  for ext in media_extenions]))
    return file_list


def fetch_movie_details(filename):
    """
    Takes the name of the media file and returns the metadata for the movie
    """
    info = guessit(filename)
    # print('\n', info['title'])
    params = {'t': info['title'].encode('ascii', 'ignore'),
              'type': info['type'],
              'tomatoes': 'true',
              'plot': 'full',
              'v': '1'}
    if 'year' in info:
        params['y'] = info['year']

    resp = requests.get(url=movie_api_url, params=params)
    response = json.loads(resp.text)

    # because resp.ok - is coming true for all cases
    if response['Response'] == 'True':
        temp = remap_response(response=response)
        return (filename, temp)
    return (filename, None)


def save_media_details(filename, details):
    """Takes the media details and saves in the DB"""
    table = dataset_db['Media']
    # temp['filename'] = filename
    # movie_data.insert(temp)
    table.insert(**details)


def remap_response(response, response_mapping=response_mapping):
    """
    Takes the Media API response body, and returns a new dict,
    with the keys and values as per `response_mapping`
    """
    result = {}
    for original_key, new_key, result_data_type, default_value in response_mapping:
        value = response.get(original_key)

        if value == 'N/A':
            value = default_value

        result[new_key] = result_data_type(value)
    return result


def flatten(lis):
    """
    Takes a list (nested or regular), and returns a flat list
    """
    result = []
    for item in lis:
        if isinstance(item, list):
            result.extend(flatten(item))
        # won't accept empty dict or tuple
        elif item not in [None, (), {}]:
            result.append(item)
    return result
