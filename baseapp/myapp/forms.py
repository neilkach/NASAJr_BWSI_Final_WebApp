from django import forms
from .models import Image

# Create your models here.
class ImgForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
