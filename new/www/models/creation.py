from . import db

class Creation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    server = db.Column(db.String(10), primary_key=True, index=True)
    revision = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, primary_key=True)
    z = db.Column(db.Integer, primary_key=True)

    def __init__(self, name, server, revision, x, z):
        self.name = name
        self.server = server
        self.revision = revision
        self.x = x
        self.z = z

    def __repr__(self):
        return '<Creation %r, %r r%r>' % (self.name, self.server, self.revision)
