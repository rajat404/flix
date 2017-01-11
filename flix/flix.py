#!/usr/bin/env python
from flask import Flask, render_template
from .models import Media


app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    all_media = Media.select().where(Media.media_type == 'movie').order_by(-Media.year)
    return render_template("index.html", all_media=all_media)


@app.route('/overflow')
def overflow():
    all_media = Media.select().where(Media.media_type == 'movie').order_by(-Media.year)
    return render_template("overflow.html", all_media=all_media)


@app.route('/table')
def table():
    all_media = Media.select()
    return render_template("table.html", all_media=all_media)


@app.route('/test2')
def test2():
    all_media = Media.select()
    return render_template("test2.html", all_media=all_media)


@app.route('/test3')
def test3():
    all_media = Media.select()
    return render_template("test3.html", all_media=all_media)
