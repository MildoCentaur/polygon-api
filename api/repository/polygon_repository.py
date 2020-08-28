from typing import List

from models.polygon import Polygon


class PolygonRepository:
    def __init__(self, session) -> None:
        self.session = session

    def find_by_name(self, name: str) -> Polygon:
        return Polygon.query.filter_by(name=name).first()

    def is_closed_polygon(self, polygon_points: List[str]) -> bool:
        return len(list(self.session.execute('ST_GeomFromText("POLYGON({0})")'.format(polygon_points)))) > 0

    def save(self, polygon: Polygon):
        pass

    def delete(self, name: str):
        pass

# Validate is a close polygon
# SELECT ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
