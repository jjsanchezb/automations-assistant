from rest_framework import generics, parsers

from .models import Integration
from .serializers import IntegrationReadSerializer, IntegrationWriteSerializer


class ListIntegrations(generics.ListCreateAPIView):
    queryset = Integration.objects.all()
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return IntegrationWriteSerializer

        return IntegrationReadSerializer
