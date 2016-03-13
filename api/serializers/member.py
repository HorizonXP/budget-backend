from rest_framework.serializers import ModelSerializer
from api import models

class MemberSerializer(ModelSerializer):
    class Meta:
        model = models.Member


