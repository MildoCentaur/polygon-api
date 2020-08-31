from unittest.mock import MagicMock

from models.polygon import Polygon
from services.polygon_services import PolygonRegistrator, PolygonEraser, PolygonSerializer, PolygonQuerySolver
from tests.test_constants import DUMMY_POLYGON, DUMMY_DATE, GEOMETRY, DUMMY_VALID_NAME, VALID_AREA

DUMMY_POLYGON_OBJECT = Polygon(DUMMY_POLYGON, DUMMY_DATE, GEOMETRY, {})


def test_register():
    mock_repository = MagicMock()
    mock_repository.geojson_to_geo = MagicMock(return_value=None)
    polygon = {"name": DUMMY_POLYGON, "date": DUMMY_DATE, "area": GEOMETRY, "properties": {}}
    expected = Polygon(polygon["name"], polygon["date"], None, polygon["properties"])
    mock_repository.save = MagicMock(return_value=expected)

    registrator = PolygonRegistrator(mock_repository)

    actual = registrator.register(polygon)

    assert actual == expected


def test_eraser():
    mock_repository = MagicMock()
    mock_repository.delete = MagicMock()

    eraser = PolygonEraser(mock_repository)

    eraser.delete(DUMMY_VALID_NAME)

    assert mock_repository.delete.called


def test_serializer():
    mock_repository = MagicMock()
    serializer = PolygonSerializer(mock_repository)
    mock_repository.to_geo_json = MagicMock(return_value=GEOMETRY)

    polygon = DUMMY_POLYGON_OBJECT
    json = serializer.serialize(polygon)
    expected = VALID_AREA

    assert json == expected


def test_serializer_area():
    mock_repository = MagicMock()
    serializer = PolygonSerializer(mock_repository)
    mock_repository.to_geo_json = MagicMock(return_value=GEOMETRY)
    area = MagicMock()
    area.intersected = MagicMock()

    json = serializer.serialize_area(area)
    expected = {'geom': {'type': 'Polygon', 'coordinates': [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]}}

    assert json == expected


def test_query_solver_query_name():
    mock_repository = MagicMock()
    mock_serializer = MagicMock()
    query_solver = PolygonQuerySolver(mock_repository, mock_serializer)
    mock_serializer.serialize = MagicMock()
    mock_repository.find_like_name = MagicMock(return_value=VALID_AREA)
    json = serializer.serialize_area(area)
    expected = {'geom': {'type': 'Polygon', 'coordinates': [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]}}

    assert json == expected
