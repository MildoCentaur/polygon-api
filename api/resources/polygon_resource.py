import logging

from flask import request
from flask_restful import Resource

from repository.polygon_repository import PolygonRepository
from services.polygon_services import PolygonRegistrator, PolygonSerializer
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
        # try:
        if "name" in args.keys():
            results = repository.find_like_name(args["name"])
        elif "intersect" in args.keys():
            results = repository.find_by_area(args["intersect"])
        elif "intersection" in args.keys():
            results = repository.find_intersected_area(args["intersection"])
            return [serializer.serialize_area(result) for result in results] if results is not None else []
        elif "properties" in args.keys():
            results = repository.find_by_properties(args["properties"])
        else:
            return {'message': 'Invalid search criteria'}, 400

        return [serializer.serialize(result) for result in results] if results is not None else []
        # except BaseException ex:
        #     return {'message': 'Invalid search data'}, 400

    def delete(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))
        dao = PolygonRepository(db.session)
        try:
            dao.delete(posted_data["name"])
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

# query_parameters = request.args
#
#     id = query_parameters.get('id')
#     published = query_parameters.get('published')
#     author = query_parameters.get('author')
