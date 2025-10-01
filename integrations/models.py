import uuid_utils as uuid
from django.db import models


class SourceCodeLocation(models.TextChoices):
    IN_APP_MODULE = "in_app_module", "In-App Module (Bundled)"
    S3_ARTIFACT = "s3_artifact", "S3 Bucket Artifact (Dynamic)"


class RuntimeChoices(models.TextChoices):
    SUBPROCESS = "subprocess", "Subprocess"
    CONTAINER = "container", "Container"


class Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    source_code_location = models.CharField(max_length=255, choices=SourceCodeLocation.choices, default=SourceCodeLocation.S3_ARTIFACT)
    source_code_path = models.CharField(max_length=100, null=True)
    runtime = models.CharField(max_length=100, choices=RuntimeChoices.choices, default=RuntimeChoices.SUBPROCESS)
    description = models.TextField(blank=True)


class IntegrationAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    name = models.CharField(max_length=100)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    entrypoint_function = models.CharField(max_length=100)
    input_schema = models.JSONField(null=True, default=None)
    output_schema = models.JSONField(null=True, default=None)
    description = models.TextField(blank=True)


class IntegrationTrigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    name = models.CharField(max_length=100)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    entrypoint_function = models.CharField(max_length=100)
    input_schema = models.JSONField(null=True, default=None)
    output_schema = models.JSONField(null=True, default=None)
    description = models.TextField(blank=True)
