import pytest

from django.urls import reverse

from stations.models import Station


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, status',
    [
        ('api:stations-list', 200),
        ('api:stations-detail', 200),
        ('api:stations-state', 200),
    ],
)
def test_get_request_url(station, client, url, status):
    """Тест GET запроса"""

    station_id = Station.objects.last().id
    if url == 'api:stations-list':
        response = client.get(reverse(url))
    else:
        response = client.get(reverse(url, kwargs={'pk': station_id}))

    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "axis, distance, condition, new_distance",
    [
        ("x", -5, "running", 95),
        ("x", -100, "broken", 0),
        ("y", 37, "running", 137),
        ("y", -111, "broken", -11),
        ("z", -88, "running", 12),
        ("z", -433, "broken", -333),
    ],
)
def test_move_state(
    station, admin_client, axis, distance, condition, new_distance
):
    """Тестирование перемещения станции"""

    station_id = Station.objects.last().id
    url_detail = reverse('api:stations-detail', kwargs={'pk': station_id})
    url_state = reverse('api:stations-state', kwargs={'pk': station_id})
    response_detail = admin_client.get(url_detail)
    response_state = admin_client.get(url_state)
    assert response_state.data['x'] == 100
    assert response_state.data['y'] == 100
    assert response_state.data['z'] == 100
    assert response_state.status_code == 200
    assert response_detail.status_code == 200
    assert response_detail.data['condition'] == 'running'

    data = {
        'axis': axis,
        'distance': distance,
    }

    admin_client.post(url_state, data=data)
    station = Station.objects.last()
    assert station.id == 1
    assert station.condition == condition
    assert station.__getattribute__(axis) == new_distance


@pytest.mark.django_db
@pytest.mark.parametrize(
    "axis, distance",
    [
        ('w', 10),
        ('http', 10),
        ('1', 10),
        (10, 10),
        ('%', 10),
        ('', 10)
    ],
)
def test_move_axis_wrong(station, admin_client, axis, distance):
    """Тест неверное значение axis"""

    station_id = Station.objects.last().id
    url = reverse('api:stations-state', kwargs={'pk': station_id})

    data = {
        'axis': axis,
        'distance': distance
    }
    response = admin_client.post(url, data=data)

    assert response.status_code == 400
    if isinstance(axis, int):
        assert response.json() == {'axis': ['Убедитесь, что это значение'
                                            ' содержит не более 1 символов.']}
    elif len(axis) > 1:
        assert response.json() == {'axis': ['Убедитесь, что это значение'
                                            ' содержит не более 1 символов.']}
    elif not axis:
        assert response.json() == {'axis': ['Это поле не может быть пустым.']}
    else:
        assert response.json() == {
            'axis': [f'Вы ввели неверную ось координат - {axis}! '
                     f'Введите - x или y или z']
        }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "axis, distance",
    [
        ('x', 10.1),
        ('x', 'x'),
        ('x', '%'),
        ('x', ''),
    ],
)
def test_move_distance_wrong(station, admin_client, axis, distance):
    """Тест неверное значение distance"""

    station_id = Station.objects.last().id
    url = reverse('api:stations-state', kwargs={'pk': station_id})

    data = {
        'axis': axis,
        'distance': distance
    }
    response = admin_client.post(url, data=data)

    assert response.status_code == 400
