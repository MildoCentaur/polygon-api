from typing import Dict, List

from app.models.polygon import Polygon
from app.repository.polygon_repository import PolygonRepository
from app.utilities.constants import DATE_FORMAT


class PolygonRegistrator:
    def __init__(self, repository: PolygonRepository):
        self.repository = repository

    def register(self, data: Dict) -> Polygon:
        geom = self.repository.geojson_to_geo(data["area"])
        polygon = Polygon(data["name"], data["date"], geom, data["properties"])
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


class PolygonQuerySolver:

    def __init__(self, repository: PolygonRepository, serializer: PolygonSerializer):
        self.repository = repository
        self.serializer = serializer

    def query(self, args):
        dispatcher = {"name": self.search_name,
                      "intersect": self.search_intersect,
                      "intersection": self.search_intersection,
                      "properties": self.search_properties}

        key = list(args.keys())[0]
        try:
            result = dispatcher[key](args)
        except KeyError:
            result = {'message': 'Invalid search criteria'}, 400

        return result

    def search_properties(self, args) -> List[Dict]:
        results = self.repository.find_by_properties(args["properties"])
        return self.serialize_polygon_results(results)

    def serialize_polygon_results(self, results) -> List[Dict]:
        return [self.serializer.serialize(result) for result in results] if results is not None else []

    def search_name(self, args) -> List[Dict]:
        results = self.repository.find_like_name(args["name"])
        return self.serialize_polygon_results(results)

    def search_intersect(self, args) -> List[Dict]:
        results = self.repository.find_by_area(args["intersect"])
        return self.serialize_polygon_results(results)

    def search_intersection(self, args) -> List[Dict]:
        results = self.repository.find_intersected_area(args["intersection"])
        return [self.serializer.serialize_area(result) for result in results] if results is not None else []
