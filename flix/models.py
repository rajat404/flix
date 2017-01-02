from peewee import (SqliteDatabase, Model, CharField, IntegerField, FloatField,
                    TextField, ForeignKeyField, DateTimeField)
from playhouse.fields import ManyToManyField

from .settings import db_file
import datetime

database = SqliteDatabase(db_file)


class BaseModel(Model):
    modified_at = DateTimeField(default=datetime.datetime.now())

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

    class Meta:
        db_table = 'media'


class Show(BaseModel):
    """
    Contains season/episode data of TV Series
    """
    media = ForeignKeyField(Media, null=True)
    season = IntegerField()
    episode = IntegerField()
    title = CharField(unique=True)  # Episode Title
    extra = CharField()

    class Meta:
        db_table = 'show'


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
    path = CharField(unique=True)

    class Meta:
        db_table = 'directory'


class List(BaseModel):
    """
    Contains all the lists and their relations with media
    """
    name = CharField()
    medias = ManyToManyField(Media, related_name='lists')
