import re
from typing import List

from models.polygon import Polygon


class PolygonRepository:
    def __init__(self, session) -> None:
        self.session = session

    def find_by_name(self, name: str) -> Polygon:
        return Polygon.query.filter_by(name=name).first()

    def is_closed_polygon(self, polygon_points: List[str]) -> bool:
        # query = session.query(Lake.name,
        # ...                       func.ST_Area(func.ST_Buffer(Lake.geom, 2)) \
        # ...                           .label('bufferarea'))
        # >>> for row in query:
        # ...     print '%s: %f' % (row.name, row.bufferarea)
        pattern = re.compile("[0-9,]+")
        complete_polygon = ''
        for polygon in polygon_points:
            if not pattern.match(polygon):
                return False
            complete_polygon += '({0})'.format(polygon)

        is_polygon = self.session.execute(
            'select ST_isclosed(ST_GeomFromText(\'POLYGON(({0}))\'))'.format(polygon_points[0]))

        return list(is_polygon)[0]

    def save(self, polygon: Polygon) -> Polygon:
        self.session.add(polygon)
        self.session.commit()
        return self.find_by_name(polygon.name)

    def delete(self, name: str) -> None:
        polygon = self.find_by_name(name)
        if polygon is not None:
            self.session.delete(polygon)
            self.session.commit()

# Validate is a close polygon
# SELECT ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');
