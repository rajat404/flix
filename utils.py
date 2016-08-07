import os
import requests
from guessit import guessit

from config import movie_ext
from db_config import db

keys_to_keep = ['Actors', 'Director', 'Genre', 'Metascore', 'Plot', 'Released',
                'Runtime', 'Title', 'Type', 'Year', 'imdbID', 'imdbRating',
                'tomatoConsensus', 'tomatoMeter', 'tomatoURL',
                'tomatoUserMeter']

url = 'http://www.omdbapi.com/?'


def create_project_directory(directory):
    """
    Creates the specified directory if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_list():
    all_paths = db.tables.movie_paths.unique('directory')['directory'].tolist()
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


def fetch_movie_details(movie):
    info = guessit(movie)
    params = {'t': info['title'].encode('ascii', 'ignore'),
              'type': info['type'],
              'tomatoes': 'true'}
    if 'year' in info:
        params['y'] = info['year']

    resp = requests.get(url=url, params=params)
    response = resp.json()
    return {k: response[k] for k in keys_to_keep if k in response}
