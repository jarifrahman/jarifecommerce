from django.urls import path, include
from django.urls import path
from .views import (
   ImageViewSet,index
)
from rest_framework.routers import DefaultRouter

from . import views as qv

router = DefaultRouter()
router.register(r"images", qv.ImageViewSet)



app_name = 'core'

urlpatterns = [
    
    
    path("api/", include(router.urls)), 
    path("classify/", index, name = 'classify'), 
    
   
]


