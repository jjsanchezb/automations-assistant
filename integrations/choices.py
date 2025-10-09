from django.db import models


class RuntimeChoices(models.TextChoices):
    SUBPROCESS = "subprocess", "Subprocess"
    CONTAINER = "container", "Container"
