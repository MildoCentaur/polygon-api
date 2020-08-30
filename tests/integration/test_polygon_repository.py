from models.polygon import Polygon
from repository.polygon_repository import PolygonRepository
from services.polygon_services import PolygonSerializer
from tests.integration.base_test import BaseTest
from tests.test_constants import GEOMETRY, INVALID_GEOMETRY, OPEN_GEOMETRY
from utilities.db import db


class PolygonRepositoryTest(BaseTest):


    def test_find_by_properties(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_by_properties('{"property2":"value21","property5":"value5"}')
            expected = ['testPolygon2']
            polygons = list(polygons)
            self.assertEqual(len(polygons), len(expected))

    def test_find_intersected_area(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_intersected_area('POLYGON((5 2, 7 6, 9 5, 5 2))')
            expected = ['PolygonWithHole', 'testPolygon3', 'testPolygon2']
            polygons = list(polygons)
            self.assertEqual(len(polygons), len(expected))

            for i in range(len(expected)):
                self.assertEqual(polygons[i].name, expected[i])
                self.assertIsNotNone(polygons[i].intersected)

    def test_find_by_area_intersects_areas(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_by_area('POLYGON((5 2, 7 6, 9 5, 5 2))')
            expected = ['PolygonWithHole', 'testPolygon3', 'testPolygon2']
            polygon_names = [polygon.name for polygon in polygons]
            self.assertListEqual(polygon_names, expected,
                                 "Expected list should be equal to the retrieved list of names.")

    def test_find_by_area_no_intersect(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_by_area('POLYGON((25 22, 27 26, 29 25, 25 22))')
            expected = []
            polygon_names = [polygon.name for polygon in polygons]
            self.assertListEqual(polygon_names, expected,
                                 "Expected list should be equal to the retrieved list of names.")

    def test_find_like_name(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_like_name('olygon')
            expected = ['Polygon', 'PolygonWithHole', 'testPolygon2', 'testPolygon3']

            polygon_names = [polygon.name for polygon in polygons]
            self.assertListEqual(polygon_names, expected,
                                 "Expected list should be equal to the retrieved list of names.")

    def test_find_like_name_returns_empty(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygons = repository.find_like_name('alejandro')
            expected = []
            self.assertListEqual(list(polygons), expected,
                                 "Expected list should be equal to the retrieved list of names.")

    def test_find_by_name_with_expected_name(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = repository.find_by_name('Polygon')
            self.assertIsNotNone(polygon, "Expected to find an area.")
            self.assertEquals(polygon.name, "Polygon", "Expected to find an area with name Polygon.")

    def test_serializer(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = repository.find_by_name('Polygon')
            serializer = PolygonSerializer(repository)
            print(serializer.serilize(polygon))

    def test_find_by_name_with_not_expected_name(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            polygon = repository.find_by_name('alejandro')
            self.assertIsNone(polygon, "It was not expected to find an area.")

    def test_is_valid_simple_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            geometry = {"type": "Polygon", "coordinates": [[[0, 4], [4, 4], [7, 2], [0, 4]]]}
            valid = repository.is_closed_polygon(geometry)
            self.assertTrue(valid, "It was expected to be valid.")

    def test_is_valid_complex_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            geometry = {"type": "Polygon", "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],
                                                           [[2, 2], [2, 4], [4, 4], [4, 2], [2, 2]],
                                                           [[5.5, 5.5], [5, 7], [7, 5], [5.5, 5.5]]]}
            valid = repository.is_closed_polygon(geometry)
            self.assertTrue(valid, "It was expected to be valid.")

    def test_is_valid_open_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            valid = repository.is_closed_polygon(OPEN_GEOMETRY)
            self.assertFalse(valid, "It was expected to be invalid.")

    def test_is_valid_invalid_polygon(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            valid = repository.is_closed_polygon(INVALID_GEOMETRY)
            self.assertFalse(valid, "It was expected to be invalid.")

    def test_crud(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            geom = repository.geojson_to_geo(GEOMETRY)
            polygon = Polygon('testpolygon3', "2020-08-21T18:25:43", geom,
                              {"prop1": "value1", "prop2": "value2"})
            saved = repository.save(polygon)
            self.assertIsNotNone(saved, "Expected to save the polygon.")
            self.assertEqual(saved, polygon, "saved polygon to be equal to the original.")

            retrieved = repository.find_by_name(polygon.name)
            self.assertEqual(retrieved, saved, "retrieved polygon to be equal to the saved.")

            repository.delete(polygon.name)
            retrieved = repository.find_by_name(polygon.name)
            self.assertIsNone(retrieved, "Polygon not expected to be found.")
