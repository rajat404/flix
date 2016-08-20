import os
import dataset
from db import DB

movie_ext = ['.3g2', '.3gp', '.3gp2', '.3gpp', '.60d', '.ajp', '.asf', '.asx',
             '.avchd', '.avi', '.bik', '.bix', '.box', '.cam', '.dat', '.divx',
             '.dmf', '.dv', '.dvr-ms', '.evo', '.flc', '.fli', '.flic', '.flv',
             '.flx', '.gvi', '.gvp', '.h264', '.m1v', '.m2p', '.m2ts', '.m2v',
             '.m4e', '.m4v', '.mjp', '.mjpeg', '.mjpg', '.mkv', '.moov',
             '.mov', '.movhd', '.movie', '.movx', '.mp4', '.mpe', '.mpeg',
             '.mpg', '.mpv', '.mpv2', '.mxf', '.nsv', '.nut', '.ogg', '.ogm',
             '.omf', '.ps', '.qt', '.ram', '.rm', '.rmvb', '.swf', '.ts',
             '.vfw', '.vid', '.video', '.viv', '.vivo', '.vob', '.vro', '.wm',
             '.wmv', '.wmx', '.wrap', '.wvx', '.wx', '.x264', '.xvid']

project_path = '{}/.mocount'.format(os.path.expanduser('~'))
# history_file = '{}/search-history'.format(project_path)
db_file = '{}/movies.db'.format(project_path)

dataset_db = dataset.connect('sqlite:///{}'.format(db_file))
db = DB(filename=db_file, dbname="movies", dbtype="sqlite")
