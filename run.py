#!/usr/bin/env python
from wiki import app

import os
basedir = os.path.abspath(os.path.dirname(__file__))

if "DATABASE_URL" in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
else:
    dbpath = os.path.join(basedir, 'wiki.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbpath

app.run(debug=True)
