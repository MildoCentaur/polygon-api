from typing import Dict

from models.polygon import Polygon
from repository.polygon_repository import PolygonRepository


class RegisterPolygon:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def register(self, data: Dict) -> Polygon:
        polygon = Polygon(data["name"], data["date"], data["are"], data["properties"])
        return self.repository.save(polygon)


class DeleterPolygon:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def delete(self, name: str) -> None:
        self.repository.delete(name)
