#!/usr/bin/env python
from wiki import app

import os
basedir = os.path.abspath(os.path.dirname(__file__))
dbpath = os.path.join(basedir, 'wiki.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbpath

if(not os.path.exists(dbpath)):
    from wiki import db
    db.create_all()

app.run(debug = True)
