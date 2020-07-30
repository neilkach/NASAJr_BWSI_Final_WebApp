from django.shortcuts import render
from . import forms as F
from .models import Image
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import tensorflow.python.saved_model
import numpy as np
from numpy import asarray
from PIL import Image

# Create your views here.

def home(request):
    return render(request, 'home.html')

def model(request):
    if request.method == "POST":
        context = F.ImgForm(request.POST, request.FILES)
        img = context.save()

        my_model = tf.keras.models.load_model('final_model.h5')

        image = Image.open(img.image.path).resize((224,224))
        image_arr = np.asarray(image)[np.newaxis]
        image_array = image_arr/255

        #This will be your classifaction
        outputs = my_model.predict(image_array)
        print('hello')
        print(outputs[0])
        index = np.where(outputs[0] == np.amax(outputs[0]))
        index=index[0][0]
        result = None
        # print(np.amax(outputs[0]))
        # print(index[0][0])
        if (index == 0):
            result = 'Lung Adenocarcinoma'
        elif (index ==1):
            result = 'Benign'
        elif (index==2):
            result = 'Lung Squamous Cell Carcinoma'
        p1 = 'Benign.....................................................: '+ str(round(outputs[0][1]*100, 2)) + '%' 
        p2 = 'Lung Adenocarcinoma....................: ' + str(round(outputs[0][0]*100, 2)) + '%'
        p3 = 'Lung Squamous Cell Carcinoma: ' + str(round(outputs[0][2]*100, 2)) + '%'
        
        return render(request, 'model.html', {'context': context, 'img': img, 'result': result, 'p1': p1, 'p2': p2, 'p3': p3})
    else:
        context = F.ImgForm()
    return render(request, 'model.html', {'context': context})
