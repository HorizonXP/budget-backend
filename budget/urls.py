from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from api import urls as apiUrls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(apiUrls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
