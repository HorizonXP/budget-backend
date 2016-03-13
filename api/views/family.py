from api import serializers, models, permissions
from rest_framework import viewsets
from rest_framework.filters import DjangoObjectPermissionsFilter

class FamilyViewSet(viewsets.ModelViewSet):
    model = models.Family
    queryset = models.Family.objects.all()
    serializer_class = serializers.FamilySerializer
    filter_backends = (DjangoObjectPermissionsFilter,)
    permission_classes = (permissions.DjangoObjectPermissionsWithView,)
