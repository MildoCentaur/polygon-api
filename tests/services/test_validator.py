from unittest.mock import MagicMock

import pytest

from app.models.polygon import Polygon
from app.services.validator import SavePolygonValidator, is_valid_name
from tests.test_constants import DUMMY_POLYGON, DUMMY_VALID_NAME, DUMMY_DATE, DUMMY_INVALID_NAME, GEOMETRY, \
    OPEN_GEOMETRY, DUMMY_INVALID_DATE, VALID_AREA


@pytest.fixture
def mock_repository():
    repository = MagicMock()
    return repository


@pytest.fixture
def validator(mock_repository):
    return SavePolygonValidator(mock_repository)


@pytest.mark.usefixtures("validator")
def test_save_polygon_validator_exists():
    assert validator is not None


def test_validate_correct_polygon(validator, mock_repository):
    posted_data = {"area": DUMMY_POLYGON,
                   "name": DUMMY_VALID_NAME,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_repository.find_by_name = MagicMock(return_value=None)
    mock_repository.is_closed_polygon = MagicMock(return_value=True)
    assert validator.validate(posted_data)


def test_validate_correct_parameters(validator):
    posted_data = {"invalid": DUMMY_POLYGON,
                   "parameters": DUMMY_VALID_NAME,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}

    assert not validator.validate(posted_data)


def test_validate_invalid_name(validator):
    posted_data = {"name": DUMMY_INVALID_NAME,
                   "area": VALID_AREA,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}

    assert not validator.validate(posted_data)


def test_validate_name_taken_by_validator(validator, mock_repository):
    posted_data = {"name": DUMMY_VALID_NAME,
                   "area": VALID_AREA,
                   "date": DUMMY_INVALID_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_repository.find_by_name = MagicMock(return_value=DUMMY_VALID_NAME)
    assert not validator.validate(posted_data)


def test_validate_invalid_date(validator, mock_repository):
    posted_data = {"name": DUMMY_VALID_NAME,
                   "area": VALID_AREA,
                   "date": DUMMY_INVALID_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_repository.find_by_name = MagicMock(return_value=None)
    assert not validator.validate(posted_data)


def test_validate_wrong_polygon(validator, mock_repository):
    posted_data = {"area": DUMMY_POLYGON,
                   "name": DUMMY_VALID_NAME,
                   "date": DUMMY_DATE,
                   "properties": {"prop1": "value1", "prop2": "value2"}}
    mock_repository.find_by_name = MagicMock(return_value=None)
    mock_repository.is_closed_polygon = MagicMock(return_value=False)
    assert not validator.validate(posted_data)


def test_validate_valid_name_ok():
    assert is_valid_name(DUMMY_VALID_NAME)


def test_validate_valid_name_fail():
    assert not is_valid_name(DUMMY_INVALID_NAME)


def test_validate_name_not_taken(validator, mock_repository):
    name = "dummy_name"
    mock_repository.find_by_name = MagicMock(return_value=None)
    assert not validator.is_name_taken(name)


def test_validate_name_taken(validator, mock_repository):
    name = "duplicated"
    duplicated_polygon = Polygon(name, "2020-04-21T18:25:43", "DUMMY_POLYGON", {})
    mock_repository.find_by_name = MagicMock(return_value=duplicated_polygon)
    assert validator.is_name_taken(name)


def test_validate_closed_polygon_with_multipolygon(validator, mock_repository):
    polygon_json = GEOMETRY
    mock_repository.is_closed_polygon = MagicMock(return_value=True)
    assert validator.is_valid_polygon(polygon_json)


def test_validate_closed_polygon_with_simple_multipolygon(validator, mock_repository):
    polygon_json = GEOMETRY
    mock_repository.is_closed_polygon = MagicMock(return_value=True)
    assert validator.is_valid_polygon(polygon_json)


def test_validate_closed_polygon_with_simple_open_polygon(validator, mock_repository):
    polygon_json = OPEN_GEOMETRY
    mock_repository.is_closed_polygon = MagicMock(return_value=False)
    assert not validator.is_valid_polygon(polygon_json)
