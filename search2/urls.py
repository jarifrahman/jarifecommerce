from django.urls import path

from .views import Csearch, Csearchpage




urlpatterns = [
    path('csearchpage', Csearchpage.as_view(), name='csearchpage'),
    path('search', Csearch.as_view(), name='csearch'),
   
    
    ]