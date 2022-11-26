import pytest

from stations.models import Move, Station


@pytest.fixture()
def station():
    return Station.objects.create(name='TestStation',)


@pytest.fixture
def move(station, user):
    return Move.objects.create(
        station=station,
        user=user,
        distance=1,
        axis='z',
    )
