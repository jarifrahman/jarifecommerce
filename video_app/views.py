from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Video
from .forms import VideoForm
from .serializers import VideoSerializer
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q


# Create your views here.

def showvideo(request):

    video= Video.objects


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

       
    
    context= {'video': video,
              'form': form
              }
    
      
    return render(request, 'video.html', context)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    #  authentication_classes=(TokenAuthentication, )
    # permission_classes = (IsAuthenticated )

