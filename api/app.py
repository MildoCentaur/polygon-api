import logging
import os

from flask import Flask
from flask_restful import Api

from resources.polygon_resource import PolygonResource
from utilities.db import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:mysecretpassword@polygon-api_postgis_1:5432/postgres')
#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(PolygonResource, "/area")


def initialize_application():
    db.init_app(app)
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    initialize_application()
