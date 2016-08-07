import dataset
from db import DB
from config import db_file

dataset_db = dataset.connect('sqlite:///{}'.format(db_file))
db = DB(filename=db_file, dbname="movies", dbtype="sqlite")
