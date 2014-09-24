from . import db

class PlayerTime(db.Model):
    playername = db.Column(db.String(16), primary_key=True, index=True)
    server = db.Column(db.String(10), primary_key=True)
    seconds = db.Column(db.Integer)

    def __init__(self, playername, server, seconds):
        self.playername = playername
        self.server = server
        self.seconds = seconds

    def __repr__(self):
        return '<PlayerTime %r, %r - %rs>' % (self.playername, self.server, self.seconds)
