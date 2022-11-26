from rest_framework import serializers

from stations.models import Move, Station


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'condition',
            'date_create',
            'date_crash',
        )
        read_only_fields = ('condition', 'date_crash',)

    def validate(self, attrs):
        print('Читай тут', attrs)
        return attrs


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = (
            'x',
            'y',
            'z',
        )

    def validate(self, attrs):
        print('Читай тут', attrs)
        return attrs


class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = (
            'axis',
            'distance',
        )
