import datetime
import logging
from typing import List, Dict

from app.repository.polygon_repository import PolygonRepository
from app.utilities.constants import DATE_FORMAT


def check_expected_parameters(expected: List, parameters: Dict) -> bool:
    if parameters is None:
        return False

    for element in expected:
        if element not in parameters.keys():
            return False
    return True


def is_valid_property_dict(element: Dict) -> bool:
    if isinstance(element, dict):
        return True
    return False


def is_valid_date(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        return False
    return True


def is_valid_name(name: str) -> bool:
    return name.isalnum()


class SavePolygonValidator:

    def __init__(self, polygon_repository: PolygonRepository):
        self.repository = polygon_repository

    def validate(self, posted_data: Dict) -> bool:
        expected_parameters = ["name", "area", "date", "properties"]
        if not check_expected_parameters(expected_parameters, posted_data):
            logging.error("Invalid parameters - too many parameters")
            return False

        if not is_valid_name(posted_data["name"]):
            logging.error("Invalid parameters - invalid name")
            return False

        if self.is_name_taken(posted_data["name"]):
            logging.error("Invalid parameters - name taken")
            return False

        if not is_valid_date(posted_data["date"]):
            logging.error("Invalid parameters - invalid date")
            return False

        if not is_valid_property_dict(posted_data["properties"]):
            logging.error("Invalid parameters - properties")
            return False

        if not self.is_valid_polygon(posted_data["area"]):
            logging.error("Invalid parameters - invalid polygon")
            return False

        return True

    def is_valid_polygon(self, polygon: Dict) -> bool:
        """This method evaluates if the polygon received is closed or not.
            The received polygon may contain holes that is why a list is received"""
        return self.repository.is_closed_polygon(polygon)

    def is_name_taken(self, name: str) -> bool:
        result = self.repository.find_by_name(name)
        if result is None:
            return False
        return True
