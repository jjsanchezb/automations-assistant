import uuid_utils as uuid
from django.db import models

from .choices import RuntimeChoices


class Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    key = models.CharField(max_length=100)
    version = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=False)
    source_code = models.FileField(upload_to="integrations/source_code/", null=True)
    runtime = models.CharField(max_length=100, choices=RuntimeChoices.choices, default=RuntimeChoices.SUBPROCESS)

    class Meta:
        unique_together = ("key", "version")
        ordering = ("key", "-version")


class IntegrationAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    key = models.CharField(max_length=100)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name="actions")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=False)
    entrypoint_function = models.CharField(max_length=100)
    input_schema = models.JSONField(blank=True, null=True)
    output_schema = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ("integration", "key")


class IntegrationTrigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    key = models.CharField(max_length=100)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name="triggers")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=False)
    entrypoint_function = models.CharField(max_length=100)
    input_schema = models.JSONField(blank=True, null=True)
    output_schema = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ("integration", "key")
