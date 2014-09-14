from flask import Flask

def create_app(config_override=None):
    application = Flask(__name__)

    import config
    application.config.from_object(config)
    application.config.from_object(config_override)

    from models import db
    db.init_app(application)

    from blueprints.api import api
    api.init_app(application)

    import assets
    assets.init_assets(application)

    import blueprints
    for blueprint in blueprints.blueprints:
        application.register_blueprint(blueprint)

    import util
    util.init_app(application)

    return application
