from flask.ext.script import Manager, Server
from models import db
from app import application

manager = Manager(application)

manager.add_command("runserver", Server(host=application.config.get("HOST", "0.0.0.0"), port=application.config.get("PORT", 5000), use_evalex=application.config.get("DEBUG_SHELL")))


@manager.command
def init_db():
    if not application.config.get("SQLALCHEMY_DATABASE_URI"):
        print("Please set the database URI in the config file first.")
        exit(-1)

    db.create_all()
    print("Database successfully initalized.")


@manager.command
def print_routes():
    for rule in application.url_map.iter_rules():
        print rule, rule.endpoint



if __name__ == "__main__":
    manager.run()
