from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=70)

    def __str__(self):
        return f"Users(login: {self.login}, password: {self.password})"


class Locations(models.Model):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(decimal_places=10, max_digits=10)
    longitude = models.DecimalField(decimal_places=10, max_digits=10)

    def __str__(self):
        return f"Locations(name: {self.name}, latitude: {self.latitude}), longitude: {self.longitude}"
