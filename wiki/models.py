from wiki import db

class WikiPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content


    def __repr__(self):
        return '<WikiPage: %s' % self.title


    def gen_title(content):
        first_line = content.split('\n')[0]
        return first_line


    def save(self):
        search = self.__class__.query.filter_by(title=self.title)
        if(searh != None and self.id != search.id):
            raise Exception('Another model with the same id already exists in db')
        db.session.add(self)
        db.session.commit()

