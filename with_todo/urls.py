"""with_todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.registerForm, name='registerForm'),
    path('', views.homepage, name='homepage'),
    path('home', views.homepage,name="home2"),
    path('logout', views.logoutuser, name='logoutuser'),
    path('login', views.loginuser, name='loginuser'),
    path('createNewMeal/', views.createNewMeal, name='createNewMeal'),
    path('update/<int:meal_pk>', views.update, name='update'),
    path('nancy' ,views.nancy, name='nancy'),
    path('mealData/<int:meal_pk>', views.mealData, name='mealData'),
    path('mealData/<int:meal_pk>/deleteMeal', views.deleteMeal, name='deleteMeal'),
  # path('meals/<int:meal_pk>/deleteMeal', views.deleteMeal, name='deleteMeal2'),
    path('meals' ,views.meals, name='meals')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

