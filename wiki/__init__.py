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
from wiki import base_pages

def init_db():
    db.create_all()

    home = models.WikiPage(base_pages.base_home_page)
    home.save()

    help = models.WikiPage(base_pages.base_help_page)
    help.save()
