from datetime import datetime
from django.db import models

from users.models import User


class Station(models.Model):
    """Class station"""

    name = models.CharField(
        max_length=255,
        verbose_name='Название станции',
    )
    condition = models.CharField(
        max_length=7,
        default='running',
        verbose_name='Состояние станции',
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания станции',
    )
    date_crash = models.DateTimeField(
        null=True,
        blank=True,
    )
    x = models.IntegerField(
        default=100,
        verbose_name='Ось x',
    )
    y = models.IntegerField(
        default=100,
        verbose_name='Ось y',
    )
    z = models.IntegerField(
        default=100,
        verbose_name='Ось z',
    )

    def save(self, *args, **kwargs):
        if any((self.x < 1, self.y < 1, self.z < 1)):
            self.condition = 'broken'
            if not self.date_crash:
                self.date_crash = datetime.utcnow()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'

    def __str__(self):
        return self.name


class Move(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='stat_move',
        verbose_name='Станция'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    axis = models.CharField(
        max_length=1,
        verbose_name='Ось координат',
    )
    distance = models.IntegerField(
        verbose_name='Дистанция',
    )

    class Meta:
        verbose_name = 'Перемещение'
        verbose_name_plural = 'Перемещение'

    def __str__(self):
        return f'Перемещение по оси {self.axis} на расстояние {self.distance}'
