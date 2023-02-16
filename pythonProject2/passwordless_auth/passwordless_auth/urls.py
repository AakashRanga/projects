
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hacker.urls')),
    path('',include('photos.urls')),
    path('',include('users.urls')),
    path('chat_app/',include('chat.urls')),
    path('',include('room.urls')),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += staticfiles_urlpatterns()