from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["MARKDOWN_EXTS"] = [
        'extra',
        'nl2br',
        'wikilinks',
        'headerid',
        'codehilite',
        'admonition'
        ]

db = SQLAlchemy(app)

from wiki import views
from wiki import models

