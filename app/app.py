import logging
import os

from flask import Flask
from flask_restful import Api

from app.repository.polygon_repository import PolygonRepository
from app.resources.polygon_resource import PolygonResource
from app.services.polygon_services import PolygonSerializer, PolygonRegistrator, PolygonQuerySolver, PolygonEraser
from app.services.validator import SavePolygonValidator
from app.utilities.db import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:mysecretpassword@polygon-api_postgis_1:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
repository = PolygonRepository(db.session)
serializer = PolygonSerializer(repository)
registrator = PolygonRegistrator(repository)
query_solver = PolygonQuerySolver(repository, serializer)
eraser = PolygonEraser(repository)
validator = SavePolygonValidator(repository)

api.add_resource(PolygonResource, "/area", resource_class_kwargs={'serializer': serializer,
                                                                  'registrator': registrator,
                                                                  'query_solver': query_solver,
                                                                  'eraser': eraser,
                                                                  'validator': validator})


def initialize_application():
    db.init_app(app)
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    initialize_application()
