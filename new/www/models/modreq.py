from . import db

class Modreq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.String(10), primary_key=True, index=True)
    status = db.Column(db.String(10))
    request_by = db.Column(db.String(16))
    response_by   = db.Column(db.String(16))
    request_text = db.Column(db.String(200))
    response_text = db.Column(db.String(200))

    def __init__(self, id, server, status, request_by, response_by, request_text, response_text):
        self.id = id
        self.server = server
        self.status = status
        self.request_by = request_by
        self.response_by = response_by
        self.request_text = request_text
        self.response_text = response_text

    def __repr__(self):
        return '<Modreq %s #%d>' % (self.server, self.id)
