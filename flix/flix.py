#!/usr/bin/env python
from flask import Flask, render_template
from .models import Media


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    all_media = Media.select()
    return render_template("index.html",
                           title='Home',
                           all_media=all_media)
