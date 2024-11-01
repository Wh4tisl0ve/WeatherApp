from django.db import models
from django.contrib.auth.models import User

class Locations(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Locations(name: {self.name}, latitude: {self.latitude}), longitude: {self.longitude}"
