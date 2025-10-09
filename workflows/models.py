import uuid_utils as uuid
from django.db import models

from .choices import WorkflowRunStatusChoices


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    version = models.PositiveIntegerField()
    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    definition = models.JSONField()

    class Meta:
        unique_together = ("key", "version")
        ordering = ("key", "-version")


class WorkflowRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=WorkflowRunStatusChoices.choices, default=WorkflowRunStatusChoices.PENDING)
    execution_state = models.JSONField(default=dict)
