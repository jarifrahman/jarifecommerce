from rest_framework import serializers

from .models import Video
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User








class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id','name','videofile')


