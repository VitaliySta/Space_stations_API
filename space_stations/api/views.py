from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from stations.models import Station

from .serializers import MoveSerializer, PositionSerializer, StationSerializer
from .utils import descriptions


@extend_schema_view(**descriptions)
class StationViewSet(viewsets.ModelViewSet):

    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    @action(
        detail=True,
        methods=('get', 'post'),
        serializer_class=PositionSerializer
    )
    def state(self, request, pk):
        station = self.get_object()

        if request.method == 'POST':
            serializer = MoveSerializer(data=request.data)
            if serializer.is_valid():
                distance = serializer.validated_data['distance']
                axis = serializer.validated_data['axis']
                new_distance = station.__getattribute__(axis)
                new_distance += distance
                setattr(station, axis, new_distance)
                station.save()
                serializer.save(station=station, user=request.user)
                return Response(self.serializer_class(station).data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(self.serializer_class(station).data)
