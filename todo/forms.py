from django.forms import ModelForm
from .models import Nancy


class NancyForm(ModelForm):
    class Meta:
        model = Nancy
        fields = ['mealName', 'description', 'Ingredients' ,'HasItamarTasted','Recipe','imagefile']






