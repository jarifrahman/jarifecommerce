from django.shortcuts import render
from .models import Image
from .serializers import ImageSerializer
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    #  authentication_classes=(TokenAuthentication, )
    # permission_classes = (IsAuthenticated )

def index(request):
    if  request.method == "POST":
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)
        original = load_img(file_url, target_size=(224, 224))
        numpy_image = img_to_array(original)
        

        image_batch = np.expand_dims(numpy_image, axis=0)
        # prepare the image for the VGG model
        processed_image = vgg16.preprocess_input(image_batch.copy())
        
        # get the predicted probabilities for each class
        with settings.GRAPH1.as_default():
            set_session(settings.SESS)
            predictions=settings.VGG_MODEL.predict(processed_image)
       
        label = decode_predictions(predictions)
        label = list(label)[0]
        response['name'] = str(label)
        return render(request,'homepage.html',response)
    else:
        return render(request,'homepage.html')