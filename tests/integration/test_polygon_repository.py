from db import db
from repository.polygon_repository import PolygonRepository
from tests.integration.base_test import BaseTest


class PolygonRepositoryTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            repository = PolygonRepository(db.session)
            self.assertIsNotNone(repository.find_by_name('Polygon'),
                                 "Found an item with name Polygon, but expected not to.")

            # item.save_to_db()
            #
            # self.assertIsNotNone(ItemModel.find_by_name('tests'))
            #
            # item.delete_from_db()
            #
            # self.assertIsNone(ItemModel.find_by_name('tests'))
