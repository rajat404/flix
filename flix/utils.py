import os
import requests
import json
import glob
from guessit import guessit
from .settings import media_extenions, media_url, response_mapping, logger
from .helpers import print_error, flatten
from peewee import IntegrityError, OperationalError
from .models import Media, File


def create_project_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_list(dir_list):
    """
    Takes list of directories and returns all media files in those directories
    """
    file_list = []
    if isinstance(dir_list, list) is False:
        raise ValueError('Please enter a list, not string')
    for directory in dir_list:
        # TODO: Instead of all media_extenions, ask user which extensions to consider
        file_list.extend(flatten([glob.glob('{}/*/**/*{}'.format(directory, ext), recursive=True)
                                  for ext in media_extenions]))
    return file_list


@print_error
def fetch_media_details(filename):
    """
    Takes the name of the media file and returns the metadata for the movie
    """
    info = guessit(filename)
    logger.info('\n', info['title'])
    params = {'t': info['title'].encode('ascii', 'ignore'),
              'type': info['type'],
              'tomatoes': 'true',
              'plot': 'full',
              'v': '1'}
    if 'year' in info:
        params['y'] = info['year']

    resp = requests.get(url=media_url, params=params)
    response = json.loads(resp.text)

    # because resp.ok - is coming true for all cases
    if response['Response'] == 'True':
        temp = remap_response(response=response)
        return temp
    return None


def save_media_details(filename, details):
    """
    Takes the media details and saves in the DB
    """
    filename = filename.split('/')[-1]
    try:
        file = File.create(filename=filename)
    except IntegrityError:
        print('File `{}` already exists'.format(filename))
        pass

    if details:
        try:
            media = Media.create(**details)
            file.media = media
            file.save()
        except IntegrityError:
            print('Details for `{}` already exists'.format(details['title']))
            pass


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
