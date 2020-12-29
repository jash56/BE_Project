from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]

urlpatters = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)