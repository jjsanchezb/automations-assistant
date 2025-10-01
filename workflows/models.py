import uuid_utils as uuid
from django.db import models


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    name = models.CharField(max_length=100)
