from django.db import models
from django.conf import settings


class Session(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expire_time = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_by_user(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            pass
