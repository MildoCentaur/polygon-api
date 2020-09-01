import logging

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import DatabaseError

logging.basicConfig(level=logging.INFO)


class PolygonResource(Resource):

    def __init__(self, **kwargs):
        self.serializer = kwargs['serializer']
        self.registrator = kwargs['registrator']
        self.query_solver = kwargs['query_solver']
        self.eraser = kwargs['eraser']
        self.validator = kwargs['validator']

    def get(self):
        args = request.args.to_dict()
        logging.info('request_data {0}'.format(args))

        if len(args.keys()) > 1:
            return {'message': 'Invalid search criteria'}, 400
        try:
            return self.query_solver.query(args)
        except DatabaseError:
            return {"message": "Database error"}, 500

    def delete(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))
        try:
            self.eraser.delete(posted_data["name"])
        except DatabaseError:
            return {"message": "Database error"}, 500
        return {"message": "Area deleted successful"}

    def post(self):
        posted_data = request.get_json()
        logging.info('posted_data {0}'.format(posted_data))

        try:
            if not self.validator.validate(posted_data):
                return {"message": "Invalid payload"}, 500
            self.registrator.register(posted_data)
        except DatabaseError:
            return {"message": "Database error"}, 500
        return {"message": "Area saved correctly"}

