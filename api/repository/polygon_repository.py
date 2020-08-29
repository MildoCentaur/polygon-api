import re
from typing import List

from models.polygon import Polygon


class PolygonRepository:
    def __init__(self, session) -> None:
        self.session = session

    def find_by_name(self, name: str) -> Polygon:
        return self.session.query(Polygon).filter_by(name=name).first()

    def find_like_name(self, name: str) -> List[Polygon]:
        search = "%{}%".format(name)
        return self.session.query(Polygon).filter(Polygon.name.like(search)).order_by(Polygon.name)

    def is_closed_polygon(self, polygon_points: List[str]) -> bool:
        pattern = re.compile("[0-9,. ]+")
        for polygon in polygon_points:
            if not pattern.fullmatch(polygon):
                return False
        complete_polygon = ",".join(["({0})".format(polygon) for polygon in polygon_points])
        try:
            is_polygon = self.session.execute(
                'select ST_isclosed(ST_GeomFromText(\'POLYGON({0})\'))'.format(complete_polygon))
        except BaseException:
            return False

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
