from . import db

class Revision(db.Model):
    revision = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.String(10), primary_key=True)
    start = db.Column(db.DateTime())
    stop = db.Column(db.DateTime())

    def __init__(self, revision, server, start, stop):
        self.revision = revision
        self.server = server
        self.start = start
        self.stop = stop

    def __repr__(self):
        return '<Revision %r - %r>' % (self.revision, self.server)
