from django.urls import path,include
from . import views
from . import views as qv
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"videos", qv.VideoViewSet)



app_name = 'video_app'


urlpatterns = [
    
    path('video', views.showvideo, name='video'),
     path('', include(router.urls)),
   

 
    ]