import logging

from flask import request, jsonify
from flask_restful import Resource

from repository.polygon_repository import PolygonRepository
from services.polygon_services import RegisterPolygon
from services.validator import SavePolygonValidator
from utilities.db import db

logging.basicConfig(level=logging.INFO)


class PolygonResource(Resource):

    def get(self):
        args = request.args.to_dict()
        logging.info('posted_data {0}'.format(args))

        if len(args.keys()) > 1:
            return jsonify({"message": "Too many parameters"})

        dao = PolygonRepository(db.session)
        if "name" in args.keys():
            result = dao.find_by_name(args["name"])
        elif "intersect" in args.keys():
            result = dao.find_by_name(args["intersect"])
        elif "intersection" in args.keys():
            result = dao.find_by_name(args["intersection"])
        elif "properties" in args.keys():
            result = dao.find_by_name(args["properties"])
        else:
            result = {'message': 'Invalid search criteria'}

        return jsonify(result)

    def delete(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))
        dao = PolygonRepository(db.session)
        try:
            dao.delete(posted_data["name"])
        except ConnectionError:
            return jsonify({"message": "Database error", "status_code": 500})

        return jsonify({"message": "Area deleted successful"})

    def post(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))

        dao = PolygonRepository(db.session)
        registrator = RegisterPolygon(dao)
        validator = SavePolygonValidator(dao)

        if not validator.validate(posted_data):
            return jsonify({"message": "Invalid payload", "status_code": 500})

        try:
            registrator.register(posted_data)
        except ConnectionError:
            return jsonify({"message": "Database error", "status_code": 500})

        return jsonify({"message": "Area saved correctly"})

# query_parameters = request.args
#
#     id = query_parameters.get('id')
#     published = query_parameters.get('published')
#     author = query_parameters.get('author')
