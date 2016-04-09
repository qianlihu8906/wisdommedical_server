from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config,basedir
from flask.ext.uploads import UploadSet,configure_uploads,IMAGES

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES,lambda app:basedir+'/static')


def create_app(config_name):
    app = Flask(__name__)
    configure_uploads(app,photos)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .api_0_1 import api as api_0_1_blueprint
    app.register_blueprint(api_0_1_blueprint,url_prefix='/api/v0.1')

    return app
