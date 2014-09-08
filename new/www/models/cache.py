from . import db

class Cache(db.Model):
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Cache %r>' % self.key
