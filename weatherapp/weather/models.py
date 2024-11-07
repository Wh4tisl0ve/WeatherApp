from django.db import models
from django.conf import settings


class Locations(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Locations(name: {self.name}, latitude: {self.latitude}), longitude: {self.longitude}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["users", "name", "latitude", "longitude"], name="unique_locations"),
        ]
