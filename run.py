#from flup.server.fcgi import WSGIServer
from nerdnu import app

if __name__ == '__main__':
    #WSGIServer(app, bindAddress='/tmp/nerd-fcgi.sock', umask=777).run()
    app.run()
