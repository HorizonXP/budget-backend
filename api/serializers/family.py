from rest_framework.serializers import ModelSerializer
from api import models

class FamilySerializer(ModelSerializer):
    class Meta:
        model = models.Family



