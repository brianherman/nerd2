import config

import sys
args = sys.argv[1:]

usage = "usage: python run.py <www|scrape>"

if len(args) != 1:
    print usage
elif args[0] == 'www':
    print "please use manage.py in www/"
    #from www import create_app
    #app = create_app(config)
    #app.run(
    #    app.config.get("HOST", "0.0.0.0"),
    #    app.config.get("PORT", 5000),
    #    use_evalex=("DEBUG_SHELL", True))
elif args[0] == 'scrape':
    from scrape.app import app
    app.config = config
    app.run()
else:
    print usage
