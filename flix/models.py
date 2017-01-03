from peewee import (SqliteDatabase, Model, CharField, IntegerField, FloatField,
                    TextField, ForeignKeyField, DateTimeField, BooleanField)
from .settings import DB_FILE
import datetime

database = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = database


class Media(BaseModel):
    """
    Contains information regarding Movies/TV Show
    """
    imdb_id = CharField(unique=True)
    title = CharField()
    year = IntegerField()
    rating = FloatField()
    metascore = FloatField()
    tomato_meter = FloatField()
    media_type = CharField()
    genre = CharField()
    actors = CharField()
    director = CharField()
    plot = TextField()
    released = CharField()
    runtime = CharField()
    tomato_url = CharField()
    poster = CharField()
    rated = CharField()
    watched = BooleanField(default=True)

    class Meta:
        db_table = 'media'


class File(BaseModel):
    """
    Record of all the filenames scanned by the app
    """
    filename = CharField(unique=True)
    media = ForeignKeyField(Media, null=True)

    class Meta:
        db_table = 'file'


class Directory(BaseModel):
    """
    Directories to scan
    """
    directory = CharField(unique=True)

    class Meta:
        db_table = 'directory'
