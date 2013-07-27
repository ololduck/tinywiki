from flask import render_template

from wiki import app

@app.route('/')
def home():
    return 'hello'
