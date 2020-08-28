import pytest

from resources.polygon_resource import PolygonResource


@pytest.fixture()
def setup():
    polygon = PolygonResource()
    return polygon


def test_add_polygon_with_empty_parameters():
    # polygon.post()
    pass
