from django.db import models


class WorkflowRunStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELED = "canceled", "Canceled"
