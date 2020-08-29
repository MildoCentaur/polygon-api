from unittest.mock import MagicMock

import pytest

from models.polygon import Polygon
from services.validator import SavePolygonValidator, is_valid_name
from tests.test_constants import *


@pytest.fixture
def mock_dao():
    mock_dao = MagicMock()
    return mock_dao


@pytest.fixture
def validator(mock_dao):
    return SavePolygonValidator(mock_dao)


@pytest.mark.usefixtures("validator")
def test_save_polygon_validator_exists():
    assert validator is not None


def test_validate_correct_polygon(validator, mock_dao):
    posted_data = {"area": DUMMY_POLYGON,
                   "name": DUMMY_VALID_NAME,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_dao.find_by_name = MagicMock(return_value=None)
    mock_dao.is_closed_polygon = MagicMock(return_value=True)
    assert validator.validate(posted_data)


def test_validate_wrong_polygon(validator, mock_dao):
    posted_data = {"area": DUMMY_POLYGON,
                   "name": DUMMY_VALID_NAME,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_dao.find_by_name = MagicMock(return_value=None)
    mock_dao.is_closed_polygon = MagicMock(return_value=False)
    assert not validator.validate(posted_data)


def test_validate_valid_name_ok():
    assert is_valid_name(DUMMY_VALID_NAME)


def test_validate_valid_name_fail():
    assert not is_valid_name(DUMMY_INVALID_NAME)


def test_validate_name_not_taken(validator, mock_dao):
    name = "dummy_name"
    mock_dao.find_by_name = MagicMock(return_value=None)
    assert not validator.is_name_taken(name)


def test_validate_name_taken(validator, mock_dao):
    name = "duplicated"
    duplicated_polygon = Polygon(name, "2020-04-21T18:25:43", "DUMMY_POLYGON", {})
    mock_dao.find_by_name = MagicMock(return_value=duplicated_polygon)
    assert validator.is_name_taken(name)


def test_validate_closed_polygon_with_multipolygon(validator, mock_dao):
    polygon_json = ["(0 0, 10 0, 10 10, 0 10, 0 0)", "(1 1, 1 2, 2 2, 2 1, 1 1)"]
    mock_dao.is_closed_polygon = MagicMock(return_value=True)
    assert validator.is_valid_polygon(polygon_json)


def test_validate_closed_polygon_with_simple_multipolygon(validator, mock_dao):
    polygon_json = ["(0 0, 10 0, 10 10, 0 10, 0 0)"]
    mock_dao.is_closed_polygon = MagicMock(return_value=True)
    assert validator.is_valid_polygon(polygon_json)


def test_validate_closed_polygon_with_simple_open_polygon(validator, mock_dao):
    polygon_json = ["(0 0, 10 0, 10 10, 0 10, 0 1)"]
    mock_dao.is_closed_polygon = MagicMock(return_value=False)
    assert not validator.is_valid_polygon(polygon_json)
