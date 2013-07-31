import markdown
import re
from wiki import db, app
from sqlalchemy.exc import OperationalError


def get_page(title):
    try:
        return WikiPage.query.filter_by(title=title).first()
    except OperationalError as e:
        from wiki import init_db
        init_db()


def get_all_page_titles():
    a = WikiPage.query.all()
    titles = []
    for page in a:
        titles.append(page.title)
    return titles


class WikiPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    content = db.Column(db.Text)
    title_regex = re.compile(r'([A-Z][a-z]*)+')

    def __init__(self, content):
        self.title = WikiPage.gen_title(content)
        self.content = content


    def __repr__(self):
        return '<WikiPage:%s>' % self.title


    @classmethod
    def gen_title(a, content):
        if('\n' in content):
            first_line = content.split('\n')[0]
        else:
            first_line = content
        if('\r' in content):
            first_line = content.split('\r')[0]
        else:
            first_line = content
        first_line = first_line[first_line.find('#')+1:]
        first_line = first_line.strip(' ')
        match = a.title_regex.match(first_line)
        if(match == None):
            raise ValidationError("Given title (%s) does not match '^([A-Z][a-z]*)+$' !" % first_line)
        return first_line


    def save(self):
        search = self.__class__.query.filter_by(title=self.title).all()
        if(search != [] and self.id != search[0].id):
            raise ValidationError('Another model with a different id already exists in db')
        db.session.add(self)
        db.session.commit()

    def html(self):
        html = markdown.markdown(self.content, extensions=app.config['MARKDOWN_EXTS'])
        return html

class ValidationError(Exception):
    pass

