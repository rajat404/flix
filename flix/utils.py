import os
import requests
import json
import glob
# from guessit import guessit
from .settings import MEDIA_EXTENSIONS, MEDIA_URL, response_mapping, logger
from .helpers import log_error, flatten
from peewee import IntegrityError
from .models import Media, File


def create_db_directory(directory):
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
        # TODO: Instead of all MEDIA_EXTENSIONS, ask user which extensions to consider
        file_list.extend(flatten([glob.glob('{}/*/**/*{}'.format(directory, ext), recursive=True)
                                  for ext in MEDIA_EXTENSIONS]))
    return file_list


def check_file_existence(info):
    """
    Check whether the file already exists in the DB
    """
    # info = guessit(filename)
    try:
        Media.get(Media.title == info['title'])
        return True
    except Media.DoesNotExist:
        return False


@log_error
def fetch_media_details(info):
    """
    Takes the name of the media file and returns the metadata for the movie
    """
    # info = guessit(filename)
    logger.info('\n', info['title'])
    params = {'t': info['title'].encode('ascii', 'ignore'),
              'tomatoes': 'true',
              'plot': 'full',
              'v': '1'}

    if 'year' in info:
        params['y'] = info['year']

    # OMDB API limitation
    if info['type'] == 'episode':
        params['type'] = 'series'

    resp = requests.get(url=MEDIA_URL, params=params)
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
        return

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

        # OMDB API limitation
        # For TV Series, the year can be a string like `2009-2015`
        if new_key == 'year' and len(value) > 4:
            value = value.split('–')[0]

        result[new_key] = result_data_type(value)
    return result
