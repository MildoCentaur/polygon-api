import json
from typing import Iterable, List, Dict

from sqlalchemy import func, desc, String, cast

from models.polygon import Polygon


class PolygonRepository:
    def __init__(self, session) -> None:
        self.session = session

    def find_by_properties(self, properties: str) -> Iterable[Polygon]:
        return self.session.query(Polygon).filter(cast(Polygon.properties, String) == properties)

    def find_intersected_area(self, search_area: str) -> Iterable[object]:
        return self.session.query(
            func.ST_Union(func.ST_Intersection(func.ST_GeomFromText(search_area, 4326), Polygon.geom))
            .label('intersected')) \
            .filter(Polygon.geom.ST_Intersects(func.ST_GeomFromText(search_area, 4326)))

    def find_by_area(self, search_area: str) -> Iterable[Polygon]:
        return self.session.query(Polygon).filter(
            Polygon.geom.ST_Intersects(func.ST_GeomFromText(search_area, 4326))) \
            .order_by(desc(func.ST_Area(Polygon.geom)))

    def find_by_name(self, name: str) -> Polygon:
        return self.session.query(Polygon).filter_by(name=name).first()

    def find_like_name(self, name: str) -> List[Polygon]:
        search = "%{}%".format(name)
        return list(self.session.query(Polygon).filter(Polygon.name.like(search)).order_by(Polygon.name))

    def is_closed_polygon(self, geometry: Dict) -> bool:
        try:
            is_closed = self.session.query(
                func.ST_isclosed(func.ST_GeomFromGeoJSON(json.dumps(geometry))).label('closed')).one().closed
        except BaseException:
            return False

        return is_closed

    def save(self, polygon: Polygon) -> Polygon:
        self.session.add(polygon)
        self.session.commit()
        return self.find_by_name(polygon.name)

    def delete(self, name: str) -> None:
        polygon = self.find_by_name(name)
        if polygon is not None:
            self.session.delete(polygon)
            self.session.commit()

    def to_geo_json(self, geom: object) -> Dict:
        result = self.session.query(func.ST_AsGeoJSON(func.ST_Transform(geom, 4326)).label('geoJson')).one().geoJson
        return json.loads(result)

    def geojson_to_geo(self, geometry: Dict) -> object:
        return self.session.query(
            func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(geometry)), 4326).label('geom')).one().geom
