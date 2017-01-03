import os
import logging
# import dataset
from playhouse.dataset import DataSet

# for DB.py
# from db import DB
# db = DB(filename=db_file, dbname="flix", dbtype="sqlite")
logger = logging.getLogger()

# LOG_FILENAME = 'flix.log'
# logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,)


project_path = '{}/.flix'.format(os.path.expanduser('~'))
db_file = '{}/flix.db'.format(project_path)

# dataset_db = dataset.connect('sqlite:///{}'.format(db_file))
dataset_db = DataSet('sqlite:///{}'.format(db_file))

media_url = 'http://www.omdbapi.com/?'

# media_extenions = [
#     '.3g2', '.3gp', '.3gp2', '.3gpp', '.60d', '.ajp', '.asf', '.asx',
#     '.avchd', '.avi', '.bik', '.bix', '.box', '.cam', '.dat', '.divx',
#     '.dmf', '.dv', '.dvr-ms', '.evo', '.flc', '.fli', '.flic', '.flv',
#     '.flx', '.gvi', '.gvp', '.h264', '.m1v', '.m2p', '.m2ts', '.m2v',
#     '.m4e', '.m4v', '.mjp', '.mjpeg', '.mjpg', '.mkv', '.moov',
#     '.mov', '.movhd', '.movie', '.movx', '.mp4', '.mpe', '.mpeg',
#     '.mpg', '.mpv', '.mpv2', '.mxf', '.nsv', '.nut', '.ogg', '.ogm',
#     '.omf', '.ps', '.qt', '.ram', '.rm', '.rmvb', '.swf', '.ts',
#     '.vfw', '.vid', '.video', '.viv', '.vivo', '.vob', '.vro', '.wm',
#     '.wmv', '.wmx', '.wrap', '.wvx', '.wx', '.x264', '.xvid'
# ]

media_extenions = [
    '.3gp', '.dat', '.divx', '.flv', '.m4v', '.mkv', '.mov', '.movhd',
    '.mp4', '.mpeg', '.mpg', '.rm', '.rmvb', '.vob', '.wm', '.wmv', '.xvid'
]

response_mapping = [
    # format: (original_key, new_key, result_data_type, default_value)
    ('Actors', 'actors', str, ''),
    ('Director', 'director', str, ''),
    ('Genre', 'genre', str, ''),
    ('Metascore', 'metascore', float, 0),
    ('Plot', 'plot', str, ''),
    ('Released', 'released', str, ''),
    ('Runtime', 'runtime', str, ''),
    ('Title', 'title', str, ''),
    ('Type', 'media_type', str, ''),
    ('Year', 'year', int, 0),
    ('imdbID', 'imdb_id', str, ''),
    ('imdbRating', 'rating', float, 0),
    ('tomatoMeter', 'tomato_meter', float, 0),
    ('tomatoURL', 'tomato_url', str, ''),
    ('Poster', 'poster', str, ''),
    ('Rated', 'rated', str, ''),
]
