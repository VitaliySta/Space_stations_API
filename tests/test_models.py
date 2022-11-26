import pytest

from datetime import datetime, timezone

from stations.models import Move, Station
from users.models import User


@pytest.mark.django_db
def test_create_user(user):
    """Тест создания объекта модели пользователя"""

    test_user = User.objects.last()
    assert test_user.username == 'TestUser'
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_station_create(station):
    """Тест создания объекта модели станции"""

    station = Station.objects.last()
    assert station.name == 'TestStation'
    assert station.condition == 'running'
    assert station.date_create.minute == datetime.now(timezone.utc).minute
    assert station.date_crash is None
    assert station.x == 100
    assert station.y == 100
    assert station.z == 100
    assert Station.objects.count() == 1
    assert str(station) == 'TestStation'


@pytest.mark.django_db
def test_move(user, move):
    """Тест создания объекта модели движения"""

    move = Move.objects.last()
    assert move.station.name == 'TestStation'
    assert move.user.username == 'TestUser'
    assert move.axis == 'z'
    assert move.distance == 1
    assert Move.objects.count() == 1
    assert str(move) == 'Перемещение по оси z на расстояние 1'
