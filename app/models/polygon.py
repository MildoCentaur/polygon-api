from datetime import datetime
from typing import Dict

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, JSON

from app.utilities.constants import DATE_FORMAT
from app.utilities.db import db


class Polygon(db.Model):
    __tablename__ = 'areas'
    name = Column(String, primary_key=True)
    date = Column(Date)
    geom = Column(Geometry('POLYGON', srid=4326))
    properties = Column(JSON)

    def __init__(self, name: str, date: str, geom: object, properties: Dict):
        self.name = name
        self.date = datetime.strptime(date, DATE_FORMAT)
        self.geom = geom
        self.properties = properties
