from django.contrib import admin

# Register your models here.
from .models import Integration, IntegrationAction, IntegrationTrigger

admin.site.register(Integration)
admin.site.register(IntegrationAction)
admin.site.register(IntegrationTrigger)
