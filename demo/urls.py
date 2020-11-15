from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
   # path('video/', include('video_app.urls')),
    path('', include('core.urls', namespace='core')),
     path('tracking/', include('tracking.urls')),
     path('maps/', include('maps.urls')),
   
     path('search/', include('search2.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
