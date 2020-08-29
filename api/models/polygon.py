from datetime import datetime
from typing import Dict

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, JSON

from db import db


class Polygon(db.Model):
    __tablename__ = 'areas'
    name = Column(String, primary_key=True)
    date = Column(Date)
    geom = Column(Geometry('POLYGON'))
    properties = Column(JSON)

    def __init__(self, name: str, date: str, geom: str, properties: Dict):
        self.name = name
        self.date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        self.geom = geom
        self.properties = properties
