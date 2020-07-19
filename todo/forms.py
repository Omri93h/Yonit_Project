from django.forms import ModelForm
from .models import Nancy
from django import forms


class NancyForm(forms.ModelForm):
    class Meta:
        model = Nancy
        fields = ['mealName', 'description', 'Ingredients',
                  'HasItamarTasted', 'Recipe', 'imagefile']
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": "3", "cols": "40", "style":"resize:none"}
            )
        }
