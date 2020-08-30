from typing import Dict

from models.polygon import Polygon
from repository.polygon_repository import PolygonRepository
from utilities.constants import DATE_FORMAT


class PolygonRegistrator:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def register(self, data: Dict) -> Polygon:
        polygon = Polygon(data["name"], data["date"], data["area"], data["properties"])
        return self.repository.save(polygon)


class PolygonEraser:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def delete(self, name: str) -> None:
        self.repository.delete(name)


class PolygonSerializer:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def serialize(self, polygon: Polygon) -> Dict:
        data = {
            'name': polygon.name,
            'date': polygon.date.strftime(DATE_FORMAT),
            'properties': polygon.properties,
            'geom': self.repository.to_geo_json(polygon.geom)
        }
        return data

    def serialize_area(self, intersected_area: object) -> Dict:
        data = {
            'geom': self.repository.to_geo_json(intersected_area.intersected)
        }
        return data
