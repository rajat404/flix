import dataset
from config import db_file

db = dataset.connect('sqlite:///{}'.format(db_file))
# movie_paths = db['movie_paths']
