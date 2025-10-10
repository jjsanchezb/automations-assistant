import uuid_utils as uuid
from django.db import models, transaction

from .choices import RuntimeChoices


class IntegrationQuerySet(models.QuerySet):
    def create_integration(self, **kwargs):
        """
        Creates an Integration aggregate (integration + actions + triggers)
        in a single, atomic transaction.
        """
        # Pop the nested data for actions and triggers
        actions_data = kwargs.pop("actions", [])
        triggers_data = kwargs.pop("triggers", [])

        integration_key = kwargs.get("key")
        with transaction.atomic():
            # Lock the relevant rows in the table.
            # Any other process trying to do this for the same 'key' will
            # have to wait until this transaction is complete.
            queryset = self.filter(key=integration_key).select_for_update()

            # Get the current max version from the locked queryset.
            current_max_version = queryset.aggregate(max_version=models.Max("version"))["max_version"] or 0

            new_version = current_max_version + 1
            kwargs["version"] = new_version

            # Create the new integration instance.
            integration = self.create(**kwargs)

            # Create the related actions and triggers
            # For performance, you could use bulk_create here
            for action_data in actions_data:
                IntegrationAction.objects.create(integration=integration, **action_data)

            for trigger_data in triggers_data:
                IntegrationTrigger.objects.create(integration=integration, **trigger_data)

        return integration


class IntegrationManager(models.Manager):
    def get_queryset(self):
        return IntegrationQuerySet(self.model, using=self._db)

    def create_integration(self, **kwargs):
        return self.get_queryset().create_integration(**kwargs)


class Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    key = models.CharField(max_length=100)
    version = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=False)
    source_code = models.FileField(upload_to="integrations/source_code/", null=True)
    runtime = models.CharField(max_length=100, choices=RuntimeChoices.choices, default=RuntimeChoices.SUBPROCESS)

    class Meta:
        unique_together = ("key", "version")
        ordering = ("key", "-version")

    objects: "IntegrationManager" = IntegrationManager()


class IntegrationAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7)
    key = models.CharField(max_length=100)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name="actions")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
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
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=False)
    entrypoint_function = models.CharField(max_length=100)
    input_schema = models.JSONField(blank=True, null=True)
    output_schema = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ("integration", "key")
