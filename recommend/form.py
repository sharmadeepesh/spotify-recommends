from django.forms import ModelForm
from .models import Artist

class artistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name']