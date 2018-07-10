from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField


class World(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    init_info = JSONField()
    # history = JSONField()
