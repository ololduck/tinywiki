from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

from wiki import views
from wiki import models

