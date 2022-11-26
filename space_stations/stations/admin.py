from django.contrib import admin

from .models import Move, Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'condition',
        'date_create',
        'date_crash',
        'x',
        'y',
        'z',
    )


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'station',
        'user',
        'axis',
        'distance',
    )
