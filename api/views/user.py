from api import serializers, permissions
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    model = get_user_model()
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminOrSelf]

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        initialized_request = self.initialize_request(request, *args, **kwargs)
        if kwargs.get('pk') == 'current' and initialized_request.user.is_authenticated():
            kwargs['pk'] = initialized_request.user.pk
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

