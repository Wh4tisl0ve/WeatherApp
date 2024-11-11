from django.db import models
from django.conf import settings


class Locations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "latitude", "longitude"], name="unique_locations"),
        ]
