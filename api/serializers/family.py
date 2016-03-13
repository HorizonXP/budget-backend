from rest_framework.serializers import ModelSerializer
from api import models
from .member import MemberSerializer

class FamilySerializer(ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = models.Family



