from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from api import views
from rest_framework.routers import DefaultRouter

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'accounts', views.UserViewSet, base_name='user')
router.register(r'families', views.FamilyViewSet, base_name='family')

urlpatterns = [
    url(r'^v1/drf/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/auth/login/$', obtain_jwt_token),
    url(r'^v1/auth/refresh/$', refresh_jwt_token),
    url(r'^v1/auth/verify/$', verify_jwt_token),
    url(r'^v1/', include(router.urls, namespace='v1')),
]

