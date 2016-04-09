#!/usr/bin/python3
import os

from app import create_app,db
from app.models import Family,Doctor,Member,Sensor,Ship,App
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,db=db,Family=Family,Doctor=Doctor,Member=Member,Sensor=Sensor,Ship=Ship,App=App)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
