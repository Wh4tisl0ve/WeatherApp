from django.db import models
from django.contrib.auth.models import User

class Locations(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(decimal_places=10, max_digits=10)
    longitude = models.DecimalField(decimal_places=10, max_digits=10)

    def __str__(self):
        return f"Locations(name: {self.name}, latitude: {self.latitude}), longitude: {self.longitude}"
