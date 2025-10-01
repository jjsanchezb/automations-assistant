from django.urls import path

from .api import ListIntegrations

urlpatterns = [path("", ListIntegrations.as_view())]
