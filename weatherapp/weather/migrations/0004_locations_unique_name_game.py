# Generated by Django 5.1.2 on 2024-11-02 12:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_alter_locations_latitude_alter_locations_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='locations',
            constraint=models.UniqueConstraint(fields=('users', 'name', 'latitude', 'longitude'), name='unique_name_game'),
        ),
    ]
