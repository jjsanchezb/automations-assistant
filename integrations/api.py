from rest_framework import generics

from .models import Integration
from .serializers import IntegrationSerializer


class ListIntegrations(generics.ListAPIView):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
