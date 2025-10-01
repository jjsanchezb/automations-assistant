from django.db import models


class SourceCodeLocation(models.TextChoices):
    IN_APP_MODULE = "in_app_module", "In-App Module (Bundled)"
    S3_ARTIFACT = "s3_artifact", "S3 Bucket Artifact (Dynamic)"


class RuntimeChoices(models.TextChoices):
    SUBPROCESS = "subprocess", "Subprocess"
    CONTAINER = "container", "Container"
