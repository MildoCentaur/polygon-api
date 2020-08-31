import logging

from flask import request
from flask_restful import Resource

from repository.polygon_repository import PolygonRepository
from services.polygon_services import PolygonRegistrator, PolygonSerializer, PolygonQuerySolver
from services.validator import SavePolygonValidator
from utilities.db import db

logging.basicConfig(level=logging.INFO)


class PolygonResource(Resource):

    def get(self):
        args = request.args.to_dict()
        logging.info('request_data {0}'.format(args))

        if len(args.keys()) > 1:
            return {'message': 'Invalid search criteria'}, 400

        repository = PolygonRepository(db.session)
        serializer = PolygonSerializer(repository)
        polygon_query_solver = PolygonQuerySolver(repository, serializer)

        return polygon_query_solver.query(args)

    def delete(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))
        repository = PolygonRepository(db.session)
        try:
            repository.delete(posted_data["name"])
        except ConnectionError:
            return {"message": "Database error"}, 500

        return {"message": "Area deleted successful"}

    def post(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))

        repository = PolygonRepository(db.session)
        registrator = PolygonRegistrator(repository)
        validator = SavePolygonValidator(repository)

        if not validator.validate(posted_data):
            return {"message": "Invalid payload"}, 500

        try:
            registrator.register(posted_data)
        except ConnectionError:
            return {"message": "Database error"}, 500

        return {"message": "Area saved correctly"}

