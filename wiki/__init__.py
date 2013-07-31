from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from wiki import config

app = Flask(__name__)
app.config.from_object(config)

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
