"""
BaseTest

This class should be the parent class to each non-unit tests.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase

from app.app import app
from app.utilities.db import db


class BaseTest(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.init_app(app)
        self.app = app.test_client()
        self.app_context = app.app_context
