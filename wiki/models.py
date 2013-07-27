import markdown

from wiki import db, app

class WikiPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    content = db.Column(db.Text)

    def __init__(self, content):
        self.title = WikiPage.gen_title(content)
        self.content = content


    def __repr__(self):
        return '<WikiPage:%s>' % self.title


    @classmethod
    def gen_title(a, content):
        first_line = content.split('\n')[0]
        if(first_line[0:1] == '# '):
            first_line = first_line[2:]
        elif(first_line[0] == '#'):
            first_line = first_line[1:]
        return first_line


    def save(self):
        search = self.__class__.query.filter_by(title=self.title).all()
        print(search)
        if(search != [] and self.id != search[0].id):
            raise Exception('Another model with the same id already exists in db')
        db.session.add(self)
        db.session.commit()

    def html(self):
        html = markdown.markdown(self.content, extensions=app.config['MARKDOWN_EXTS'])
        return html

