from api import serializers, models

from rest_framework import viewsets

class FamilyViewSet(viewsets.ModelViewSet):
    model = models.Family
    queryset = models.Family.objects.all()
    serializer_class = serializers.FamilySerializer
