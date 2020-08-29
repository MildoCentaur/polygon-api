from db import db
from models.polygon import Polygon
from repository.polygon_repository import PolygonRepository
from tests.integration.base_test import BaseTest


class PolygonRepositoryTest(BaseTest):

    def test_find_by_name_with_expected_name(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = repository.find_by_name('Polygon')
            self.assertIsNotNone(polygon, "Expected to find an area.")
            self.assertEquals(polygon.name, "Polygon", "Expected to find an area with name Polygon.")

    def test_find_by_name_with_not_expected_name(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = repository.find_by_name('alejandro')
            self.assertIsNone(polygon, "It was not expected to find an area.")

    def test_is_valid_simple_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            valid = repository.is_closed_polygon(['0 0,1 0,1 1,0 1,0 0'])
            self.assertTrue(valid, "It was expected to be valid.")

    def test_is_valid_complex_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            valid = repository.is_closed_polygon(
                ['0 0,10 0,10 10,0 10,0 0', '2 2,2 4,4 4,4 2,2 2', '5.5 5.5,5 7,7 7,7 5,5.5 5.5'])
            self.assertTrue(valid, "It was expected to be valid.")

    def test_crud(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = Polygon('testpolygon3', "2020-08-21T18:25:43", 'POLYGON((0 0,1 0,1 1,0 1,0 0))',
                              {"prop1": "value1", "prop2": "value2"})
            saved = repository.save(polygon)
            self.assertIsNotNone(saved, "Expected to save the polygon.")
            self.assertEqual(saved, polygon, "saved polygon to be equal to the original.")

            retrieved = repository.find_by_name(polygon.name)
            self.assertEqual(retrieved, saved, "retrieved polygon to be equal to the saved.")

            repository.delete(polygon.name)
            retrieved = repository.find_by_name(polygon.name)
            self.assertIsNone(retrieved, "Polygon not expected to be found.")
