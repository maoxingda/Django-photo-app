"""Photo app Forms"""
from django import forms

from photoapp.models import Photo


class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('submitter', )
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
