import logging

from binstar_client import ServerError
from flask import request, jsonify
from flask_restful import Resource

from db import db
from repository.polygon_repository import PolygonRepository
from services.polygon_services import RegisterPolygon
from services.validator import SavePolygonValidator

logging.basicConfig(level=logging.INFO)


class PolygonResource(Resource):

    def get(self):
        """ tTBD"""
        pass

    def delete(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))
        dao = PolygonRepository(db.session)
        try:
            dao.delete(posted_data)
        except ConnectionError:
            raise ServerError("Error message", '301', {"error": "mensaje", 'error2': 'mensaje2'})

        return jsonify(), 200

    def post(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))

        dao = PolygonRepository(db.session)
        registrator = RegisterPolygon(dao)
        validator = SavePolygonValidator(dao)

        if not validator.validate(posted_data):
            return jsonify(), 400

        try:
            polygon = registrator.register(posted_data)
        except ConnectionError:
            raise ServerError("Error message", '301', {"error": "mensaje", 'error2': 'mensaje2'})

        return jsonify(polygon), 200

# query_parameters = request.args
#
#     id = query_parameters.get('id')
#     published = query_parameters.get('published')
#     author = query_parameters.get('author')
