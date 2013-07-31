import os
basedir = os.path.abspath(os.path.dirname(__file__))

MARKDOWN_EXTS = [
    'extra',
    'nl2br',
    'wikilinks',
    'headerid',
    'codehilite',
    'admonition'
]

if "DATABASE_URL" in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
else:
    dbpath = os.path.join(basedir, 'wiki.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbpath
