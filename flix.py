#!/usr/bin/env python
from models import database, Media, Show, File, Directory, List
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    database.create_tables([Media, Show, File, Directory, List], safe=True)
    app.run()
