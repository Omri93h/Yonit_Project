from django.db import models
from django.contrib.auth.models import User
from PIL import Image 
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize

class Nancy(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) #relationship 1:n (user:todos) ??
    dateCreated = models.DateField(auto_now_add=True) #automatic
    dateCompleted = models.DateField(null=True, blank=True) #blank at first ?
    mealName = models.CharField(max_length=30)
    scheduled = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    mainIngredient = models.CharField(max_length=70)
    HasItamarTasted = models.BooleanField(default=False)
    Recipe = models.CharField(max_length=70)
    imagefile = models.ImageField(default='todo\static\nancy\images\Mashed_apple.png',upload_to='nancy/images')

    mediumIm=ImageSpecField(
        source='imagefile',processors=[SmartResize( 80,100)],format='PNG')
    
    smallIm=ImageSpecField(
        source='imagefile',processors=[SmartResize(40,50)],format='PNG')
   
    bigImage=ImageSpecField(
        source='imagefile',processors=[SmartResize(200,300)],format='PNG')
   
    def __str__(self):
        return self.mealName


