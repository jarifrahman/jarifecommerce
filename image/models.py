from django.db import models
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2, decode_predictions, preprocess_input
# Create your models here.
class Image(models.Model):
    picture = models.ImageField()
    classified = models.CharField(blank= True, max_length= 200)
    uploaded = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.classified
'''
    def save(self, *args, **kwargs):
        try:
            img = load_img(self.picture, target_size=(299,299))
            img_array = img_to_array(img)
            
            to_pred = np.expand_dims(img_array,axis=0)
            prep = preprocess_input(to_pred)
            model = InceptionResNetV2(weights='imagnet')
            prediction = model.predict(prep)
            decoded = decode_predictions(prediction)[0][0][1]
            self.classified = str(decoded)
            
        except Exception as e:
            print('classification failed', e)

        super().save(*args,**kwargs)
'''