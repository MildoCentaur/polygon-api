from typing import Dict

from models.polygon import Polygon
from repository.polygon_repository import PolygonRepository


class RegisterPolygon:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def register(self, data: Dict) -> Polygon:
        return self.repository.save(data)


class DeleterPolygon:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def delete(self, name: str) -> Polygon:
        return self.repository.delete(name)
