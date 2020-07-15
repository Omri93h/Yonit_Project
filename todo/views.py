# from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import  NancyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Nancy
from django.utils import timezone


def registerForm(request):
    if (request.method == 'GET'):
        return render(request, 'nancy/registerForm.html', {'form': UserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('nancy')
            except IntegrityError:
                return render(request, 'nancy/registerForm.html', {'form': UserCreationForm(), "errMsg": "User exists. Choose a different one" })
        else:
            return render(request, 'nancy/registerForm.html', {'form': UserCreationForm(), "errMsg": "Password didn't match" })


def nancy(request):
    return render(request, 'nancy/index1.html')

@login_required
def meals(request):
    meal = Nancy.objects.filter(user_id = request.user).order_by('-dateCreated')
    return render(request, 'nancy/meals.html',{'allmeals':meal})

@login_required
def mealData(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk)
    form = NancyForm(instance=meal)
    # creator=get_object_or_404(User,pk=meal.user_id)
    if (request.method == 'GET'):
        return render(request, 'nancy/meal-data.html', {'meal': meal, 'form': form , 'creator':meal.user_id})
    else:
        # meal = get_object_or_404(Nancy, pk=meal_pk) #, user_id=request.user
        try:
            # form = NancyForm(request.POST, instance=meal)
            form.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/meal-data.html', {'form': form, 'errMsg': "Data mismatch"})




def homepage(request):
    return render(request, 'nancy/index.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('homepage') 

def update(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk)

    if (request.method == 'GET'):
        form = NancyForm(instance=meal)
        act=2
        return render(request, 'nancy/create-meal.html', {'meal': meal, 'form': form ,'act':act})
    else:
        try:
            form = NancyForm(request.POST, instance=meal)
            form.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/create-meal.html', {'form': form, 'errMsg': "Data mismatch"})

def loginuser(request):
    if (request.method == 'GET'):
        return render(request, 'nancy/loginform.html', {'form': AuthenticationForm() })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'nancy/loginform.html', {'form': AuthenticationForm(), "errMsg": "User doesn't exist" })
        else:
            login(request, user)
            return redirect('nancy')



  
def createNewMeal(request):
    if request.method == 'GET':
        act=1
        return render(request, 'nancy/create-meal.html', {'form': NancyForm(),'act':act})
    else:
        try:
            form = NancyForm(request.POST,request.FILES)
            newMeal = form.save(commit=False) #commit=False
            newMeal.user_id = request.user
            newMeal.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/create-meal.html', {'form': NancyForm(), 'errMsg': 'Data mismatch'})




@login_required
def deleteMeal(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk, user_id=request.user)

    if (request.method == 'POST'):
        meal.delete()
        return redirect('meals') 
    

           
