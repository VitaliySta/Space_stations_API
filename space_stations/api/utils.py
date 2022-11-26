from drf_spectacular.utils import extend_schema

from .serializers import MoveSerializer, PositionSerializer


descriptions = {
    "list": extend_schema(
        description='Displays a list of all stations.'
    ),
    "create": extend_schema(
        description='Creates a station'
                    '(you must enter the **name** of the station).'
    ),
    "retrieve": extend_schema(
        description='Displays data of a specific station by **id**.'
    ),
    "update": extend_schema(
        description='Update specific station data by **id**.'
    ),
    "partial_update": extend_schema(
        description='Partial update specific station data by **id**.'
    ),
    "destroy": extend_schema(
        description="Delete specific station by **id**."
    ),
    "state": [
        extend_schema(request=PositionSerializer, responses=MoveSerializer),
        extend_schema(
            description='Displays the position of a specific station.',
            methods=["GET"],
        ),
        extend_schema(
            description='Changing the position of a specific station (enter '
                        'one of the **axis (x, y, z)** and **distance**).',
            methods=["POST"],
        ),
    ],
}
