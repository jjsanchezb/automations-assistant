from rest_framework import serializers

from .models import Integration, IntegrationAction, IntegrationTrigger


class IntegrationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationAction
        fields = "__all__"


class IntegrationTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationTrigger
        fields = "__all__"


class IntegrationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = "__all__"


class IntegrationWriteSerializer(serializers.ModelSerializer):
    actions = IntegrationActionSerializer(many=True, write_only=True)
    triggers = IntegrationTriggerSerializer(many=True, write_only=True)

    class Meta:
        model = Integration
        fields = "__all__"

    def create(self, validated_data):
        return self.Meta.model.objects.create_integration(**validated_data)
