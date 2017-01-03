#!/usr/bin/env python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('test.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])
    # return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

